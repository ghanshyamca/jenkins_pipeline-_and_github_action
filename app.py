"""
Simple Flask Web Application
This application provides basic endpoints for demonstration of CI/CD pipelines.
"""

from flask import Flask, jsonify, render_template_string
import os

app = Flask(__name__)

# HTML template for home page
HOME_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Flask CI/CD Demo</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
        }
        .endpoint {
            background-color: #f0f0f0;
            padding: 10px;
            margin: 10px 0;
            border-radius: 5px;
        }
        code {
            background-color: #e0e0e0;
            padding: 2px 6px;
            border-radius: 3px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Flask CI/CD Demo Application</h1>
        <p>Welcome to the Flask CI/CD demonstration application!</p>

        <h2>Available Endpoints:</h2>
        <div class="endpoint">
            <strong>GET /</strong> - This home page
        </div>
        <div class="endpoint">
            <strong>GET /api/health</strong> - Health check endpoint
        </div>
        <div class="endpoint">
            <strong>GET /api/info</strong> - Application information
        </div>
        <div class="endpoint">
            <strong>GET /api/add/&lt;num1&gt;/&lt;num2&gt;</strong> - Add two numbers
        </div>
        <h2>Environment:</h2>
        <p>Current environment: <strong>{{ environment }}</strong></p>
        <p>Version: <strong>1.0.0</strong></p>
    </div>
</body>
</html>
"""


@app.route('/')
def home():
    """Home page with application information"""
    environment = os.getenv('ENVIRONMENT', 'development')
    return render_template_string(HOME_TEMPLATE, environment=environment)


@app.route('/api/health')
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'message': 'Application is running successfully'
    }), 200


@app.route('/api/info')
def info():
    """Application information endpoint"""
    return jsonify({
        'name': 'Flask CI/CD Demo',
        'version': '1.0.0',
        'environment': os.getenv('ENVIRONMENT', 'development'),
        'description': 'A simple Flask application demonstrating CI/CD with Jenkins and GitHub Actions'
    }), 200


@app.route('/api/add/<num1>/<num2>')
def add_numbers(num1, num2):
    """Add two numbers and return the result"""
    try:
        num1 = int(num1)
        num2 = int(num2)
        result = num1 + num2
        return jsonify({
            'num1': num1,
            'num2': num2,
            'result': result,
            'operation': 'addition'
        }), 200
    except ValueError:
        return jsonify({
            'error': 'Invalid input',
            'message': 'Both parameters must be valid integers'
        }), 400


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Not Found',
        'message': 'The requested endpoint does not exist'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'An unexpected error occurred'
    }), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
