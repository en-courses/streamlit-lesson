from streamlit.testing.v1 import AppTest
import api

def test_airport():
    """A user increments the number input, then clicks Add"""
    at = AppTest.from_file("api.py").run(timeout=60)
    at.sidebar.text_input[0].set_value("JFK").run()
    
    assert at.columns[0].metric[0].label == "Latitude"
    assert at.columns[1].metric[0].label == "Longitude"
    assert at.columns[0].metric[0].value == "40-38-23.7400N"
    assert at.columns[1].metric[0].value == "073-46-43.2930W"