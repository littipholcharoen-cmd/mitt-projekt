#!/usr/bin/env python3
"""
Tests for the 10 Agent Patterns
"""

import pytest
import sys
from pathlib import Path

# Add agent module to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent.patterns.pattern1_role_constraints import (
    RoleDefinition, ConstraintSet, ConstraintValidator
)
from agent.patterns.pattern2_verification import (
    VerificationChain, VerificationStatus
)
from agent.patterns.pattern3_structured_output import (
    TaskOutput, OutputEnforcer
)
from agent.patterns.pattern5_error_recovery import (
    ErrorRecoveryHandler, ErrorCode, ErrorSeverity
)
from agent.patterns.pattern7_guard_rails import (
    GuardRailSystem, GuardRailType
)


class TestPattern1:
    """Test Pattern 1: Role + Constraints"""
    
    def test_role_definition(self):
        role = RoleDefinition()
        assert role.name == "AEX-Agent"
        assert len(role.primary_objectives) > 0
    
    def test_constraints_set(self):
        constraints = ConstraintSet()
        all_constraints = constraints.get_all_constraints()
        assert len(all_constraints) > 0
        assert any("Cannot" in c for c in all_constraints)
    
    def test_constraint_validator(self):
        validator = ConstraintValidator()
        safe_dirs = ['agent/', 'data/']
        
        # Valid path
        assert validator.validate_file_operation('read', 'data/test.txt', safe_dirs)
        
        # Invalid path
        assert not validator.validate_file_operation('write', '/etc/passwd', safe_dirs)


class TestPattern2:
    """Test Pattern 2: Chain of Verification"""
    
    def test_verification_chain(self):
        chain = VerificationChain("Test Chain")
        chain.add_check("Check 1", lambda: True)
        chain.add_check("Check 2", lambda: False)
        
        result = chain.verify()
        
        assert result.passed_count == 1
        assert result.total_checks == 2
        assert result.status == VerificationStatus.FAILED
    
    def test_all_checks_pass(self):
        chain = VerificationChain("All Pass")
        chain.add_check("Check 1", lambda: True)
        chain.add_check("Check 2", lambda: True)
        
        result = chain.verify()
        assert result.status == VerificationStatus.PASSED


class TestPattern3:
    """Test Pattern 3: Structured Output Enforcement"""
    
    def test_task_output_validation(self):
        output = TaskOutput(
            task_id="task_001",
            status="success",
            timestamp="2026-07-26T12:00:00",
            result={"data": "test"}
        )
        
        assert output.validate()
    
    def test_task_output_json(self):
        output = TaskOutput(
            task_id="task_001",
            status="success",
            timestamp="2026-07-26T12:00:00"
        )
        
        json_str = output.to_json()
        assert '"task_id"' in json_str
        assert '"status"' in json_str


class TestPattern5:
    """Test Pattern 5: Error Recovery"""
    
    def test_recoverable_error(self):
        handler = ErrorRecoveryHandler()
        result = handler.handle_error(
            ErrorCode.RATE_LIMIT,
            "API rate limit"
        )
        
        assert result['action'] in ['retry', 'skip']
        assert result['wait_seconds'] > 0
    
    def test_unrecoverable_error(self):
        handler = ErrorRecoveryHandler()
        result = handler.handle_error(
            ErrorCode.MISSING_CREDENTIALS,
            "Missing API key"
        )
        
        assert result['action'] == 'halt'


class TestPattern7:
    """Test Pattern 7: Guard Rails"""
    
    def test_spending_guard_rail(self):
        system = GuardRailSystem()
        
        # Within limit
        assert system.check_spending(0.25)
        
        # Over limit
        assert not system.check_spending(1.00)
    
    def test_communication_guard_rail(self):
        system = GuardRailSystem()
        
        # Allowed
        assert system.check_communication("api.github.com")
        
        # Not allowed
        assert not system.check_communication("evil.com")
    
    def test_file_access_guard_rail(self):
        system = GuardRailSystem()
        
        # Allowed directory
        assert system.check_file_access("logs/test.log", "write")
        
        # Not allowed directory
        assert not system.check_file_access("/etc/passwd", "read")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
