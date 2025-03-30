import api2
# Mock the requests.get method
from unittest.mock import patch, Mock
import requests

def test_api():
    # Test the fetch_airport_data function
    airport_data = api2.fetch_airport_data('KAVL')
    
    # Check if the data is not None
    assert airport_data is not None, "Failed to fetch airport data"
    
    # Check if the data contains the expected keys
    assert 'KAVL' in airport_data, "ICAO code not found in the response"
    
    # Check if the data contains expected fields
    airport_info = airport_data['KAVL'][0]
    assert 'facility_name' in airport_info, "Facility name not found in the response"
    assert 'city' in airport_info, "City not found in the response"

def test_mock_api():
    mock_response = {
        "KAVL": [
            {
                "facility_name": "Asheville Regional Airport",
                "city": "Asheville",
                "state": "NC",
                "country": "USA"
            }
        ]
    }
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response
        
        # Call the function to test
        airport_data = api2.fetch_airport_data('KAVL')
        
        # Check if the data is not None
        assert airport_data is not None, "Failed to fetch airport data"
        
        # Check if the data contains the expected keys
        assert 'KAVL' in airport_data, "ICAO code not found in the response"
        
        # Check if the data contains expected fields
        airport_info = airport_data['KAVL'][0]
        assert 'facility_name' in airport_info, "Facility name not found in the response"
        assert 'city' in airport_info, "City not found in the response"


def test_mock_fetch():
    mock_fetch_data = Mock()
    mock_fetch_data.return_value = {
        "KAVL": [
            {
                "facility_name": "Asheville Regional Airport",
                "city": "Asheville",
                "state": "NC",
                "country": "Canada"
            }
        ]
    }

    airport_data = mock_fetch_data('KAVL')

    ## mock_api_client.get.return_value = mock_response
    with patch('api2.fetch_airport_data', mock_fetch_data):
        airport_data = api2.fetch_airport_data('KAVL')   
        # Check if the data contains expected fields
        airport_info = airport_data['KAVL'][0]
        
        assert 'city' in airport_info, "City not found in the response"
        assert airport_info['city'] == "Asheville", "City name mismatch"
        assert airport_info['state'] == "NC", "State name mismatch"
        assert airport_info['country'] == "Canada", "Country name mismatch"