import streamlit as st
import pandas as pd
from PIL import Image
import os
import base64
import pickle

import warnings
# stdlib. imports
from collections import OrderedDict
from time import sleep;
from padelpy import padeldescriptor
from padelpy import from_smiles
from sklearn.feature_selection import VarianceThreshold
import jdk
jdk.install('11', jre=True)

# Molecular descriptor calculator
def desc_calc(smiles):
    # Performs the descriptor calculation
    # df is a dataframe containing the calculated molecular descriptors from the given smiles
    output = from_smiles(smiles, output_csv = None, descriptors= False,fingerprints = True, timeout = 60)
    if type(output) == OrderedDict:
        columns = [key for key in list(output.keys())]
        values = [ int(value) for value in list(output.values())]
        df = pd.DataFrame(val, columns = columns)
        
    else:
        df = pd.DataFrame(output).apply(lambda x: pd.Series(x))
    
    return df

# File download
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="prediction.csv">Download Predictions</a>'
    return href

# Model building
def build_model(input_data):
    # Reads in saved regression model
    load_model = pickle.load(open('Bromodomain_protein_target_bioactivity_model.pkl', 'rb'))
    # Apply model to make predictions
    st.write(input_data)
    st.write("OK")
    # removing the IDs column
    clean_input_data = input_data.drop("Name", axis = 1)
    #clean_input_data = remove_low_variance(clean_input_data, threshold=0.1)
   
    prediction = load_model.predict(clean_input_data)
    
    st.header('**Prediction output**')
    prediction_output = pd.Series(prediction, name='pIC50')
    molecule_name = pd.Series(load_data[1], name='molecule_name')
    df = pd.concat([molecule_name, prediction_output], axis=1)
    st.write(df)
    st.markdown(filedownload(df), unsafe_allow_html=True)

def remove_low_variance(input_data, threshold=0.1):
    selection = VarianceThreshold(threshold)
    selection.fit(input_data)
    return input_data[input_data.columns[selection.get_support(indices=True)]]
# Logo image
image = Image.open('logo.png')

st.image(image, use_column_width=True)

# Page title
st.markdown("""
# Bioactivity Prediction App (Bromodomain Protein Target)

This app allows you to predict the bioactivity towards inhibting the `Bromodomain target` protein. `Bromodomain` is a drug target for testicular cancer.

**Credits**
- App built in `Python` + `Streamlit` by [Cyrille M. NJUME](https://cyrillemesue.github.io/)
- Descriptor calculated using PubChem [PaDEL-Descriptor](http://www.yapcwsoft.com/dd/padeldescriptor/) [[Read the Paper]](https://doi.org/10.1002/jcc.21707).
---
""")

# Sidebar
with st.sidebar.header('1. Upload your CSV data'):
    uploaded_file = st.sidebar.file_uploader("Upload your input file", type=['txt'])
    st.sidebar.markdown("""
[Example input file](https://raw.githubusercontent.com/CyrilleMesue/bioactivity_webapp/master/bromodomain_example.txt)
""")

if st.sidebar.button('Predict'):
    load_data = pd.read_table(uploaded_file, sep=' ', header=None)
    smiles = list(load_data[0])
    CHEMBEL_ids = list(load_data[1])
    names = pd.DataFrame(CHEMBEL_ids, columns = ['Name'])

    st.header('**Original input data**')
    st.write(load_data)

    with st.spinner("Calculating descriptors..."):
        descriptors = desc_calc(smiles)
        
    descriptors = pd.concat([names,descriptors], axis=1)

    # Read in calculated descriptors and display the dataframe
    st.header('**Calculated molecular descriptors**')
    st.write(descriptors)
    st.write(descriptors.shape)

    # Read descriptor list used in previously built model
    st.header('**Subset of descriptors from previously built models**')
    Xlist = list(descriptors.columns)
    desc_subset = descriptors[Xlist]
    st.write(desc_subset)
    st.write(desc_subset.shape)
    
    # Apply trained model to make prediction on query compounds
    build_model(desc_subset)
else:
    st.info('Upload input data in the sidebar to start!')
