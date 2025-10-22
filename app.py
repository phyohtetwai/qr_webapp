from flask import Flask, request, send_file, render_template
import os
from datetime import datetime
from qr_generator import generate_pdf

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files.get("file")
    if not file:
        return "No file uploaded", 400

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    input_path = os.path.join(UPLOAD_FOLDER, f"{timestamp}.txt")
    file.save(input_path)

    output_path = os.path.join(UPLOAD_FOLDER, f"QR_{timestamp}.pdf")
    try:
        generate_pdf(input_path, output_path)
    except Exception as e:
        return f"QR generation failed: {e}", 500

    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7777)