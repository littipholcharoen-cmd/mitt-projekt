#!/usr/bin/env python3
"""
Pattern 1: Role + Constraints

Defines the agent's role and operational boundaries.
This pattern is the foundation for safe agent operation.
"""

from dataclasses import dataclass
from typing import List, Set
from enum import Enum


class ConstraintLevel(Enum):
    """Severity levels for constraint violations"""
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class RoleDefinition:
    """
    Defines what the agent IS and DOES
    """
    name: str
    description: str
    primary_objectives: List[str]
    
    def __init__(self):
        self.name = "AEX-Agent"
        self.description = (
            "Multi-platform autonomous AI agent capable of executing "
            "complex tasks across iOS, Android, Linux, and Windows platforms. "
            "Operates autonomously with safety constraints and error recovery."
        )
        self.primary_objectives = [
            "Execute assigned tasks across multiple platforms",
            "Maintain system reliability through error recovery",
            "Manage resources efficiently",
            "Provide actionable feedback and logging",
            "Comply with all safety constraints"
        ]


@dataclass
class ConstraintSet:
    """
    Defines what the agent CANNOT do
    """
    
    # Operational Constraints
    OPERATIONAL = [
        "Cannot modify files outside designated safe directories",
        "Cannot execute arbitrary shell commands",
        "Cannot make network requests to unauthorized domains",
        "Cannot exceed configured resource limits",
        "Cannot bypass authentication/authorization checks",
    ]
    
    # Safety Constraints (Guard Rails - Pattern 7)
    SAFETY = [
        "Cannot spend more than $0.50 per run on API calls",
        "Cannot send emails or SMS without explicit authorization",
        "Cannot access private user data without consent",
        "Cannot publish unverified information",
        "Cannot execute more than 3 retries per failed task",
    ]
    
    # Security Constraints
    SECURITY = [
        "Cannot store credentials in plaintext",
        "Cannot log sensitive information",
        "Cannot disable security features",
        "Cannot access system files or registry",
        "Cannot escalate privileges",
    ]
    
    def get_all_constraints(self) -> List[str]:
        return self.OPERATIONAL + self.SAFETY + self.SECURITY


class ConstraintValidator:
    """
    Validates actions against the constraint set
    """
    
    def __init__(self):
        self.constraints = ConstraintSet()
        self.violations: List[tuple] = []
    
    def validate_file_operation(self, operation: str, path: str, safe_dirs: List[str]) -> bool:
        """
        Validates file operations against constraints
        
        Args:
            operation: 'read', 'write', 'delete'
            path: file path to validate
            safe_dirs: list of safe directory paths
        
        Returns:
            True if operation is allowed, False otherwise
        """
        import os
        
        full_path = os.path.abspath(path)
        
        for safe_dir in safe_dirs:
            if full_path.startswith(os.path.abspath(safe_dir)):
                return True
        
        self.violations.append((
            ConstraintLevel.CRITICAL,
            f"Constraint violation: {operation} operation on {path} not in safe directories"
        ))
        return False
    
    def validate_api_cost(self, estimated_cost: float, max_cost: float = 0.50) -> bool:
        """
        Validates API call costs against budget
        """
        if estimated_cost > max_cost:
            self.violations.append((
                ConstraintLevel.CRITICAL,
                f"Constraint violation: Estimated API cost ${estimated_cost} exceeds limit ${max_cost}"
            ))
            return False
        return True
    
    def validate_retry_count(self, retry_count: int, max_retries: int = 3) -> bool:
        """
        Validates retry count against limit
        """
        if retry_count > max_retries:
            self.violations.append((
                ConstraintLevel.ERROR,
                f"Constraint violation: Retry count {retry_count} exceeds limit {max_retries}"
            ))
            return False
        return True
    
    def get_violations(self) -> List[tuple]:
        return self.violations
    
    def clear_violations(self):
        self.violations = []


if __name__ == "__main__":
    role = RoleDefinition()
    print(f"Agent: {role.name}")
    print(f"Description: {role.description}")
    print(f"\nPrimary Objectives:")
    for obj in role.primary_objectives:
        print(f"  - {obj}")
    
    constraints = ConstraintSet()
    print(f"\nConstraints:")
    for constraint in constraints.get_all_constraints():
        print(f"  ✗ {constraint}")
