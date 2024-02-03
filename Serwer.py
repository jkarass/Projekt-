from flask import Flask, request, send_file, jsonify
from cryptography.fernet import Fernet
import os

app = Flask(__name__)

key = Fernet.generate_key()
cipher_suite = Fernet(key)

UPLOAD_FOLDER = 'uploaded_files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def encrypt_file(file_path, key):
    with open(file_path, 'rb') as file:
        data = file.read()
        encrypted_data = cipher_suite.encrypt(data)
    with open(file_path, 'wb') as file:
        file.write(encrypted_data)

def decrypt_file(file_path, key):
    with open(file_path, 'rb') as file:
        data = file.read()
        decrypted_data = cipher_suite.decrypt(data)
    with open(file_path, 'wb') as file:
        file.write(decrypted_data)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']
    if file.filename == '':
        return 'No selected file'

    if file:
        new_filename = 'encrypted_' + file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)

        file.save(file_path)

        encrypt_file(file_path, key)

        return 'File uploaded and encrypted successfully'

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        decrypt_file(file_path, key)

        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return f"Error: {e}", 500

@app.route('/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        os.remove(file_path)
        
        return 'File deleted successfully'
    except Exception as e:
        return f"Error: {e}", 500

@app.route('/browse', methods=['GET'])
def browse_files():
    file_list = []
    for file_name in os.listdir(app.config['UPLOAD_FOLDER']):
        if file_name.startswith('encrypted_'):
            file_list.append(file_name)
    return jsonify(file_list)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)



