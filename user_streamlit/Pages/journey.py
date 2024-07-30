import streamlit as st
import openai


openai.api_key = api_key


# Function to generate AI response based on user input
def generate_response(user_input):
   
    response=openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
     messages=[
        {"role": "system", "content": f"The following is a conversation with an AI assistant about mental health. The assistant is helpful, creative, clever, and very friendly. Your task is to make a mental health journey plan for a user. His input is {user_input}.Make a detailed journey with steps and make it with points."},
        
        ],
        )
    # print(response)
    return response["choices"][0]["message"]["content"]

# Streamlit UI
def main():
    st.title('Personalized Mental Health Journey')

    st.write("#### Welcome to the Personalized Mental Health Journey Generator! Please provide some information about yourself and your mental health concerns, and we'll generate a personalized mental health journey for you.")

    # Text input for user's description
    user_description = st.text_area('Please provide some information about yourself or your mental health concerns:')

    # Dropdown for selecting mood
    mood_options = ['Happy', 'Sad', 'Anxious', 'Stressed', 'Neutral']
    selected_mood = st.selectbox('How are you feeling today?', mood_options)

    # Number input for stress level
    stress_level = st.slider('On a scale of 1 to 10, how stressed are you?', 1, 10, 5)

    # Button to trigger AI response generation
    if st.button('Generate Mental Health Journey'):
        user_input = f"{user_description} My mood is {selected_mood.lower()}. My stress level is {stress_level}."
        ai_response = generate_response(user_input)
        st.write('Our plan for you!')
        st.write(ai_response)

if __name__ == '__main__':
    main()
