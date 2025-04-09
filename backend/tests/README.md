# API Tests

This directory contains API tests written using Tavern for the School News Feed API.

## Prerequisites

1. Python 3.7+
2. Tavern package installed:
   ```bash
   pip install tavern
   ```

## Test Structure

- `test_auth.tavern.yaml`: Tests for authentication endpoints (login, register, refresh token)
- `test_posts.tavern.yaml`: Tests for posts and wall newspapers endpoints
- `config.yaml`: Configuration file with test server settings and global variables

## Running Tests

1. Make sure your backend server is running on port 8081 (configured in app.py)
2. Run all tests:
   ```bash
   tavern-ci tests/*.tavern.yaml
   ```
3. Run specific test file:
   ```bash
   tavern-ci tests/test_auth.tavern.yaml
   ```

## Test Configuration

The `config.yaml` file contains:
- Test server URL (http://localhost:8081)
- Global test variables (test user and admin credentials)
- Request timeout settings
- SSL verification settings

## Test Cases

### Authentication Tests
- Register new client
- Register new admin
- Login as client
- Login as admin
- Refresh token
- Invalid login attempts
- Duplicate registration attempts

### Posts Tests
- Get posts by category
- Get detailed post
- Create wall newspaper (authorized and unauthorized)
- Get non-existent post

## Notes

- Tests are designed to run in sequence, with later tests depending on the results of earlier ones
- Authentication tokens are saved and reused between tests
- The test server URL is configured to match the backend server port (8081)
- Test credentials are defined in config.yaml and reused across tests 