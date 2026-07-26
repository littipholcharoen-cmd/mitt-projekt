# AEX-Agent Setup Guide

## Prerequisites

- Python 3.9+
- Node.js 18+ (for web platform)
- iOS Development Environment (Xcode 14+)
- Android Studio 2023+
- Git

## Installation Steps

### 1. Clone Repository

```bash
git clone https://github.com/littipholcharoen-cmd/mitt-projekt.git
cd mitt-projekt
```

### 2. Setup Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Initialize Agent

```bash
# Create required directories
mkdir -p logs data cache

# Run main agent
python agent/core/main.py
```

### 4. Run Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=agent --cov-report=html
```

### 5. Start Web API

```bash
# Start Flask server
python platforms/web/flask_app.py

# API will be available at http://localhost:5000
```

## Platform-Specific Setup

### iOS

1. Open `platforms/ios/AEXAgent.xcodeproj` in Xcode
2. Select target device
3. Build and run (Cmd+R)

### Android

1. Open `platforms/android/` in Android Studio
2. Configure SDK and build tools
3. Run on emulator or device

### Linux

```bash
# Install systemd service
sudo cp platforms/linux/aex-agent.service /etc/systemd/system/
sudo systemctl enable aex-agent
sudo systemctl start aex-agent
```

### Windows

```bash
# Install as Windows Service
python platforms/windows/install_service.py
sc start AEXAgent
```

## Verification

### Check Agent Status

```bash
curl http://localhost:5000/api/agent/status
```

### Expected Response

```json
{
  "success": true,
  "timestamp": "2026-07-26T12:00:00",
  "data": {
    "agent_status": "initialized",
    "active_tasks": 0
  }
}
```

## Debugging

### View Logs

```bash
# Real-time logs
tail -f logs/agent.log

# Error logs
tail -f logs/error.log
```

### Enable Debug Mode

```bash
# Set environment variable
export DEBUG=1
python agent/core/main.py
```

## Troubleshooting

### Issue: Module not found

```bash
# Solution: Update Python path
export PYTHONPATH=$PYTHONPATH:$(pwd)
```

### Issue: Port already in use

```bash
# Solution: Use different port
python platforms/web/flask_app.py --port 5001
```

### Issue: Permission denied

```bash
# Solution: Fix file permissions
chmod +x agent/core/main.py
```

## Next Steps

1. Read [Configuration Guide](./CONFIGURATION.md)
2. Review [The 10 Patterns](./PATTERNS.md)
3. Check [Examples](../examples/)
