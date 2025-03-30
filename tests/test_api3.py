import api3
from unittest.mock import patch, Mock

@patch('api3.requests.get')
def test_github_user(mock_get):
    mock_response = Mock()  
    mock_response.status_code = 200  
    mock_response.json.return_value = {  
        "User": "octocat",  
        "Name": "Octocat",  
        "Public Repos": 222 
    }  
    mock_get.return_value = mock_response

    # Call the function  
    user_data = api3.get_github_user("octocat")  

   
    # Check if the data is not None
    assert user_data is not None, "Failed to fetch user data"
    
    # Check if the data contains the expected keys
    assert 'User' in user_data, "Login not found in the response"
    assert 'Name' in user_data, "Name not found in the response"
    assert 'Public Repos' in user_data, "Public repos not found in the response"
    assert user_data['User'] == "octocat", "User login does not match"
    assert user_data['Name'] == "Octocat", "User name does not match"
    assert user_data['Public Repos'] == 222, "Public repos count does not match"

@patch('api3.requests.get')
def test_get_github_user_failure(mock_get):  
    """  
    Test that get_github_user returns None  
    when the API call fails (HTTP 404).  
    """  
    # Create a mock response with status_code=404  
    mock_response = Mock()  
    mock_response.status_code = 404  
    # Make mock_get return our mock_response  
    mock_get.return_value = mock_response  

    # Call the function  
    user_data = api3.get_github_user("this_user_does_not_exist")  

    # Assertions  
    assert user_data is None, "Expected None when user not found"