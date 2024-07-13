from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
import os
import subprocess
from flask_socketio import SocketIO, emit
import color_analysis

app = Flask(__name__)

# Define a folder to store uploaded images
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = "super_secret_key"  # Used for flashing messages
socketio = SocketIO(app)


@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/photo_pick", methods=["GET", "POST"])
def photo_pick():
    message = None
    if request.method == "POST":
        print("POST request received")
        if "image" in request.files:
            print("File 'image' found in request.files")
            image = request.files["image"]
            if image.filename == "":
                message = "No selected file."
            elif image:
                filename = secure_filename(image.filename)
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

                try:
                    image.save(filepath)
                    if os.path.exists(filepath):
                        message = f"Image '{filename}' uploaded successfully!"
                        flash(message, "success")
                        print(f"Image '{filename}' saved to {filepath}")
                    else:
                        message = f"Failed to save image '{filename}' to {filepath}. Check folder permissions."
                        flash(message, "danger")
                        print(f"Failed to save image '{filename}'")
                except Exception as e:
                    message = f"Error saving image: {str(e)}"
                    flash(message, "danger")
                    print(f"Error saving image: {str(e)}")
        else:
            print("No 'image' found in request.files")

    return render_template("photo_pick.html", message=message)


@app.route("/use_camera", methods=["POST"])
def use_camera():
    filename = "captured_image.png"
    save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    # Call the capture_image.py script
    result = subprocess.run(
        ["python", "capture_image.py", save_path], capture_output=True, text=True
    )

    if result.returncode == 0:
        message = f"Image '{filename}' captured and saved successfully!"
        flash(message, "success")
    else:
        message = f"Error capturing image: {result.stderr}"
        flash(message, "danger")

    return redirect(url_for("photo_pick"))


@app.route("/loading")
def loading():
    return render_template("loading.html")


@socketio.on("start_color_analysis")
def start_color_analysis(data):
    skin_color = data["skin_color"]
    eye_color = data["eye_color"]
    hair_color = data["hair_color"]

    response = color_analysis.get_color_analysis(skin_color, eye_color, hair_color)
    palette = color_analysis.extract_palette(response)
    recommended_colors = color_analysis.extract_color(response)
    color_hexcodes_list = color_analysis.get_hexcodes_for_colors(recommended_colors)

    result = {
        "response": response,
        "palette": palette,
        "recommended_colors": recommended_colors,
        "color_hexcodes_list": color_hexcodes_list,
    }

    emit("color_analysis_complete", result)


@app.route("/color_analysis_results")
def color_analysis_results():
    return render_template("color_analysis_results.html")


@app.route("/shop_myntra")
def shop_myntra():
    return render_template("shop_myntra.html")


if __name__ == "__main__":
    app.run(debug=True)
