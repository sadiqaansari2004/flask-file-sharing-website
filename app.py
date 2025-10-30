from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file found"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        # Step 1: Get an available GoFile.io server
        server_res = requests.get("https://api.gofile.io/getServer")
        server_data = server_res.json()
        upload_server = server_data['data']['server']

        # Step 2: Upload the file to that server
        upload_url = f"https://{upload_server}.gofile.io/uploadFile"
        files = {'file': (file.filename, file.stream, file.mimetype)}

        upload_res = requests.post(upload_url, files=files)
        data = upload_res.json()

        # Step 3: Return the download link to frontend
        if data['status'] == 'ok':
            download_link = data['data']['downloadPage']
            return jsonify({"link": download_link})
        else:
            print("GoFile error:", data)
            return jsonify({"error": "Upload failed, please try again."}), 500

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    app.run(debug=True)
