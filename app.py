import base64
from flask import Flask, request, jsonify
import re
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/bfhl', methods=['GET', 'POST'])
def bfhl():
    if request.method == 'GET':
        return jsonify({"operation_code": 1}), 200
     
    elif request.method == 'POST':
        try:
            data = request.json.get("data", [])
            file_b64 = request.json.get("file_b64", None)
            email = request.json.get("email", "")
            roll_number = request.json.get("roll_number", "")
            
            if not email.endswith("srmist.edu.in"):
                return jsonify({"is_success": False, "message": "Invalid email format"}), 400
            
            roll_number_pattern = re.compile(r'^RA\d{14}$')
            if not roll_number_pattern.match(roll_number):
                return jsonify({"is_success": False, "message": "Invalid roll number format"}), 400
            
            numbers = [item for item in data if item.isdigit()]
            alphabets = [item for item in data if item.isalpha()]
            lower_alphabets = [char for char in alphabets if char.islower()]
            highest_lowercase_alphabet = max(lower_alphabets) if lower_alphabets else None

            file_valid = False
            file_mime_type = ""
            file_size_kb = ""
            
            if file_b64:
                try:
                    file_data = base64.b64decode(file_b64)
                    file_size_kb = len(file_data) / 1024
                    file_mime_type = "application/octet-stream"
                    file_valid = True
                except Exception:
                    file_valid = False
            
            response = {
                "is_success": True,
                "user_id": "john_doe_17091999",
                "email": email,
                "roll_number": roll_number,
                "numbers": numbers,
                "alphabets": alphabets,
                "highest_lowercase_alphabet": [highest_lowercase_alphabet] if highest_lowercase_alphabet else [],
                "file_valid": file_valid,
                "file_mime_type": file_mime_type,
                "file_size_kb": str(file_size_kb)
            }
            return jsonify(response), 200
        
        except Exception as e:
            return jsonify({"is_success": False, "error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
