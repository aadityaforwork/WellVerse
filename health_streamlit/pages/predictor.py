import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import pickle

# Load your trained models

with open('C:\\Users\\Swar Jagdale\\Code\\Untitled Folder\\models\\EEGClassifier.pkl', 'rb') as f:
    random_forest_model = pickle.load(f)

# User input for features
def user_input_features():
    # User inputs for features
    sex = st.selectbox('Sex', ['Male', 'Female'],key='assasdd')
    iq = st.number_input('IQ', min_value=0, value=100,key='gds')
    age = st.number_input('Age', min_value=0, value=30,key='345')

    # Direct inputs or calculations for COH_MEAN and AB_MEAN
    COH_A_MEAN = st.number_input('COH_A_MEAN', value=0.0,key='ager')
    COH_B_MEAN = st.number_input('COH_B_MEAN', value=0.0,key='hrt')
    COH_C_MEAN = st.number_input('COH_C_MEAN', value=0.0,key='uyh')
    COH_D_MEAN = st.number_input('COH_D_MEAN', value=0.0,key='guyi')
    COH_E_MEAN = st.number_input('COH_E_MEAN', value=0.0,key='asg')
    COH_F_MEAN = st.number_input('COH_F_MEAN', value=0.0,key='lhiu')
    AB_MEAN = st.number_input('AB_MEAN', value=0.0,key='houi')
    specdis = st.selectbox('Specific Disorder', ['Alcohol use disorder', 'Acute stress disorder',
       'Depressive disorder', 'Healthy control',
       'Behavioral addiction disorder', 'Obsessive compulsitve disorder',
       'Schizophrenia', 'Panic disorder', 'Social anxiety disorder',
       'Posttraumatic stress disorder', 'Adjustment disorder',
       'Bipolar disorder'],key='gu2yi')
    # Process IQ and age into bins as in your notebook
    IQ_bins = 'low' if iq < 85 else 'high' if iq > 115 else 'mid'
    age_bins = 'young' if age < 25 else 'old' if age > 55 else 'mid'

    # Creating a DataFrame for the features
    data = {
        'no.':[0],
        'sex': [sex],
        'IQ_bins': [IQ_bins],
        'age_bins': [age_bins],
        'COH_A_MEAN': [COH_A_MEAN],
        'COH_B_MEAN': [COH_B_MEAN],
        'COH_C_MEAN': [COH_C_MEAN],
        'COH_D_MEAN': [COH_D_MEAN],
        'COH_E_MEAN': [COH_E_MEAN],
        'COH_F_MEAN': [COH_F_MEAN],
        'AB_MEAN': [AB_MEAN],
        'specific.disorder': [specdis]
    }
    features = pd.DataFrame(data)
    return features

st.title("EEG Disorder Prediction")
df_user = user_input_features()



# Encode categorical features
le = LabelEncoder()
# Assuming 'sex', 'IQ_bin', and 'age_bin' are the only categorical features
# You'll need to fit_transform your training data categories beforehand or save the encoder
df_user['sex'] = le.fit_transform(df_user['sex'])
df_user['IQ_bins'] = le.fit_transform(df_user['IQ_bins'])
df_user['age_bins'] = le.fit_transform(df_user['age_bins'])
df_user['specific.disorder'] = le.fit_transform(df_user['specific.disorder'])
# Display user inputs
st.subheader('User Input Features')
st.write(df_user)

# Predict button
if st.button('Predict'):

    prediction_random_forest = random_forest_model.predict(df_user.to_numpy())
    st.subheader('Predictions')
    selected_columns = prediction_random_forest
    st.success(f'#### WellVerseAI Prediction: {prediction_random_forest[0]}')