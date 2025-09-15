# Polly-API: FastAPI Poll Application

A comprehensive poll application built with FastAPI, SQLite, and JWT authentication. Users can register, log in, create, retrieve, vote on, and delete polls. The project includes both a robust API server and a complete Python client library for easy integration.

## Features

### API Server
- User registration and login (JWT authentication)
- Create, retrieve, and delete polls
- Add options to polls (minimum of two options required)
- Vote on polls (authenticated users only)
- View poll results with vote counts
- SQLite database with SQLAlchemy ORM
- Modular code structure for maintainability
- OpenAPI 3.0 specification with interactive docs

### Python Client Library
- **Complete API Client**: Full-featured Python client with all API endpoints
- **Authentication Support**: JWT Bearer token authentication for protected endpoints
- **Input Validation**: Comprehensive validation of request parameters and response schemas
- **Error Handling**: Robust error handling with structured logging and meaningful error messages
- **Schema Compliance**: Full compliance with OpenAPI specification schemas
- **Client-Side Functions**: Enhanced client-side functions for voting and results retrieval
- **Pagination Support**: Built-in pagination for fetching polls
- **Type Safety**: Full type hints and type checking throughout

## Project Structure

```
Polly-API/
├── api/                    # API server modules
│   ├── __init__.py
│   ├── auth.py            # JWT authentication logic
│   ├── database.py        # Database configuration
│   ├── models.py          # SQLAlchemy models
│   ├── routes.py          # API route handlers
│   └── schemas.py         # Pydantic schemas
├── tests/                 # Test files
│   └── test_routes.py
├── main.py                # FastAPI application entry point
├── register_user.py       # Complete Python API client library
├── openapi.yaml          # OpenAPI 3.0 specification
├── polls.db              # SQLite database
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Setup Instructions

1. **Clone the repository**

```bash
git clone <your-repo-url>
cd Polly-API
```

2. **Set up a Python virtual environment (recommended)**

A virtual environment helps isolate your project dependencies.

- **On Unix/macOS:**

  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

- **On Windows (cmd):**

  ```cmd
  python -m venv venv
  venv\Scripts\activate
  ```

- **On Windows (PowerShell):**

  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```

To deactivate the virtual environment, simply run:

```bash
deactivate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set environment variables (optional)**

Create a `.env` file in the project root to override the default secret key:

```
SECRET_KEY=your_super_secret_key
```

5. **Run the application**

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## Python API Client Usage

The project includes a comprehensive Python client library (`register_user.py`) that provides easy-to-use functions for all API operations.

### Quick Start

```python
from register_user import register_user, login_user, create_poll, cast_vote, retrieve_poll_results

# Register a new user
user = register_user("myusername", "mypassword")
if user:
    print(f"User registered with ID: {user['id']}")

# Login to get access token
token = login_user("myusername", "mypassword")
if token:
    access_token = token["access_token"]
    
    # Create a poll
    poll = create_poll(
        question="What's your favorite programming language?",
        options=["Python", "JavaScript", "Java", "Go"],
        access_token=access_token
    )
    
    if poll:
        poll_id = poll["id"]
        
        # Vote on the poll
        vote = cast_vote(poll_id, poll["options"][0]["id"], access_token)
        if vote:
            print("Vote cast successfully!")
        
        # Get poll results
        results = retrieve_poll_results(poll_id)
        if results:
            print(f"Poll results: {results}")
```

### Available Client Functions

#### User Management
- `register_user(username, password, base_url)` - Register a new user
- `login_user(username, password, base_url)` - Login and get JWT token

#### Poll Management
- `fetch_polls(skip, limit, base_url)` - Get paginated polls
- `fetch_all_polls_paginated(base_url, page_size)` - Get all polls automatically
- `get_poll_by_id(poll_id, base_url)` - Get specific poll by ID
- `create_poll(question, options, access_token, base_url)` - Create new poll (authenticated)
- `delete_poll(poll_id, access_token, base_url)` - Delete poll (authenticated)

#### Voting System
- `cast_vote(poll_id, option_id, access_token, base_url)` - Cast a vote (authenticated)
- `cast_vote_with_validation(poll_id, option_id, access_token, base_url)` - Enhanced vote casting with validation
- `vote_on_poll(poll_id, option_id, access_token, base_url)` - Low-level vote function

#### Results and Analytics
- `retrieve_poll_results(poll_id, base_url)` - Get poll results
- `retrieve_poll_results_with_validation(poll_id, base_url)` - Enhanced results with validation
- `get_poll_results(poll_id, base_url)` - Low-level results function

#### Utility Functions
- `format_poll_display(poll)` - Format poll data for display
- `register_user_with_error_handling()` - Registration with comprehensive error handling
- `fetch_polls_with_error_handling()` - Poll fetching with error handling

### Client Features

#### Input Validation
All functions include comprehensive input validation:
- Required field validation
- Type checking (strings, integers, lists)
- Business logic validation (non-empty options, valid IDs)
- Schema compliance checking

#### Error Handling
- **Structured Logging**: Professional logging with timestamps and context
- **Error Categorization**: Different error types (ValidationError, NotFoundError, NetworkError)
- **Meaningful Messages**: Human-readable error descriptions
- **Graceful Degradation**: Functions return None or error dictionaries instead of crashing

#### Authentication
- **JWT Bearer Tokens**: Automatic token handling for protected endpoints
- **Token Validation**: Validates token presence and format
- **Secure Headers**: Proper Authorization header formatting

#### Response Validation
- **Schema Compliance**: All responses validated against OpenAPI schemas
- **Type Safety**: Full type hints and runtime type checking
- **Data Integrity**: Ensures response data matches expected structure

### Example: Complete Workflow

```python
from register_user import *

