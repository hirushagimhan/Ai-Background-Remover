from flask import Flask, render_template, request, send_file
from rembg import new_session, remove
from PIL import Image
import io
import os

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
OUTPUT_FOLDER = "static/outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "image" not in request.files:
            return "No file uploaded", 400

        file = request.files["image"]
        if file.filename == "":
            return "No file selected", 400

        # Validate file type
        if file.filename.lower().endswith(("png", "jpg", "jpeg")):
            input_path = os.path.join(UPLOAD_FOLDER, file.filename)
            output_path = os.path.join(OUTPUT_FOLDER, "output.png")

            file.save(input_path)

            # Remove background
            with Image.open(input_path) as img:
                result = remove(img)
                result.save(output_path, "PNG")

            return render_template("index.html", uploaded=True, input_image=input_path, output_image=output_path)

    return render_template("index.html", uploaded=False)

if __name__ == "__main__":
    app.run(debug=True)
