import streamlit as st
import requests
from textblob import TextBlob
urll="https://api.bland.ai/v1/calls"
authorization_token = ""
headers = {"authorization": authorization_token}
list_ofcid= requests.request("GET", urll, headers=headers)


listOfCid=list_ofcid.json()['calls']

def fetch_call_recording(call_id):
    url = f"https://api.bland.ai/v1/calls/{call_id}/recording"
    response = requests.get(url, headers=headers)
    return response.json() 
def fetch_call_details(call_id, authorization):
    url = f"https://api.bland.ai/v1/calls/{call_id}"
    headers={"authorization": authorization}
    response = requests.get(url, headers=headers)
    return response.json()  # Assuming the API returns JSON
for i in listOfCid:
    st.subheader("C_id="+i['c_id'])
    st.subheader(f"From: {i['from']}. To: {i['to']}.")

    recording_data = fetch_call_recording(i['c_id'])
    
    # Assuming the transcript is available in the response. 
    # You might need to adjust the key based on the actual structure of the response
    # transcript = recording_data.get('transcript', 'No transcript available')
    print(recording_data)
    # check if recording data is a json or a string
    call_deets = fetch_call_details(i['c_id'], authorization_token)
    if isinstance(call_deets, dict):
        transcript = call_deets.get("concatenated_transcript", 'No transcript available')
        st.success(f"Transcript: \n{transcript}")
    else:
        # transcript = 'No transcript available'
        pass
    # if isinstance(recording_data, dict):
        # transcript = recording_data.get('url', 'No transcript available')
    # else:
        # transcript = 'No transcript available'
    print()
    # st.write(f"Transcript: \n{transcript}")
    

# Function to fetch call details
def fetch_call_details(call_id, authorization):
    url = f"https://api.bland.ai/v1/calls/{call_id}"
    headers = {"authorization": authorization}
    response = requests.get(url, headers=headers)
    return response.json()  # Assuming the API returns JSON

# Function to fetch call recording
 # Assuming the API returns JSON

# Function for sentiment analysis
def analyze_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment

# Streamlit app layout
st.title("Call Analysis for Mental Health Support")

# Input fields for Call ID and Authorization Token
call_id = st.text_input("Call ID")
authorization_token = ""

# Button to fetch call details and recording
if st.button("Analyze Call"):
    if call_id and authorization_token:
        # Fetch call details and recording
        call_details = fetch_call_details(call_id, authorization_token)
        call_recording = fetch_call_recording(call_id)
        
        # Assuming the call transcript is part of the call details
        transcript = call_details.get("transcript", "")
        
        # Perform sentiment analysis on the transcript
        sentiment = analyze_sentiment(transcript)
        
        # Display results
        st.subheader("Call Details")
        st.json(call_details)
        
        st.subheader("Call Recording")
        st.json(call_recording)
        
        st.subheader("Sentiment Analysis")
        st.write(f"Sentiment: {sentiment}")
        
        # Additional analysis can be added here
    else:
        st.error("Please enter both a Call ID and an Authorization Token.")

