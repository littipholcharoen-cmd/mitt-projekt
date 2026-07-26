#!/usr/bin/env python3
"""
Web Platform: Flask-based REST API for AEX-Agent

Supports both Node.js and Python environments for cross-platform web deployment.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebAgentAPI:
    """
    REST API interface for AEX-Agent
    """
    
    def __init__(self):
        self.agent_status = "initialized"
        self.active_tasks = {}
    
    @staticmethod
    def create_response(success: bool, data: dict = None, error: str = None):
        """
        Standard response format
        """
        return {
            'success': success,
            'timestamp': datetime.now().isoformat(),
            'data': data or {},
            'error': error
        }


# Initialize API
api = WebAgentAPI()


@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    return jsonify(api.create_response(
        success=True,
        data={'status': 'online', 'version': '1.0.0'}
    ))


@app.route('/api/agent/status', methods=['GET'])
def agent_status():
    """
    Get agent status
    """
    return jsonify(api.create_response(
        success=True,
        data={
            'agent_status': api.agent_status,
            'active_tasks': len(api.active_tasks)
        }
    ))


@app.route('/api/tasks', methods=['POST'])
def create_task():
    """
    Create a new task
    """
    data = request.get_json()
    
    if not data or 'task_type' not in data:
        return jsonify(api.create_response(
            success=False,
            error='Missing required field: task_type'
        )), 400
    
    task_id = f"task_{len(api.active_tasks) + 1}"
    api.active_tasks[task_id] = {
        'type': data['task_type'],
        'status': 'pending',
        'created_at': datetime.now().isoformat()
    }
    
    logger.info(f"Created task: {task_id}")
    
    return jsonify(api.create_response(
        success=True,
        data={'task_id': task_id}
    )), 201


@app.route('/api/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    """
    Get task details
    """
    if task_id not in api.active_tasks:
        return jsonify(api.create_response(
            success=False,
            error='Task not found'
        )), 404
    
    return jsonify(api.create_response(
        success=True,
        data=api.active_tasks[task_id]
    ))


@app.route('/api/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    """
    Cancel/delete a task
    """
    if task_id not in api.active_tasks:
        return jsonify(api.create_response(
            success=False,
            error='Task not found'
        )), 404
    
    del api.active_tasks[task_id]
    logger.info(f"Deleted task: {task_id}")
    
    return jsonify(api.create_response(
        success=True,
        data={'deleted': task_id}
    ))


@app.errorhandler(404)
def not_found(error):
    return jsonify(api.create_response(
        success=False,
        error='Endpoint not found'
    )), 404


@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal error: {error}")
    return jsonify(api.create_response(
        success=False,
        error='Internal server error'
    )), 500


if __name__ == '__main__':
    print("Starting AEX-Agent Web API...")
    print("Available endpoints:")
    print("  GET  /health                - Health check")
    print("  GET  /api/agent/status      - Agent status")
    print("  POST /api/tasks             - Create task")
    print("  GET  /api/tasks/<task_id>   - Get task")
    print("  DELETE /api/tasks/<task_id> - Delete task")
    print("\nServer running on http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
