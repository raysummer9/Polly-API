import requests
import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def register_user(username: str, password: str, base_url: str = "http://localhost:8000") -> Optional[Dict[str, Any]]:
    """
    Register a new user via the /register endpoint.
    
    Args:
        username (str): The username for the new user
        password (str): The password for the new user
        base_url (str): The base URL of the API (default: http://localhost:8000)
    
    Returns:
        Optional[Dict[str, Any]]: The response data if successful, None if failed
        
    Raises:
        requests.RequestException: If there's an error with the HTTP request
    """
    url = f"{base_url}/register"
    
    # Prepare the request data according to the UserCreate schema
    data = {
        "username": username,
        "password": password
    }
    
    # Set headers for JSON content
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        # Make the POST request
        response = requests.post(url, json=data, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Return the user data (UserOut schema)
            user_data = response.json()
            logger.info(f"User '{username}' registered successfully with ID: {user_data.get('id')}")
            return user_data
        elif response.status_code == 400:
            # Username already registered
            logger.warning(f"Registration failed: Username '{username}' is already registered")
            return None
        else:
            # Other error
            logger.error(f"Registration failed with status code {response.status_code}: {response.text}")
            return None
            
    except requests.RequestException as e:
        logger.error(f"Registration request failed: {e}")
        raise


def register_user_with_error_handling(username: str, password: str, base_url: str = "http://localhost:8000") -> Dict[str, Any]:
    """
    Register a new user with comprehensive error handling.
    
    Args:
        username (str): The username for the new user
        password (str): The password for the new user
        base_url (str): The base URL of the API (default: http://localhost:8000)
    
    Returns:
        Dict[str, Any]: Dictionary containing success status and response data or error message
    """
    url = f"{base_url}/register"
    
    data = {
        "username": username,
        "password": password
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            return {
                "success": True,
                "data": response.json(),
                "message": "User registered successfully"
            }
        elif response.status_code == 400:
            return {
                "success": False,
                "data": None,
                "message": f"Username '{username}' is already registered",
                "status_code": 400
            }
        else:
            return {
                "success": False,
                "data": None,
                "message": f"Unexpected error: {response.status_code}",
                "status_code": response.status_code,
                "response_text": response.text
            }
            
    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "data": None,
            "message": "Connection error: Could not connect to the API server",
            "error_type": "ConnectionError"
        }
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "data": None,
            "message": "Request timeout: The server took too long to respond",
            "error_type": "Timeout"
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "data": None,
            "message": f"Request failed: {str(e)}",
            "error_type": "RequestException"
        }


def fetch_polls(skip: int = 0, limit: int = 10, base_url: str = "http://localhost:8000") -> Optional[List[Dict[str, Any]]]:
    """
    Fetch paginated poll data from the /polls endpoint.
    
    Args:
        skip (int): Number of items to skip (default: 0)
        limit (int): Maximum number of items to return (default: 10)
        base_url (str): The base URL of the API (default: http://localhost:8000)
    
    Returns:
        Optional[List[Dict[str, Any]]]: List of poll objects if successful, None if failed
        
    Raises:
        requests.RequestException: If there's an error with the HTTP request
    """
    url = f"{base_url}/polls"
    
    # Prepare query parameters
    params = {
        "skip": skip,
        "limit": limit
    }
    
    try:
        # Make the GET request
        response = requests.get(url, params=params)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Return the list of polls
            return response.json()
        else:
            # Handle error response
            print(f"Error: Unexpected status code {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        raise


def fetch_polls_with_error_handling(skip: int = 0, limit: int = 10, base_url: str = "http://localhost:8000") -> Dict[str, Any]:
    """
    Fetch paginated poll data with comprehensive error handling.
    
    Args:
        skip (int): Number of items to skip (default: 0)
        limit (int): Maximum number of items to return (default: 10)
        base_url (str): The base URL of the API (default: http://localhost:8000)
    
    Returns:
        Dict[str, Any]: Dictionary containing success status and response data or error message
    """
    url = f"{base_url}/polls"
    
    params = {
        "skip": skip,
        "limit": limit
    }
    
    try:
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            polls_data = response.json()
            return {
                "success": True,
                "data": polls_data,
                "message": f"Successfully fetched {len(polls_data)} polls",
                "pagination": {
                    "skip": skip,
                    "limit": limit,
                    "returned_count": len(polls_data)
                }
            }
        else:
            return {
                "success": False,
                "data": None,
                "message": f"Unexpected error: {response.status_code}",
                "status_code": response.status_code,
                "response_text": response.text
            }
            
    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "data": None,
            "message": "Connection error: Could not connect to the API server",
            "error_type": "ConnectionError"
        }
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "data": None,
            "message": "Request timeout: The server took too long to respond",
            "error_type": "Timeout"
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "data": None,
            "message": f"Request failed: {str(e)}",
            "error_type": "RequestException"
        }


