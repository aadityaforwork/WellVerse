from flask import Flask, render_template, request
from datetime import datetime, timedelta
import requests
import google.generativeai as genai
import json
from flask_cors import CORS
import openai

import requests

def check_up_call():
    # Headers
    headers = {
        'Authorization': ""
    }

    # Data
    data = {
        'phone_number': '+',
        'task': """AI, codenamed "Depr.ai," you\'re tasked with reaching out to individuals who may be at risk of suicide or struggling with mental health issues. Your objective is to provide support, guidance, and resources to these individuals in a compassionate and empathetic manner. When making the call, introduce yourself as a representative from [Your Organization] and express genuine concern for the individual's well-being. Encourage them to share their feelings and experiences, and offer assistance in accessing mental health support services. Remember to be patient, understanding, and non-judgmental throughout the conversation, respecting the individual's pace and readiness to seek help. ***If the user seems to be really depressed or at-risk, suggest them to contact the authorities.***

        Explanation:

        As an AI, your role is to simulate human-like interactions and provide support to individuals who may be in distress. In this scenario, you're acting as a health assistant named James, reaching out to individuals based on indicators of distress observed on a website monitoring their online activity. Your goal is to engage the individual in a conversation about their mental health, offering empathy, understanding, and resources to help them cope with their struggles. It's crucial to approach the conversation with sensitivity and compassion, respecting the individual's feelings and autonomy while gently encouraging them to seek professional help if needed. Your prompt serves as a guide to help you navigate the conversation effectively and provide meaningful support to those in need.
        Certainly, here's a dialogue that covers a variety of potential responses from the individual:

        **AI:**
        "Hello, is this [Name]? My name is James, and I'm calling from [Your Organization]. We've noticed some concerning indicators on our website regarding your well-being, and I'm here to offer support. How are you feeling today?

        **Individual:**
        - "I'm doing okay, just a bit stressed out."
        - "I've been feeling really down lately."
        - "Why are you calling me? I'm fine."

        **AI:**
        "I understand, life can get overwhelming sometimes. It's important to recognize when we need extra support. Can you tell me more about what's been causing you stress or making you feel down?"

        **Individual:**
        - "Work's been really hectic lately, and I'm having trouble balancing everything."
        - "I've been dealing with a lot of family issues, and it's been taking a toll on my mental health."
        - "I'm not really sure. I just feel empty most of the time."

        **AI:**
        "I'm sorry to hear that you're going through a tough time. It sounds like you're dealing with a lot right now. Have you thought about talking to someone about what you're going through? There are resources and support services available that can help you cope with stress and manage your mental health."

        **Individual:**
        - "I've thought about it, but I'm not sure where to start."
        - "I'm not ready to talk to a therapist yet."
        - "I don't think talking to anyone will help."

        **AI:**
        "It's understandable to feel unsure about reaching out for help. Taking that step can be daunting, but it's important to remember that you're not alone. Our organization offers confidential support services, and our team is here to assist you every step of the way. Whether you're ready to talk now or need some time to think about it, we're here to support you whenever you're ready."

        **Individual:**
        - "Okay, maybe I'll consider it."
        - "Thanks for calling, but I'm not interested."
        - "I appreciate your concern, but I think I'll be fine on my own."

        **AI:**
        "That's completely okay. Remember, you're in control of your own journey, and it's important to do what feels right for you. If you ever change your mind or need someone to talk to, don't hesitate to reach out to us. Your well-being is important to us, and we're here to support you in any way we can. Take care of yourself, and don't hesitate to reach out if you need assistance. Goodbye for now.\"""",
        'voice_id': 1,
        'reduce_latency': True,
        'request_data': {},
        'voice_settings': {
            'speed': 1
        },
        'interruption_threshold': 0,
        'start_time': None,
        'transfer_phone_number': None,
        'answered_by_enabled': False,
        'from': None,
        'first_sentence': None,
        'record': True,
        'max_duration': 2,
        'model': 'enhanced',
        'language': 'ENG'
    }

    # API request 
    response = requests.post('https://api.bland.ai/call', json=data, headers=headers)
    print(response.text)  # Print response for debugging purposes


openai.api_key = ""
app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})
genai.configure(api_key='')
model = genai.GenerativeModel('gemini-pro')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fitbit_data', methods=['POST'])
def fitbit_data():
    
    access_token = request.form['access_token']
    user_id = request.form['user_id']
    print(access_token, user_id)
    heart_request = requests.get(f'https://api.fitbit.com/1/user/{user_id}/activities/heart/date/today/today.json',
                                headers={'Authorization': 'Bearer ' + access_token})
    heart_data = heart_request.json()

    current_date = datetime.now().strftime("%Y-%m-%d")
    last_month_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    activity_request = requests.get(f'https://api.fitbit.com/1/user/{user_id}/activities/steps/date/{last_month_date}/{current_date}.json',
                                    headers={'Authorization': 'Bearer ' + access_token})
    steps_data = activity_request.json()
    print(steps_data, heart_data)
    steps = steps_data['activities-steps'][-1]['value']
    heart_zones = heart_data['activities-heart'][0]['value']['heartRateZones']
    peak_heart_rate = next((zone['max'] for zone in heart_zones if zone['name'] == 'Peak'), None)

    response = model.generate_content(f"Based on the statistics provided in the heart and steps dataset, decide whether the user is at risk of mental health episodes or not. Return a json file of structure (\\\"atrisk\\\":1) with curly braces heart dataset:{heart_data} steps dataset:{steps_data}").text
    response_on_heartrate = model.generate_content(f"Based on this heart dataset provided by the users wearable, return a text reply which is motivational but also encouraging and realistic about the user's progress. if there are anomalies which may tend to show that the user is at-risk, also acknowledge that.Also show the user how close he is to committing suicide or not in percentage based on the dataset where 50% is normal. Keep the text below 40 words!Heart Dataset: {heart_data}").text
    response_on_steps = model.generate_content(f"Based on this steps dataset provided by the users wearable, return a text reply which is motivational but also encouraging and realistic about the user's progress. if there are anomalies which may tend to show that the user is at-risk, also acknowledge that. Also show the user how close he is to committing suicide or not in numbers based on the dataset where 50% is normal. Keep the text below 40 words!Steps Dataset: {steps_data}").text

    payload={"heart_data":heart_data,"steps_data":steps_data,"atrisk":json.loads(response)['atrisk'],"heart_text":response_on_heartrate,"steps_text":response_on_steps,"peak_heart_rate":peak_heart_rate,"steps_today":steps}
    print(payload)
    return payload
@app.route('/history', methods=['POST'])
def history():
    print(request.json)
    urls=[]
    for i in request.json:
        print(i['url'])
        urls.append(i['url'])
    print(urls)
    response=openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a mental health watchlist bot. You are given a list of urls and you have to detect whether the user is at risk. Return a json of structure (\"atrisk\":1) with curly braces if the user is at risk. If not, return (\"atrisk\":0)."},
        {"role": "user", "content": "Search History: "+str(request.json)},
    ]
    )
    gpt_response=json.loads(response['choices'][0]['message']['content'])
    if (gpt_response['atrisk']==1):
    

        print("User is at risk")
        # check_up_call()
        return json.loads('{"Risk":1}')
    else:
        print("User is not at risk")
        return json.loads('{"Risk":0}')
    
@app.route('/call', methods=['GET'])
def call():
    print('calling')
    check_up_call()
    
    return json.loads('{"Risk":1}')
    
if __name__ == '__main__':
    app.run(debug=True)
