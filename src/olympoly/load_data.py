from urllib import response
from datasets import load_dataset
import pandas as pd
import requests

# Settings to fetch Demographic Data of Countries using Census API

API_KEY = "TYPE KEY HERE"
BASE_URL = "https://api.census.gov/data/timeseries/idb/5year"

params = {
    "get": "NAME,GENC,POP,TFR,E0,IMR,GR,NMR,CBR,CDR",
    "YR": "2026",
    "for": "genc standard countries and areas:*",
    "key": API_KEY
}


# Load the Olympic dataset from the repository, turn it into a pandas dataframe and return it
def load_olympic_data():
    dataset = load_dataset("Haider67795/veriseti_20220203_olimpiyatlar",
                           data_files="veriseti_20220203_olimpiyatlar.csv")
    return dataset['train'].to_pandas()

# Load Demographic data using Census API and return it as a pandas dataframe
def load_demographic_data():

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    # First row is the header
    df = pd.DataFrame(data[1:], columns=data[0])

    # Drop redundant geography column
    df = df.drop(columns=["genc standard countries and areas"])

    # Fix data types
    for col in ["POP", "TFR", "E0", "IMR", "GR", "NMR", "CBR", "CDR"]:
        df[col] = pd.to_numeric(df[col])

    ###### Need to rename these variables to understadable names #####

    return df

data = load_demographic_data()
print(data.head(10))