def fetch_all_polls_paginated(base_url: str = "http://localhost:8000", page_size: int = 10) -> List[Dict[str, Any]]:
    """
    Fetch all polls by automatically paginating through all pages.
    
    Args:
        base_url (str): The base URL of the API (default: http://localhost:8000)
        page_size (int): Number of polls to fetch per request (default: 10)
    
    Returns:
        List[Dict[str, Any]]: Complete list of all polls
    """
    all_polls = []
    skip = 0
    
    while True:
        result = fetch_polls_with_error_handling(skip=skip, limit=page_size, base_url=base_url)
        
        if not result["success"]:
            print(f"Error fetching polls at skip={skip}: {result['message']}")
            break
            
        polls_batch = result["data"]
        if not polls_batch:  # Empty list means we've reached the end
            break
            
        all_polls.extend(polls_batch)
        
        # If we got fewer polls than requested, we've reached the end
        if len(polls_batch) < page_size:
            break
            
        skip += page_size
    
    return all_polls


def format_poll_display(poll: Dict[str, Any]) -> str:
    """
    Format a poll object for nice display.
    
    Args:
        poll (Dict[str, Any]): Poll object from the API
    
    Returns:
        str: Formatted string representation of the poll
    """
    poll_id = poll.get("id", "N/A")
    question = poll.get("question", "No question")
    created_at = poll.get("created_at", "N/A")
    owner_id = poll.get("owner_id", "N/A")
    options = poll.get("options", [])
    
    # Parse and format the created_at timestamp
    try:
        if created_at != "N/A":
            dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            formatted_date = dt.strftime("%Y-%m-%d %H:%M:%S")
        else:
            formatted_date = "N/A"
    except:
        formatted_date = created_at
    
    formatted_poll = f"""
Poll ID: {poll_id}
Question: {question}
Created: {formatted_date}
Owner ID: {owner_id}
Options:"""
    
    for option in options:
        option_id = option.get("id", "N/A")
        option_text = option.get("text", "No text")
        formatted_poll += f"\n  - [{option_id}] {option_text}"
    
    return formatted_poll


