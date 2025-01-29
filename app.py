import pandas as pd
import numpy as np
import tensorflow as tf
import streamlit as st
from sklearn.preprocessing import StandardScaler,LabelEncoder,OneHotEncoder
import pickle

model = tf.keras.models.load_model('model.h5')

#load the encoder and scaler
with open('label_encoded_gender.pkl', 'rb') as file:
    label_encoded_gender = pickle.load(file)

with open('onehot_encoded_geo.pkl', 'rb') as file:
    onehot_encoded_geo = pickle.load(file)

with open('scaler.pkl', 'rb') as file:
    scaler = pickle.load(file)

##streamlit app
st.title('Customer Churn Prediction')

#user input
Geography = st.selectbox('Geography', onehot_encoded_geo.categories_[0])
Gender = st.selectbox('Gender', label_encoded_gender.classes_)
Age = st.slider('Age', 18,92)
Balance = st.number_input('Balance')
CreditScore = st.number_input('Credit Score')
EstimatedSalary = st.number_input('Estimated Salary')
Tenure = st.slider('Tenure', 0,10)
NumOfProducts= st.slider('Number of Prducts',1,4)
HasCrCard = st.selectbox('Has Credit Card',[0,1])
IsActiveMember = st.selectbox('Is Active Member',[0,1])

#prepare input data
input_data = pd.DataFrame({
    'CreditScore' : [CreditScore],
    'Gender' :[label_encoded_gender.transform([Gender])[0]],
    'Age' : [Age],
    'Tenure':[Tenure],
    'Balance':[Balance],
    'NumOfProducts':[NumOfProducts],
    'HasCrCard' :[HasCrCard],
    'IsActiveMember' : [IsActiveMember],
    'EstimatedSalary':[EstimatedSalary]
})


#one-hot encoded Geography
geo_encoded = onehot_encoded_geo.transform([[Geography]]).toarray()
geo_encoded_df = pd.DataFrame(geo_encoded,columns=onehot_encoded_geo.get_feature_names_out(['Geography']))

#Combine one-hot encoded columns with input data
input_data = pd.concat([input_data.reset_index(drop=True),geo_encoded_df], axis=1)

#Scale the input data
input_data_scaled = scaler.transform(input_data)

#Predict churn
prediction = model.predict(input_data_scaled)
prediction_prob = prediction[0][0]

st.write(f'Churn Probability: {prediction_prob:.2f}')
if prediction_prob > 0.5:
    st.write('The Customer is likely to churn.')
else: st.write('The Customer is not likely to churn.')