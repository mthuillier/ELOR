import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

time = datetime.date(datetime.now())
st.title('ELOR on ' + str(time))

DATA_URL = "ELOR.csv"

@st.cache
def load_data():
    data = pd.read_csv(DATA_URL)
    data.drop(data.columns[0], axis=1, inplace=True)
    data = data[["name","1","latitude","longitude"]]
    data.columns = ["Teams","ELOR","latitude","longitude"]
    data = data.head(10)
    return data

data = load_data()

st.map(data, zoom = 15)
    

#https://docs.streamlit.io/tutorial/create_a_data_explorer_app.html