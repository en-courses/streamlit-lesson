import api3
from unittest.mock import  Mock
import pytest

@pytest.fixture
def github_user_response():
    """
    Returns a dictionary that simulates a typical response from
    the GitHub API for a user.
    """
    return {
    "login": "octocat",
    "Name": "Octocat",
    "url": "https://api.github.com/users/octocat"
    }

@pytest.fixture
def mock_requests_get(mocker):
    """
    A fixture that patches requests.get via pytest-mock (mocker).
    Returns the mock object so you can configure it within tests.
    """
    return mocker.patch("api3.requests.get")


def test_get_github_user_successful(github_user_response, 
                                    mock_requests_get):
    """
    Test that get_github_user returns correct JSON data
    when the API call is successful (HTTP 200).
    """
    # Create a mock response with status_code=200
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = github_user_response
    mock_requests_get.return_value = mock_response


    # Call the function  
    result = api3.get_github_user("octocat")  

    # Assertions  
    assert result is not None  
    assert result["login"] == "octocat"  
    assert result["Name"] == "Octocat"

def test_get_github_user_failure(mock_requests_get):
    """
    Test that get_github_user returns None
    when the API call fails (e.g., HTTP 404).
    """
    # Create a mock response with status_code=404
    mock_response = Mock()
    mock_response.status_code = 404
    mock_requests_get.return_value = mock_response


    # Call the function  
    result = api3.get_github_user("this_user_does_not_exist")  

    # Assertions  
    assert result is None  