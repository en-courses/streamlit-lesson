import streamlit as st
import requests

st.title('✈️ Aviation Airport Data App')

st.sidebar.header('Input')
icao_code = st.sidebar.text_input('Enter ICAO airport code', 'KAVL')

if icao_code:
    airport_url = f'https://api.aviationapi.com/v1/airports?apt={icao_code}'
    response = requests.get(airport_url)
    
    if response.status_code == 200:
        airport_data = response.json()
        
        if airport_data and icao_code in airport_data:
            airport_info = airport_data[icao_code][0]
            st.header(f'Airport Information for {icao_code}')
            
            st.info(f"Facility Name: {airport_info['facility_name']}")
            st.write(f"**City:** {airport_info['city']}, **State:** {airport_info['state_full']}")
            st.write(f"**County:** {airport_info['county']}")
            st.write(f"**Elevation:** {airport_info['elevation']} ft")
            st.write(f"**Control Tower:** {'Yes' if airport_info['control_tower'] == 'Y' else 'No'}")
            st.write(f"**Manager:** {airport_info['manager']} ({airport_info['manager_phone']})")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label='Latitude', value=airport_info['latitude'])
            with col2:
                st.metric(label='Longitude', value=airport_info['longitude'])
        else:
            st.error('Airport data not available for this ICAO code.')
    else:
        st.error('Failed to retrieve data. Please check the ICAO code.')