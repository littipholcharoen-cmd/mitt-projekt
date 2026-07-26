# AEX-Agent: Advanced Multi-Platform AI Agent

## Overview
AEX-Agent är en avancerad AI-agent som kan köras på flera plattformar: iOS, Android, Linux och Windows. Agenten är designad enligt de 10 agentmönstren för robust och långsiktig operation.

## Projektstruktur

```
mitt-projekt/
├── agent/                    # Core agent logic
│   ├── core/                 # Base agent implementation
│   ├── patterns/             # The 10 agent patterns
│   ├── tools/                # Tool definitions
│   └── config/               # Configuration files
├── platforms/                # Platform-specific code
│   ├── web/                  # Web (Node.js/Python)
│   ├── ios/                  # iOS implementation
│   ├── android/              # Android implementation
│   ├── linux/                # Linux implementation
│   └── windows/              # Windows implementation
├── api/                      # REST API layer
├── tests/                    # Test suite
├── docs/                     # Documentation
└── examples/                 # Example implementations
```

## Quick Start

1. **Setup Development Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Initialize Agent**
   ```bash
   python agent/core/main.py
   ```

3. **Run Tests**
   ```bash
   pytest tests/
   ```

## Features

✅ **Pattern 1**: Role + Constraints - Clear boundaries
✅ **Pattern 2**: Chain of Verification - Self-checking
✅ **Pattern 3**: Structured Output - JSON enforcement
✅ **Pattern 4**: Tool Selection Heuristics - Smart tool usage
✅ **Pattern 5**: Error Recovery - Autonomous error handling
✅ **Pattern 6**: Context Window Management - Memory optimization
✅ **Pattern 7**: Guard Rails - Safety boundaries
✅ **Pattern 8**: Progressive Disclosure - Phase-based execution
✅ **Pattern 9**: Memory Integration - Persistent state
✅ **Pattern 10**: Self-Evaluation Loop - Quality assessment

## Platform Support

| Platform | Status | Implementation |
|----------|--------|----------------|
| **Web** | ✅ Ready | Node.js / Python Flask |
| **iOS** | ✅ Ready | Swift + Native integration |
| **Android** | ✅ Ready | Kotlin + Native integration |
| **Linux** | ✅ Ready | Python + systemd |
| **Windows** | ✅ Ready | Python + Windows Service |

## License
MIT License
