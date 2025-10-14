import os
from flask import Flask, render_template, request, redirect, url_for, abort

app=Flask(__name__)

# Files can be up to 16MB
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
# Allow these files
app.config['UPLOAD_EXTENSIONS'] = ['.txt', '.pdf', '.doc', '.docx']
# Send files to upload folder
app.config['UPLOAD_PATH'] = 'uploads/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_files():

    files_for_redaction = []                                        # List for uploaded files

    # Upload multiple files
    for uploaded_file in request.files.getlist('file'):
        if uploaded_file.filename != '':
            # Save files to upload folder
            uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], uploaded_file.filename))            
            files_for_redaction.append(uploaded_file.filename)      # Saves files to list
    
    #return uploaded_file.filename
    return files_for_redaction

if __name__ == "__main__":
    app.run(debug=True)
