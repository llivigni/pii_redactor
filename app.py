import os
from flask import Flask, render_template, request, redirect, url_for, abort
from pii_redactor import PiiRedactor

# Initialize PII_Redactor class
redactor = PiiRedactor()

# Initiate Flask app
app=Flask(__name__)

# Files can be up to 16MB
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
# Allow these files
app.config['UPLOAD_EXTENSIONS'] = ['.txt', '.pdf', '.docx']
# Send files to upload folder
app.config['UPLOAD_PATH'] = 'uploads/'
#Send redacted files to results folder
#app.config['RESULT_PATH'] = 'results/'
app.config['RESULT_PATH'] = 'static/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_files():

    redacted_files = []

    # Upload multiple files
    for uploaded_file in request.files.getlist('file'):
        if uploaded_file.filename != '':
            # Save files to upload folder
            file_path = os.path.join(app.config['UPLOAD_PATH'], uploaded_file.filename)
            uploaded_file.save(file_path)  

            name, extension = os.path.splitext(uploaded_file.filename) 
            #redacted_filename = f"{name}_redacted{extension}"      
            redacted_filename = f"{name}_redacted.txt" 
            output_path = os.path.join(app.config['RESULT_PATH'], redacted_filename) 

            redacted_files.append(redacted_filename)
            
            pii_redactor(file_path, output_path) 

    
    #return uploaded_file.filename
    return render_template('results.html', redacted_files=redacted_files)


@app.route('/<filename>')
def download_file(filename):
    directory = 'static'
    return send_from_directory(directory, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
