# Predcting thr Bioactivity of Possible Compounds to Target Bromodomain Protein - Web App Deployed on Heroku



This web app predicts 

The web app was built in Python using the following libraries:
* streamlit
* pandas
* numpy
* scikit-learn
* pickle

[https://bromodomain-bioactivity.herokuapp.com/](https://bromodomain-bioactivity.herokuapp.com/)

# Reproducing this web app
To recreate this web app on your own computer, do the following.

### Create conda environment
Firstly, we will create a conda environment called *bromodomain*
```
conda create -n bromodomain python=3.7.9
```
Secondly, we will login to the *bromodomain* environement
```
conda activate bromodomain
```
### Install prerequisite libraries

Download requirements.txt file

```
wget https://raw.githubusercontent.com/CyrilleMesue/bioactivity_webapp/master/requirements.txt

```

Pip install libraries
```
pip install -r requirements.txt
```

###  Download and unzip contents from GitHub repo

Download and unzip contents from https://github.com/dataprofessor/moldesc-app/archive/main.zip

###  Launch the app

```
streamlit run app.py
