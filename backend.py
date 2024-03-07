from flask import Flask, render_template, request, redirect, jsonify
import uuid
import json
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
import logging
from triz_config import TrizConfig as CONFIG
from sessions import Sessions
from rioquery import TrizDoc, DocumentData

app = Flask(__name__)
CORS(app, resources={r"/api/*": CONFIG.CORS_RESOURCES})


chat_messages = []
document = DocumentData().collection

# Define the folder where uploaded documents will be stored
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'txt'}  # Specify allowed file extensions here

"""
The upload route is meant to work as file uploader. At this point
this is more of a placeholder. This function need to be revisited.
"""
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the POST request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an empty file without a filename
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'File uploaded successfully'
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

"""
The converse API endpoint interacts with the UIX. 
It receives messages from the users, sends it as a request to the AI and
returns the AI response. It also manages session IDs.
"""
@app.route('/api/converse', methods=['GET', 'POST'])
def converse():
    if request.method == 'POST':
        data = request.json
        message = data.get('message', '')
        session_id = data.get('session_id', '')
        if session_id == '' :
            session_id = Sessions.create_session()
            Sessions.set_chat_object(chat_id=session_id, chat_object=TrizDoc(retrieval_document=document)) # create new instance of Trizdoc and save it with the session id.
        
        chat_object = Sessions.get_chat_object(session_id)
        response, session_id = chat_object.query(prompt=message, session_id=session_id)

        response_data = {
            'message': response,
            'session_id': session_id
        }
        json_str = json.dumps(response_data, indent=4)
        print("\n\n\n", json_str)
        return jsonify(response_data)
    return jsonify({'error': 'method not allowed'}), 405

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True, host='0.0.0.0')
