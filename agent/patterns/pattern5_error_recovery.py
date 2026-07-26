#!/usr/bin/env python3
"""
Pattern 5: Error Recovery Instructions

Defines automatic error handling and recovery strategies.
"""

import logging
from enum import Enum
from dataclasses import dataclass
from typing import Optional, Callable
from datetime import datetime

logger = logging.getLogger(__name__)


class ErrorSeverity(Enum):
    RECOVERABLE = "recoverable"
    UNRECOVERABLE = "unrecoverable"
    WARNING = "warning"


class ErrorCode(Enum):
    RATE_LIMIT = "429"  # HTTP 429
    SERVICE_UNAVAILABLE = "503"  # HTTP 503
    FILE_NOT_FOUND = "404_FILE"
    JSON_PARSE_ERROR = "JSON_PARSE"
    TIMEOUT = "TIMEOUT"
    MISSING_CREDENTIALS = "CRED_MISSING"
    PERMISSION_DENIED = "PERM_DENIED"
    NETWORK_ERROR = "NETWORK"
    UNKNOWN = "UNKNOWN"


@dataclass
class ErrorRecoveryStrategy:
    """
    Defines how to handle specific errors
    """
    error_code: ErrorCode
    severity: ErrorSeverity
    max_retries: int
    wait_seconds: int
    fallback_action: Optional[str]
    log_location: str


class ErrorRecoveryHandler:
    """
    Implements Pattern 5: Error Recovery
    """
    
    # Recovery strategies for different error types
    RECOVERY_STRATEGIES = {
        ErrorCode.RATE_LIMIT: ErrorRecoveryStrategy(
            error_code=ErrorCode.RATE_LIMIT,
            severity=ErrorSeverity.RECOVERABLE,
            max_retries=3,
            wait_seconds=60,
            fallback_action="skip_source",
            log_location="logs/rate_limit.log"
        ),
        ErrorCode.SERVICE_UNAVAILABLE: ErrorRecoveryStrategy(
            error_code=ErrorCode.SERVICE_UNAVAILABLE,
            severity=ErrorSeverity.RECOVERABLE,
            max_retries=3,
            wait_seconds=60,
            fallback_action="skip_source",
            log_location="logs/service_errors.log"
        ),
        ErrorCode.FILE_NOT_FOUND: ErrorRecoveryStrategy(
            error_code=ErrorCode.FILE_NOT_FOUND,
            severity=ErrorSeverity.RECOVERABLE,
            max_retries=0,
            wait_seconds=0,
            fallback_action="use_default",
            log_location="logs/file_errors.log"
        ),
        ErrorCode.JSON_PARSE_ERROR: ErrorRecoveryStrategy(
            error_code=ErrorCode.JSON_PARSE_ERROR,
            severity=ErrorSeverity.RECOVERABLE,
            max_retries=0,
            wait_seconds=0,
            fallback_action="skip_item",
            log_location="logs/parse_errors.log"
        ),
        ErrorCode.MISSING_CREDENTIALS: ErrorRecoveryStrategy(
            error_code=ErrorCode.MISSING_CREDENTIALS,
            severity=ErrorSeverity.UNRECOVERABLE,
            max_retries=0,
            wait_seconds=0,
            fallback_action="halt",
            log_location="logs/HALT.txt"
        ),
    }
    
    def __init__(self):
        self.error_count = 0
        self.total_errors = {}
    
    def handle_error(
        self,
        error_code: ErrorCode,
        error_message: str,
        context: Optional[dict] = None
    ) -> dict:
        """
        Handle an error and return recovery instructions
        
        Returns:
            {
                'action': str,  # 'retry', 'skip', 'halt'
                'wait_seconds': int,
                'message': str
            }
        """
        strategy = self.RECOVERY_STRATEGIES.get(error_code)
        
        if not strategy:
            strategy = self.RECOVERY_STRATEGIES[ErrorCode.UNKNOWN]
        
        self.error_count += 1
        self.total_errors[error_code] = self.total_errors.get(error_code, 0) + 1
        
        # Log error
        self._log_error(strategy, error_message, context)
        
        # Determine action
        if strategy.severity == ErrorSeverity.UNRECOVERABLE:
            return self._handle_unrecoverable(strategy, error_message)
        else:
            return self._handle_recoverable(strategy, error_message)
    
    def _handle_recoverable(self, strategy: ErrorRecoveryStrategy, error_msg: str) -> dict:
        """
        Handle recoverable errors
        """
        action = "retry" if strategy.max_retries > 0 else "skip"
        
        return {
            'action': action,
            'wait_seconds': strategy.wait_seconds,
            'max_retries': strategy.max_retries,
            'fallback_action': strategy.fallback_action,
            'message': f"Recoverable error: {error_msg}. Action: {action}"
        }
    
    def _handle_unrecoverable(self, strategy: ErrorRecoveryStrategy, error_msg: str) -> dict:
        """
        Handle unrecoverable errors
        """
        return {
            'action': 'halt',
            'wait_seconds': 0,
            'message': f"UNRECOVERABLE ERROR: {error_msg}. Agent halting.",
            'log_to': 'HALT.txt',
            'halt_required': True
        }
    
    def _log_error(self, strategy: ErrorRecoveryStrategy, error_msg: str, context: dict):
        """
        Log error to appropriate location
        """
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'error_code': strategy.error_code.value,
            'severity': strategy.severity.value,
            'message': error_msg,
            'context': context
        }
        
        logger.warning(f"Error: {error_msg}")
        # In production, would write to strategy.log_location
    
    def get_error_summary(self) -> dict:
        """
        Get summary of all errors encountered
        """
        return {
            'total_errors': self.error_count,
            'error_breakdown': self.total_errors
        }


if __name__ == "__main__":
    handler = ErrorRecoveryHandler()
    
    # Example recoverable error
    result = handler.handle_error(
        ErrorCode.RATE_LIMIT,
        "API rate limit exceeded",
        {'source': 'external_api'}
    )
    print("Recoverable Error Result:", result)
    
    # Example unrecoverable error
    result = handler.handle_error(
        ErrorCode.MISSING_CREDENTIALS,
        "API credentials not found",
        {'env_var': 'API_KEY'}
    )
    print("Unrecoverable Error Result:", result)