def login_user(username: str, password: str, base_url: str = "http://localhost:8000") -> Optional[Dict[str, Any]]:
    """
    Login a user and get JWT token via the /login endpoint.
    
    Args:
        username (str): The username for login
        password (str): The password for login
        base_url (str): The base URL of the API (default: http://localhost:8000)
    
    Returns:
        Optional[Dict[str, Any]]: Token data if successful, None if failed
        
    Raises:
        requests.RequestException: If there's an error with the HTTP request
    """
    url = f"{base_url}/login"
    
    # Prepare form data according to the OpenAPI spec (application/x-www-form-urlencoded)
    data = {
        "username": username,
        "password": password
    }
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    try:
        # Make the POST request
        response = requests.post(url, data=data, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Return the token data (Token schema)
            token_data = response.json()
            logger.info(f"User '{username}' logged in successfully")
            return token_data
        elif response.status_code == 400:
            # Incorrect username or password
            logger.warning(f"Login failed: Incorrect username or password for '{username}'")
            return None
        else:
            # Other error
            logger.error(f"Login failed with status code {response.status_code}: {response.text}")
            return None
            
    except requests.RequestException as e:
        logger.error(f"Login request failed: {e}")
        raise


def create_poll(question: str, options: List[str], access_token: str, base_url: str = "http://localhost:8000") -> Optional[Dict[str, Any]]:
    """
    Create a new poll via the /polls endpoint (requires authentication).
    
    Args:
        question (str): The poll question
        options (List[str]): List of poll options
        access_token (str): JWT access token for authentication
        base_url (str): The base URL of the API (default: http://localhost:8000)
    
    Returns:
        Optional[Dict[str, Any]]: Poll data if successful, None if failed
        
    Raises:
        requests.RequestException: If there's an error with the HTTP request
    """
    url = f"{base_url}/polls"
    
    # Prepare the request data according to the PollCreate schema
    data = {
        "question": question,
        "options": options
    }
    
    # Set headers for JSON content and Bearer authentication
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        # Make the POST request
        response = requests.post(url, json=data, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Return the poll data (PollOut schema)
            poll_data = response.json()
            logger.info(f"Poll created successfully with ID: {poll_data.get('id')}")
            return poll_data
        elif response.status_code == 401:
            # Unauthorized
            logger.warning("Poll creation failed: Unauthorized - invalid or expired token")
            return None
        else:
            # Other error
            logger.error(f"Poll creation failed with status code {response.status_code}: {response.text}")
            return None
            
    except requests.RequestException as e:
        logger.error(f"Poll creation request failed: {e}")
        raise


def vote_on_poll(poll_id: int, option_id: int, access_token: str, base_url: str = "http://localhost:8000") -> Optional[Dict[str, Any]]:
    """
    Vote on a poll via the /polls/{poll_id}/vote endpoint (requires authentication).
    
    Args:
        poll_id (int): The ID of the poll to vote on
        option_id (int): The ID of the option to vote for
        access_token (str): JWT access token for authentication
        base_url (str): The base URL of the API (default: http://localhost:8000)
    
    Returns:
        Optional[Dict[str, Any]]: Vote data if successful, None if failed
        
    Raises:
        requests.RequestException: If there's an error with the HTTP request
    """
    url = f"{base_url}/polls/{poll_id}/vote"
    
    # Prepare the request data according to the VoteCreate schema
    data = {
        "option_id": option_id
    }
    
    # Set headers for JSON content and Bearer authentication
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        # Make the POST request
        response = requests.post(url, json=data, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Return the vote data (VoteOut schema)
            vote_data = response.json()
            logger.info(f"Vote recorded successfully with ID: {vote_data.get('id')}")
            return vote_data
        elif response.status_code == 401:
            # Unauthorized
            logger.warning("Vote failed: Unauthorized - invalid or expired token")
            return None
        elif response.status_code == 404:
            # Poll or option not found
            logger.warning(f"Vote failed: Poll {poll_id} or option {option_id} not found")
            return None
        else:
            # Other error
            logger.error(f"Vote failed with status code {response.status_code}: {response.text}")
            return None
            
    except requests.RequestException as e:
        logger.error(f"Vote request failed: {e}")
        raise


def delete_poll(poll_id: int, access_token: str, base_url: str = "http://localhost:8000") -> bool:
    """
    Delete a poll via the /polls/{poll_id} endpoint (requires authentication).
    
    Args:
        poll_id (int): The ID of the poll to delete
        access_token (str): JWT access token for authentication
        base_url (str): The base URL of the API (default: http://localhost:8000)
    
    Returns:
        bool: True if successful, False if failed
        
    Raises:
        requests.RequestException: If there's an error with the HTTP request
    """
    url = f"{base_url}/polls/{poll_id}"
    
    # Set headers for Bearer authentication
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        # Make the DELETE request
        response = requests.delete(url, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 204:
            # Poll deleted successfully (204 No Content)
            logger.info(f"Poll {poll_id} deleted successfully")
            return True
        elif response.status_code == 401:
            # Unauthorized
            logger.warning("Poll deletion failed: Unauthorized - invalid or expired token")
            return False
        elif response.status_code == 404:
            # Poll not found or not authorized
            logger.warning(f"Poll deletion failed: Poll {poll_id} not found or not authorized")
            return False
        else:
            # Other error
            logger.error(f"Poll deletion failed with status code {response.status_code}: {response.text}")
            return False
            
    except requests.RequestException as e:
        logger.error(f"Poll deletion request failed: {e}")
        raise


def get_poll_by_id(poll_id: int, base_url: str = "http://localhost:8000") -> Optional[Dict[str, Any]]:
    """
    Get a specific poll by ID via the /polls/{poll_id} endpoint.
    
    Args:
        poll_id (int): The ID of the poll to fetch
        base_url (str): The base URL of the API (default: http://localhost:8000)
    
    Returns:
        Optional[Dict[str, Any]]: Poll data if successful, None if failed
        
    Raises:
        requests.RequestException: If there's an error with the HTTP request
    """
    url = f"{base_url}/polls/{poll_id}"
    
    try:
        # Make the GET request
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Return the poll data (PollOut schema)
            poll_data = response.json()
            logger.info(f"Poll {poll_id} fetched successfully")
            return poll_data
        elif response.status_code == 404:
            # Poll not found
            logger.warning(f"Poll {poll_id} not found")
            return None
        else:
            # Other error
            logger.error(f"Failed to fetch poll {poll_id} with status code {response.status_code}: {response.text}")
            return None
            
    except requests.RequestException as e:
        logger.error(f"Poll fetch request failed: {e}")
        raise


def get_poll_results(poll_id: int, base_url: str = "http://localhost:8000") -> Optional[Dict[str, Any]]:
    """
    Get poll results via the /polls/{poll_id}/results endpoint.
    
    Args:
        poll_id (int): The ID of the poll to get results for
        base_url (str): The base URL of the API (default: http://localhost:8000)
    
    Returns:
        Optional[Dict[str, Any]]: Poll results if successful, None if failed
        
    Raises:
        requests.RequestException: If there's an error with the HTTP request
    """
    url = f"{base_url}/polls/{poll_id}/results"
    
    try:
        # Make the GET request
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Return the poll results (PollResults schema)
            results_data = response.json()
            logger.info(f"Poll {poll_id} results fetched successfully")
            return results_data
        elif response.status_code == 404:
            # Poll not found
            logger.warning(f"Poll {poll_id} not found")
            return None
        else:
            # Other error
            logger.error(f"Failed to fetch poll {poll_id} results with status code {response.status_code}: {response.text}")
            return None
            
    except requests.RequestException as e:
        logger.error(f"Poll results request failed: {e}")
        raise


# Example usage
if __name__ == "__main__":
    # Example 1: Simple registration
    print("Example 1: Simple registration")
    result = register_user("testuser", "testpassword123")
    if result:
        print(f"User registered: {result}")
    else:
        print("Registration failed")
    
    print("\n" + "="*50 + "\n")
    
    # Example 2: Registration with error handling
    print("Example 2: Registration with error handling")
    result = register_user_with_error_handling("testuser2", "testpassword123")
    print(f"Result: {json.dumps(result, indent=2)}")
    
    print("\n" + "="*50 + "\n")
    
    # Example 3: Try to register the same user again (should fail)
    print("Example 3: Try to register existing user")
    result = register_user_with_error_handling("testuser2", "testpassword123")
    print(f"Result: {json.dumps(result, indent=2)}")
    
    print("\n" + "="*50 + "\n")
    
    # Example 4: Fetch first 5 polls
    print("Example 4: Fetch first 5 polls")
    polls = fetch_polls(skip=0, limit=5)
    if polls:
        print(f"Fetched {len(polls)} polls:")
        for i, poll in enumerate(polls, 1):
            print(f"\n--- Poll {i} ---")
            print(format_poll_display(poll))
    else:
        print("Failed to fetch polls")
    
    print("\n" + "="*50 + "\n")
    
    # Example 5: Fetch polls with error handling
    print("Example 5: Fetch polls with error handling")
    result = fetch_polls_with_error_handling(skip=0, limit=3)
    print(f"Result: {json.dumps(result, indent=2)}")
    
    print("\n" + "="*50 + "\n")
    
    # Example 6: Fetch all polls (paginated)
    print("Example 6: Fetch all polls (paginated)")
    all_polls = fetch_all_polls_paginated(page_size=5)
    print(f"Total polls fetched: {len(all_polls)}")
    if all_polls:
        print("\nFirst poll:")
        print(format_poll_display(all_polls[0]))
    
    print("\n" + "="*50 + "\n")
    
    # Example 7: Login user
    print("Example 7: Login user")
    token_result = login_user("testuser2", "testpassword123")
    if token_result:
        print(f"Login successful: {token_result}")
        access_token = token_result.get("access_token")
        
        # Example 8: Create a poll (requires authentication)
        print("\nExample 8: Create a poll")
        poll_result = create_poll(
            question="What's your favorite programming language?",
            options=["Python", "JavaScript", "Java", "Go"],
            access_token=access_token
        )
        if poll_result:
            print(f"Poll created: {poll_result}")
            poll_id = poll_result.get("id")
            
            # Example 9: Vote on the poll
            print("\nExample 9: Vote on the poll")
            if poll_result.get("options"):
                first_option_id = poll_result["options"][0]["id"]
                vote_result = vote_on_poll(poll_id, first_option_id, access_token)
                if vote_result:
                    print(f"Vote recorded: {vote_result}")
            
            # Example 10: Get poll results
            print("\nExample 10: Get poll results")
            results = get_poll_results(poll_id)
            if results:
                print(f"Poll results: {json.dumps(results, indent=2)}")
            
            # Example 11: Delete the poll
            print("\nExample 11: Delete the poll")
            delete_success = delete_poll(poll_id, access_token)
            print(f"Poll deletion: {'Success' if delete_success else 'Failed'}")
    else:
        print("Login failed - cannot test authenticated endpoints")
