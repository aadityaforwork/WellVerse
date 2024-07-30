import streamlit as st
from datetime import datetime
# import openai
import requests
import os

openai.api_key = api_key


# Initialize OpenAI (ensure you have set your API key)

def analyze_journal_entry(text):
    """
    Analyze the journal entry and return a depression score (0-10).
    This function is a placeholder for actual analysis.
    """
    response=openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": f"You are a mental health chatbot. Analyze this journal entry for depression signs:{text}"},
       
    ]
    )
    # Interpret the response to generate a depression score
    # This part is simplified and needs refining based on response
    score = interpret_response_to_score(response['choices'][0]['message']['content'])
    return score

def interpret_response_to_score(response):
    """
    Convert OpenAI's response to a depression score.
    This function needs customization based on how you define the response.
    """
    # response2 = client.chat.completions.create(
    #   engine="gpt-3.5-turbo",
    #   prompt=f"Analyse the response submitted by the user : {response} and give a score based on the depression signs. Output given should just be a number between 0-10. I want no text other than that as an output",
    #   temperature=0.7,
    #   max_tokens=60,
    #   top_p=1.0,
    #   frequency_penalty=0.0,
    #   presence_penalty=0.0
    # )
    response2=openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": f"Analyse the response submitted by the user : {response} and give a score based on the depression signs. Output given should just be a number between 0-10. I want no text other than that as an output"},
       
    ]
    )
    # Placeholder for conversion logic
    return response2['choices'][0]['message']['content']  # Example fixed score, replace with actual logic

def get_motivational_quote():
    """
    Generate a motivational quote using OpenAI.
    """
    response3=openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": f"Generate a short motivational quote about gift of life."},
       
    ]
    )
    return response3['choices'][0]['message']['content']

# Streamlit UI
st.title("Emotional Diary with AI Insights")
quote = get_motivational_quote()
st.write(quote)
# Sidebar for journal entries
st.sidebar.header("Journal Entries")
# Assuming 'entries' is a list of dictionaries with date, title, and text
entries = []
selected_entry = st.sidebar.selectbox("Choose an entry", entries, format_func=lambda x: x['title'])

# Main page for adding a new entry
with st.form("new_journal_entry", clear_on_submit=True):
    date = st.date_input("Date", datetime.today())
    title = st.text_input("Title")
    thoughts = st.text_area("Your thoughts for the day")
    submitted = st.form_submit_button("Submit")

    if submitted:
        # Process the new journal entry
        # Here you would save the entry to a database or file system
        depression_score = analyze_journal_entry(thoughts)
        entries.append({'date': date, 'title': title, 'text': thoughts, 'score': depression_score})
        st.success("Journal entry added!")

# Display statistics and motivational quote
if entries:
    st.write(f"Total Journal Entries: {len(entries)}")
    # Display each entry with its depression score
    for entry in entries:
        st.write(f"Title: {entry['title']} - Depression Score: {entry['score']}")
        if float(entry['score']) > 7:
            st.error("This entry indicates high levels of mental stress.")
            st.warning('Scheduling a checkup call on you. Please talk to us or any  authorities immediately')
            requests.get('http://127.0.0.1:5000/call')
            
            
else:
    st.write("No entries yet.")

# Display a motivational quote

