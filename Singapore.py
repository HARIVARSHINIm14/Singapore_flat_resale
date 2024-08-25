import streamlit as st
import pandas as pd
import pickle

# Load data
data = pd.read_csv(r"C:\\Users\\hariv\\OneDrive\\Desktop\\Data Science\\Python\\Resale\\Singapore_resale.csv")
# Create dictionary to get the encoded values
town_dict = dict(zip(data['town'].unique(), data['town_code'].unique()))
model_dict = dict(zip(data['flat_model'].unique(), data['flat_model_code'].unique()))
town_list = data['town'].unique()
model_list = data['flat_model'].unique()
type_cat = {'1 ROOM': 1, '2 ROOM': 2, '3 ROOM': 3, '4 ROOM': 4, '5 ROOM': 5, 'EXECUTIVE': 6, 'MULTI GENERATION': 7}
type_list = list(type_cat.keys())

# Set page config for the web app
st.set_page_config(page_title='Price Prediction', page_icon=':bar_chart:', layout='wide')
st.title('Singapore Flat Resale Price Prediction')

# Create columns in UI
col1, col2, col3, col4 = st.columns(4)

with col1:
    # Create input field for year input
    Selling_Year = st.number_input('Selling Year', value=None, placeholder="yyyy")

with col2:
    # Create input field for month input
    Selling_Month = int(st.select_slider('Selling month', options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]))

with col3:
    # Create input field for town
    town_key = st.selectbox('Town', options=town_list)

with col4:
    # Create input field for flat type
    flat_type = st.selectbox('Flat Type', options=type_list)

with col1:
    # Create input field for storey range
    storey_range = st.text_input('Storey range', value=None, placeholder="ex: 01 TO 03")

with col2:
    # Create input field for floor area
    floor_area_sqm = st.number_input('Floor Area (sqm)', value=None, placeholder="Type floor area...")

with col3:
    # Create input field for flat model
    flat_model = st.selectbox('Flat Model', options=model_list)

with col4:
    # Create input field for lease commence date
    lease_commence_date = st.number_input('Lease Commence Date', value=None, placeholder="yyyy")

# Function to load pickled model
def model_data():
    with open(r"C:\\Users\\hariv\\OneDrive\\Desktop\\Data Science\\Python\\Resale\\resale", "rb") as files:
        model = pickle.load(files)
    return model

# Function to predict
def predict(model, a, b, c, d, e, f, g, h):
    pred_value = model.predict([[a, b, c, d, e, f, g, h]])
    return pred_value 

# Create predict button
if st.button('Predict Price'):
    town = town_dict[town_key]
    flat_type = type_cat[flat_type]
    if storey_range is not None:
        storey_min, storey_max = map(int, storey_range.split(" TO "))
    flat_modelcode = model_dict[flat_model]

    # Call predict function
    pred = predict(model_data(), Selling_Year, Selling_Month, town, flat_type, storey_min, floor_area_sqm, flat_modelcode, lease_commence_date)

    # Display predicted price in dollar
    st.success(f'Predicted Price: ${pred[0]:,.2f}')

    # Display predicted price in INR
    st.success(f'Resale Price in INR: ₹{(pred[0] * 62.07):,.2f}')
