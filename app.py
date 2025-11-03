from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Get the uploaded file
        file = request.files.get('file')
        if not file:
            return jsonify({"error": "No file provided"}), 400

        # Upload to GoFile API
        response = requests.post(
            "https://api.gofile.io/uploadFile", files={'file': file})

        # Try to read JSON safely
        try:
            result = response.json()
        except ValueError:
            print("Invalid response from API:", response.text)
            return jsonify({"error": "Invalid response from GoFile API"}), 500

        return jsonify(result)

    except Exception as e:
        print("Unexpected error:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
