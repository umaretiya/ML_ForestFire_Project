import flask,logging
from flask import Flask, request, jsonify, render_template
import pickle
import bz2
from flask_cors import cross_origin
from logger import Logger
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings("ignore")

app = Flask(__name__)

log = Logger.logger_func()
print('Logger class')

pickle_in = bz2.BZ2File('classification.pkl', 'rb')
log.info("Loading Pickle classificatins file")
model_C = pickle.load(pickle_in)

pickle_r = bz2.BZ2File("regression_rfr.pkl", "rb")
log.info("Loading Pickle regression file")
model_R = pickle.load(pickle_r)

df1 = pd.read_csv("Algerian_fires_data_Cleaned.csv")
print(df1.columns.tolist())

df = df1.drop(['day', 'month', 'year','Rain','Region','RH','DC','BUI'],axis=1)
X = df.drop(['FWI', 'Classes'], axis=1)
scaler = StandardScaler()
X_reg_scaled = scaler.fit_transform(X)

@cross_origin()
@app.route('/')
def home():
    print("home function running")
    log.info('home page is running')
    return render_template('index.html')

@cross_origin()
@app.route('/predict_api', methods=['POST'])
def predict_api():
    try:
        log.info('predict api functions')
        data = request.json['data']
        final_data= [list(data.values())]
        output = int(model_c.predict(final_data))
        if output == 1:
            print("High chnse for fire")
            text = "High chnse for fire"
        else:
            print("Forest is safe from fire")
            text = "Forest is safe from fire"
        return jsonify(output)
    except Exception as e:
        output = 'Check the input again!'
        log.error('Errors i input from pstomat')
        return jsonify(output)

@cross_origin()
@app.route('/predict',methods=['POST'])
def predict():
    try:
        data = [float(x) for x in request.form.values()]
        final_features = [np.array(data)]
        final_features = scaler.transform(final_features)
        output = model_C.predict(final_features)[0]
        log.info('Prediction done for Classification model')
        if output == 0:
            text = 'Forest is Safe!'
        else:
            text = 'Forest is in Danger!'
        return render_template('index.html', prediction_text1="{} --- Chance of Fire is {}".format(text, output))
    except Exception as e:
        log.error('Input error, check input', e)
        return render_template('index.html', prediction_text1="Check the Input again!!!")

    

@cross_origin()
@app.route('/predictR',methods=['POST'])
def predictR():
    try:
        data = [float(x) for x in request.form.values()]
        data = [np.array(data)]
        data = scaler.transform(data)
        output = model_R.predict(data)[0]
        log.info('Prediction done for Regression model')
        if output > 15:
            return render_template('index.html', prediction_text2="Fuel Moisture Code index is {:.4f} ---- Warning!!! High hazard rating".format(output))
        else:
            return render_template('index.html', prediction_text2="Fuel Moisture Code index is {:.4f} ---- Safe.. Low hazard rating".format(output))
    except Exception as e:
        log.error('Input error, check input', e)
        return render_template('index.html', prediction_text2="Check the Input again!!!")



if __name__ == '__main__':
    print("mainstudy project")
    log.info("main app running")
    app.run()
