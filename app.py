import os
from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory
from pii_redactor import pii_redactor

app=Flask(__name__)

# Files can be up to 16MB
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
# Allow these files
app.config['UPLOAD_EXTENSIONS'] = ['.txt', '.pdf', '.docx']
# Send files to upload folder
app.config['UPLOAD_PATH'] = 'uploads/'
#Send redacted files to results folder
app.config['RESULT_PATH'] = 'static/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_files():

    redacted_files = []

    text_input = request.form.get('text_input')

    if text_input and text_input.strip():
        text_input_file_path = os.path.join(app.config['UPLOAD_PATH'], 'text_input.txt')

        with open(text_input_file_path, 'w', encoding='utf-8') as file:
            file.write(text_input)

        redacted_filename = "text_input_redacted.txt"

        output_path = os.path.join(app.config['RESULT_PATH'], redacted_filename) 


        pii_redactor(text_input_file_path, output_path)

        redacted_files.append(redacted_filename)



    # Upload multiple files
    for uploaded_file in request.files.getlist('file'):
        if uploaded_file.filename != '':
            # Save files to upload folder
            file_path = os.path.join(app.config['UPLOAD_PATH'], uploaded_file.filename)
            uploaded_file.save(file_path)  

            name, extension = os.path.splitext(uploaded_file.filename) 
            redacted_filename = f"{name}_redacted{extension}" 
            output_path = os.path.join(app.config['RESULT_PATH'], redacted_filename) 

            redacted_files.append(redacted_filename)
            
            pii_redactor(file_path, output_path) 

    
    return render_template('results.html', redacted_files=redacted_files)


@app.route('/<filename>')
def download_file(filename):
    directory = 'static'
    return send_from_directory(directory, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
