"""
Unit tests for the Flask application using pytest
"""

import pytest
import json
from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask application"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home_page(client):
    """Test the home page endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Flask CI/CD Demo Application' in response.data


def test_health_check(client):
    """Test the health check endpoint"""
    response = client.get('/api/health')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert 'message' in data


def test_info_endpoint(client):
    """Test the application info endpoint"""
    response = client.get('/api/info')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['name'] == 'Flask CI/CD Demo'
    assert data['version'] == '1.0.0'
    assert 'environment' in data
    assert 'description' in data


def test_add_numbers_positive(client):
    """Test adding two positive numbers"""
    response = client.get('/api/add/5/3')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['num1'] == 5
    assert data['num2'] == 3
    assert data['result'] == 8
    assert data['operation'] == 'addition'


def test_add_numbers_negative(client):
    """Test adding negative numbers"""
    response = client.get('/api/add/-5/3')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['num1'] == -5
    assert data['num2'] == 3
    assert data['result'] == -2


def test_add_numbers_zero(client):
    """Test adding with zero"""
    response = client.get('/api/add/0/0')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['result'] == 0


def test_add_numbers_large(client):
    """Test adding large numbers"""
    response = client.get('/api/add/1000/2000')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['result'] == 3000


def test_invalid_endpoint(client):
    """Test accessing an invalid endpoint"""
    response = client.get('/api/invalid')
    assert response.status_code == 404
    
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == 'Not Found'


def test_add_non_integer(client):
    """Test adding with non-integer values"""
    response = client.get('/api/add/abc/def')
    assert response.status_code == 404  # Route won't match


def test_health_check_returns_json(client):
    """Test that health check returns proper JSON content type"""
    response = client.get('/api/health')
    assert response.content_type == 'application/json'


def test_info_returns_json(client):
    """Test that info endpoint returns proper JSON content type"""
    response = client.get('/api/info')
    assert response.content_type == 'application/json'
