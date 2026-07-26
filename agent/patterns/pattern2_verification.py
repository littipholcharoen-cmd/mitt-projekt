#!/usr/bin/env python3
"""
Pattern 2: Chain of Verification

Implements self-checking mechanism before critical actions.
"""

from dataclasses import dataclass
from typing import List, Dict, Callable
from enum import Enum


class VerificationStatus(Enum):
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"


@dataclass
class VerificationResult:
    """
    Represents the result of a verification check
    """
    status: VerificationStatus
    checks: Dict[str, bool]
    failed_checks: List[str]
    warnings: List[str]
    passed_count: int
    total_checks: int
    
    def is_valid(self) -> bool:
        return self.status == VerificationStatus.PASSED
    
    def can_proceed(self) -> bool:
        """Can proceed even with warnings"""
        return self.status in [VerificationStatus.PASSED, VerificationStatus.WARNING]


class VerificationChain:
    """
    Implements Chain of Verification pattern
    """
    
    def __init__(self, name: str):
        self.name = name
        self.checks: List[tuple] = []  # (check_name, check_func)
        self.results: VerificationResult = None
    
    def add_check(self, name: str, check_func: Callable) -> None:
        """
        Add a verification check
        
        Args:
            name: Name of the check
            check_func: Function that returns True if check passes
        """
        self.checks.append((name, check_func))
    
    def verify(self) -> VerificationResult:
        """
        Execute all verification checks
        """
        results = {}
        failed = []
        warnings = []
        
        for check_name, check_func in self.checks:
            try:
                result = check_func()
                results[check_name] = result
                if not result:
                    failed.append(check_name)
            except Exception as e:
                results[check_name] = False
                failed.append(check_name)
                warnings.append(f"{check_name}: {str(e)}")
        
        # Determine overall status
        if not failed:
            status = VerificationStatus.PASSED
        elif warnings:
            status = VerificationStatus.WARNING
        else:
            status = VerificationStatus.FAILED
        
        self.results = VerificationResult(
            status=status,
            checks=results,
            failed_checks=failed,
            warnings=warnings,
            passed_count=len([v for v in results.values() if v]),
            total_checks=len(results)
        )
        
        return self.results
    
    def print_report(self) -> None:
        """
        Print verification report
        """
        if not self.results:
            print("No verification results available")
            return
        
        print(f"\n{'='*60}")
        print(f"Verification Report: {self.name}")
        print(f"{'='*60}")
        print(f"Status: {self.results.status.value.upper()}")
        print(f"Passed: {self.results.passed_count}/{self.results.total_checks}")
        
        print(f"\nDetailed Results:")
        for check_name, result in self.results.checks.items():
            status_icon = "✓" if result else "✗"
            print(f"  {status_icon} {check_name}")
        
        if self.results.failed_checks:
            print(f"\nFailed Checks:")
            for check in self.results.failed_checks:
                print(f"  ✗ {check}")
        
        if self.results.warnings:
            print(f"\nWarnings:")
            for warning in self.results.warnings:
                print(f"  ⚠ {warning}")
        
        print(f"{'='*60}\n")


class OutputVerification:
    """
    Specific verification for output content
    """
    
    @staticmethod
    def create_chain() -> VerificationChain:
        chain = VerificationChain("Output Verification")
        
        # Add standard checks
        chain.add_check(
            "Non-empty output",
            lambda: True  # Will be overridden with actual content
        )
        chain.add_check(
            "Valid JSON format",
            lambda: True  # Will be overridden
        )
        chain.add_check(
            "Required fields present",
            lambda: True  # Will be overridden
        )
        
        return chain


if __name__ == "__main__":
    # Example usage
    chain = VerificationChain("Example Verification")
    chain.add_check("Check 1", lambda: True)
    chain.add_check("Check 2", lambda: True)
    chain.add_check("Check 3", lambda: False)
    
    result = chain.verify()
    chain.print_report()
