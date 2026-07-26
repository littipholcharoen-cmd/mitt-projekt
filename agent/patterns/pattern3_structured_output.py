#!/usr/bin/env python3
"""
Pattern 3: Structured Output Enforcement

Enforces predictable JSON output formats for all agent operations.
"""

import json
from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional, List
from datetime import datetime


@dataclass
class TaskOutput:
    """
    Standard structure for all task outputs
    """
    task_id: str
    status: str  # "success", "failed", "pending"
    timestamp: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def to_json(self) -> str:
        """
        Convert to JSON without preamble or markdown formatting
        """
        return json.dumps(asdict(self), indent=2)
    
    def validate(self) -> bool:
        """
        Validate output structure
        """
        required_fields = ['task_id', 'status', 'timestamp']
        return all(getattr(self, field) is not None for field in required_fields)


@dataclass
class ToolCallOutput:
    """
    Standard structure for tool call responses
    """
    tool_name: str
    call_id: str
    success: bool
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    execution_time_ms: Optional[float] = None
    
    def to_json(self) -> str:
        return json.dumps(asdict(self))
    
    def validate(self) -> bool:
        required_fields = ['tool_name', 'call_id', 'success']
        return all(getattr(self, field) is not None for field in required_fields)


@dataclass
class AgentStateSnapshot:
    """
    Standard structure for agent state persistence
    """
    agent_id: str
    session_id: str
    state: Dict[str, Any]
    context_window_size: int
    active_tools: List[str]
    memory_usage_mb: float
    timestamp: str
    
    def to_json(self) -> str:
        return json.dumps(asdict(self))
    
    def validate(self) -> bool:
        required_fields = ['agent_id', 'session_id', 'state', 'timestamp']
        return all(getattr(self, field) is not None for field in required_fields)


class OutputEnforcer:
    """
    Enforces structured output across all agent operations
    """
    
    SCHEMA_REGISTRY = {
        'task_output': TaskOutput,
        'tool_call': ToolCallOutput,
        'state_snapshot': AgentStateSnapshot,
    }
    
    @staticmethod
    def validate_schema(output_type: str, data: Dict[str, Any]) -> bool:
        """
        Validate data against registered schema
        """
        if output_type not in OutputEnforcer.SCHEMA_REGISTRY:
            raise ValueError(f"Unknown output type: {output_type}")
        
        schema_class = OutputEnforcer.SCHEMA_REGISTRY[output_type]
        try:
            instance = schema_class(**data)
            return instance.validate()
        except Exception as e:
            print(f"Schema validation failed: {e}")
            return False
    
    @staticmethod
    def enforce_json_output(func):
        """
        Decorator to enforce JSON output format
        """
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            
            # Ensure result is JSON-serializable
            try:
                json.dumps(result)
            except TypeError as e:
                raise TypeError(f"Function must return JSON-serializable output: {e}")
            
            return result
        
        return wrapper


if __name__ == "__main__":
    # Example usage
    output = TaskOutput(
        task_id="task_001",
        status="success",
        timestamp=datetime.now().isoformat(),
        result={"data": "example"},
        metadata={"version": "1.0.0"}
    )
    
    if output.validate():
        print("Output is valid")
        print(output.to_json())
    else:
        print("Output validation failed")
