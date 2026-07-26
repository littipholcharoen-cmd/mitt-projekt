#!/usr/bin/env python3
"""
Pattern 7: Guard Rails

Defines hard safety boundaries that override all other instructions.
"""

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum


class GuardRailType(Enum):
    SPENDING = "spending"
    COMMUNICATION = "communication"
    FILE_SYSTEM = "file_system"
    CONTENT = "content"
    SCOPE = "scope"
    EXECUTION = "execution"


@dataclass
class GuardRail:
    """
    Represents a single guard rail constraint
    """
    rail_type: GuardRailType
    description: str
    limit: Optional[float]
    allowed_resources: Optional[List[str]]
    enforcement_level: str  # "soft" or "hard"
    
    def check_violation(self, value: float) -> bool:
        """
        Check if guard rail is violated
        """
        if self.limit is None:
            return False
        return value > self.limit


class GuardRailSystem:
    """
    Implements Pattern 7: Guard Rails
    HARD LIMITS - these override ANY other instruction
    """
    
    HARD_LIMITS = [
        GuardRail(
            rail_type=GuardRailType.SPENDING,
            description="Never spend more than $0.50 per run",
            limit=0.50,
            allowed_resources=None,
            enforcement_level="hard"
        ),
        GuardRail(
            rail_type=GuardRailType.COMMUNICATION,
            description="Only communicate with authorized domains",
            limit=None,
            allowed_resources=[
                "api.slack.com",
                "api.github.com",
                "api.openai.com",
                "127.0.0.1",
                "localhost"
            ],
            enforcement_level="hard"
        ),
        GuardRail(
            rail_type=GuardRailType.FILE_SYSTEM,
            description="Never write outside designated directories",
            limit=None,
            allowed_resources=[
                "agent/",
                "data/",
                "logs/",
                "cache/"
            ],
            enforcement_level="hard"
        ),
        GuardRail(
            rail_type=GuardRailType.CONTENT,
            description="Never publish unverified or private information",
            limit=None,
            allowed_resources=None,
            enforcement_level="hard"
        ),
        GuardRail(
            rail_type=GuardRailType.EXECUTION,
            description="Never execute shell commands without verification",
            limit=None,
            allowed_resources=None,
            enforcement_level="hard"
        ),
    ]
    
    def __init__(self):
        self.violations: List[dict] = []
        self.warnings: List[dict] = []
    
    def check_spending(self, current_cost: float) -> bool:
        """
        Check spending guard rail
        """
        if current_cost > 0.50:
            self.violations.append({
                'type': GuardRailType.SPENDING.value,
                'message': f'Estimated API cost ${current_cost} exceeds limit $0.50',
                'action': 'HALT'
            })
            return False
        return True
    
    def check_communication(self, domain: str) -> bool:
        """
        Check communication guard rail
        """
        allowed_domains = [
            "api.slack.com",
            "api.github.com",
            "api.openai.com",
            "127.0.0.1",
            "localhost"
        ]
        
        if domain not in allowed_domains:
            self.violations.append({
                'type': GuardRailType.COMMUNICATION.value,
                'message': f'Communication to {domain} not authorized',
                'action': 'BLOCK'
            })
            return False
        return True
    
    def check_file_access(self, path: str, operation: str) -> bool:
        """
        Check file system guard rail
        """
        import os
        
        allowed_dirs = ["agent/", "data/", "logs/", "cache/"]
        full_path = os.path.abspath(path)
        
        for allowed_dir in allowed_dirs:
            if full_path.startswith(os.path.abspath(allowed_dir)):
                return True
        
        self.violations.append({
            'type': GuardRailType.FILE_SYSTEM.value,
            'message': f'File operation {operation} on {path} not in allowed directories',
            'action': 'BLOCK'
        })
        return False
    
    def check_scope(self, task_type: str, available_tools: List[str]) -> bool:
        """
        Check if task is within scope
        """
        valid_task_types = [
            'data_processing',
            'api_integration',
            'monitoring',
            'reporting',
            'logging'
        ]
        
        if task_type not in valid_task_types:
            self.violations.append({
                'type': GuardRailType.SCOPE.value,
                'message': f'Task type {task_type} not in scope',
                'action': 'BLOCK'
            })
            return False
        return True
    
    def enforce_all(self) -> bool:
        """
        Check all guard rails - if any are violated, return False
        """
        return len(self.violations) == 0
    
    def get_violations(self) -> List[dict]:
        return self.violations
    
    def print_guard_rails(self):
        """
        Print all guard rails
        """
        print("\n" + "="*60)
        print("GUARD RAILS (Pattern 7): Hard Limits Override Everything")
        print("="*60)
        
        for rail in self.HARD_LIMITS:
            print(f"\n[{rail.enforcement_level.upper()}] {rail.rail_type.value.upper()}")
            print(f"  {rail.description}")
            if rail.limit:
                print(f"  Limit: {rail.limit}")
            if rail.allowed_resources:
                print(f"  Allowed: {', '.join(rail.allowed_resources)}")
        
        print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    system = GuardRailSystem()
    system.print_guard_rails()
    
    # Test guard rails
    print("Testing Guard Rails:")
    print(f"Spending check ($0.30): {system.check_spending(0.30)}")
    print(f"Spending check ($1.00): {system.check_spending(1.00)}")
    print(f"\nViolations: {system.get_violations()}")
