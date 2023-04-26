

from flask import Flask, render_template, request,session
from flask_wtf import FlaskForm
from wtforms import FileField,SubmitField
import os
from werkzeug.utils import secure_filename

import imageio as iio

import tensorflow as tf
from PIL import Image
import numpy as np
from numpy import asarray
 

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)

# WSGI Application
# Defining upload folder path
UPLOAD_FOLDER = os.path.join('static')
# # Define allowed files
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
 
# Provide template folder name
# The default folder name should be "templates" else need to mention custom folder name for template path
# The default folder name for static files should be "static" else need to mention custom folder for static path
app = Flask(__name__, template_folder='templates', static_folder='static')
# Configure upload folder for Flask application
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
 
# Define secret key to enable session
app.secret_key = 'This is your secret key to utilize session in Flask'
 
 


@app.route('/',  methods=("POST", "GET"))
def hello_world():
     if request.method == 'POST':
        # Upload file flask
        uploaded_img = request.files['myfile']
        # Extracting uploaded data file name
        img_filename = secure_filename(uploaded_img.filename)
        # Upload file to database (defined uploaded folder in static path)
        uploaded_img.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))
        # Storing uploaded file path in flask session
        session['uploaded_img_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)
        
        
        savedModel= tf.keras.models.load_model("C:/Users/pathr/Downloads/Model.h5")

        img = Image.open(session['uploaded_img_file_path'])
 

        numpydata = asarray(img)
        arr_resized = np.resize(numpydata, (201, 201, 3))

        # slice the resized array to get a shape of (1, 201, 201, 2)
        arr_final = arr_resized[:,:,:2].reshape(1, 201, 201, 2)

        a=savedModel.predict(arr_final)
        b=a[0][0]%155
        
        str=''
        if b<=33:
            str='Tropical Depression'
        elif b>33 and b<=63:
            str='Tropical Storm'
        elif b>63 and b<=129:
            str='Typhoon'
        elif b>129:
            str='Super Typhoon'
        return render_template("index.html",b=b,str=str)
     return render_template("index.html")
    



if __name__=="__main__":
    app.run(debug=True)