# 1. Register and login
user = register_user("alice", "password123")
token = login_user("alice", "password123")
access_token = token["access_token"]

# 2. Create a poll
poll = create_poll(
    question="Best programming language for beginners?",
    options=["Python", "JavaScript", "Java", "C++"],
    access_token=access_token
)

# 3. Get all polls with pagination
polls = fetch_polls(skip=0, limit=10)
print(f"Found {len(polls)} polls")

# 4. Vote on the poll
if poll and poll["options"]:
    vote = cast_vote_with_validation(
        poll["id"], 
        poll["options"][0]["id"], 
        access_token
    )
    if vote["success"]:
        print(f"Voted for: {vote['poll_info']['option_text']}")

# 5. Get results with enhanced validation
results = retrieve_poll_results_with_validation(poll["id"])
if results["success"]:
    summary = results["summary"]
    print(f"Total votes: {summary['total_votes']}")
    for result in results["data"]["results"]:
        print(f"{result['text']}: {result['vote_count']} votes")

# 6. Clean up - delete the poll
delete_success = delete_poll(poll["id"], access_token)
print(f"Poll deleted: {delete_success}")
```

## API Usage (Direct HTTP)

### 1. Register a new user

- **Endpoint:** `POST /register`
- **Body:**

```json
{
  "username": "yourusername",
  "password": "yourpassword"
}
```

### 2. Login

- **Endpoint:** `POST /login`
- **Body (form):**
  - `username`: yourusername
  - `password`: yourpassword
- **Response:**

```json
{
  "access_token": "...",
  "token_type": "bearer"
}
```

### 3. Get all polls

- **Endpoint:** `GET /polls`
- **Query params:** `skip` (default 0), `limit` (default 10)
- **Authentication:** Not required

### 4. Create a poll

- **Endpoint:** `POST /polls`
- **Headers:** `Authorization: Bearer <access_token>`
- **Body:**

```json
{
  "question": "Your poll question",
  "options": ["Option 1", "Option 2"]
}
```

### 5. Get a specific poll

- **Endpoint:** `GET /polls/{poll_id}`
- **Authentication:** Not required

### 6. Vote on a poll

- **Endpoint:** `POST /polls/{poll_id}/vote`
- **Headers:** `Authorization: Bearer <access_token>`
- **Body:**

```json
{
  "option_id": 1
}
```

### 7. Get poll results

- **Endpoint:** `GET /polls/{poll_id}/results`
- **Authentication:** Not required
- **Response:**

```json
{
  "poll_id": 1,
  "question": "Your poll question",
  "results": [
    {
      "option_id": 1,
      "text": "Option 1",
      "vote_count": 3
    },
    {
      "option_id": 2,
      "text": "Option 2",
      "vote_count": 1
    }
  ]
}
```

### 8. Delete a poll

- **Endpoint:** `DELETE /polls/{poll_id}`
- **Headers:** `Authorization: Bearer <access_token>`

## Technical Specifications

### OpenAPI Compliance
The API client is fully compliant with the OpenAPI 3.0 specification:

- **Request Schemas**: All request bodies match the defined schemas exactly
- **Response Schemas**: All responses are validated against the OpenAPI response schemas
- **Status Codes**: Proper handling of all documented HTTP status codes (200, 400, 401, 404, 422, 204)
- **Authentication**: Bearer token authentication implemented for all protected endpoints
- **Content Types**: Correct Content-Type headers for JSON and form-encoded requests

### Schema Validation
The client includes comprehensive schema validation functions:

- `_validate_user_out_schema()` - Validates UserOut responses
- `_validate_token_schema()` - Validates Token responses  
- `_validate_poll_out_schema()` - Validates PollOut responses
- `_validate_vote_out_schema()` - Validates VoteOut responses
- `_validate_poll_results_schema()` - Validates PollResults responses

### Error Handling
Robust error handling with multiple layers:

1. **Input Validation**: Validates all parameters before making requests
2. **HTTP Status Codes**: Handles all expected status codes with appropriate responses
3. **Schema Validation**: Validates response schemas to ensure data integrity
4. **Network Errors**: Handles connection errors, timeouts, and other network issues
5. **Structured Logging**: Professional logging with context and error categorization

### Security Features
- **JWT Authentication**: Secure Bearer token authentication
- **Input Sanitization**: Validates and sanitizes all input parameters
- **Schema Validation**: Prevents malformed data from being processed
- **Error Information**: Provides meaningful error messages without exposing sensitive data

## Testing

The project includes comprehensive test coverage:

```bash
# Run the test suite
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=api
```

### Test the API Client

```python
# Run the example usage in register_user.py
python register_user.py
```

This will execute all 13 example scenarios demonstrating:
- User registration and login
- Poll creation, voting, and deletion
- Error handling scenarios
- Authentication workflows
- Response structure handling

## Interactive API Docs

Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for the interactive Swagger UI documentation.

## Dependencies

### Server Dependencies
- FastAPI - Modern web framework for building APIs
- SQLAlchemy - SQL toolkit and ORM
- SQLite - Lightweight database
- JWT - JSON Web Token authentication
- Pydantic - Data validation using Python type annotations

### Client Dependencies
- requests - HTTP library for making API calls
- typing - Type hints for better code clarity
- logging - Structured logging for debugging and monitoring
- datetime - Date/time handling for timestamps

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License
