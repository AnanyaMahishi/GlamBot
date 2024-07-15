from flask import Flask, render_template, request, redirect, url_for, flash, jsonify,send_from_directory
from werkzeug.utils import secure_filename
import os
import subprocess
from flask_socketio import SocketIO, emit
import color_analysis
from seg_hex_model import segment_and_extract_hex
from capture_image import capture_image
import requests
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError
import requests
import os
import urllib.request
import re
import shutil
from search_outfits import clear_images_folder, search_outfits, fetch_image_urls, extract_product_details, download_images, colors, gender
import base64
from io import BytesIO
from PIL import Image

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
        if "image" in request.files:
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

                        # Redirect to loading page and start color analysis
                        return redirect(url_for("loading", image_path=filepath))

                    else:
                        message = f"Failed to save image '{filename}' to {filepath}. Check folder permissions."
                        flash(message, "danger")
                except Exception as e:
                    message = f"Error saving image: {str(e)}"
                    flash(message, "danger")

    return render_template("photo_pick.html", message=message)


@app.route("/capture_image", methods=["POST"])
def capture_image_route():
    captured_image_data = request.form["capturedImage"]
    if captured_image_data:
        try:
            # Decode the base64 image data
            image_data = base64.b64decode(captured_image_data.split(",")[1])
            image = Image.open(BytesIO(image_data))
            
            # Save the image to the UPLOAD_FOLDER
            filename = "captured_image.png"
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            image.save(filepath)

            if os.path.exists(filepath):
                message = "Captured image saved successfully!"
                flash(message, "success")

                # Redirect to loading page and start color analysis
                return redirect(url_for("loading", image_path=filepath))

            else:
                message = "Failed to save captured image. Check folder permissions."
                flash(message, "danger")
        except Exception as e:
            message = f"Error processing captured image: {str(e)}"
            flash(message, "danger")

    return redirect(url_for("photo_pick"))

@app.route("/loading")
def loading():
    image_path = request.args.get("image_path")
    print(f"Loading image path: {image_path}")
    return render_template("loading.html", image_path=image_path)


@socketio.on("start_color_analysis")
def start_color_analysis(data):
    image_path = data["image_path"]

    # Call the segmentation and extraction function
    print(image_path)
    skin_color, eye_color, hair_color = segment_and_extract_hex(image_path)

    # Perform color analysis
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
    response = request.args.get("response")
    palette = request.args.get("palette")
    recommended_colors = request.args.get("recommended_colors")
    color_hexcodes_list = request.args.get("color_hexcodes_list")

    return render_template(
        "color_analysis_results.html",
        response=response,
        palette=palette,
        recommended_colors=recommended_colors,
        color_hexcodes_list=color_hexcodes_list,
    )


@app.route("/shop_myntra")
def shop_myntra():
    clear_images_folder()
    # save_folder = "/images"
    # os.makedirs(save_folder, exist_ok=True)
    outfits = search_outfits(colors, gender)
    product_details = extract_product_details(outfits)
    for product in product_details:
        name = product['product_title']
        search_term = f"image for {name}"
        image_urls = fetch_image_urls(search_term)
        # product['image_url'] = image_urls[0] if image_urls else None
        # print( product['image_url'])
        if image_urls:
            saved_path = download_images(image_urls[0],product_details.index(product))
            if saved_path:
                product['image_url'] = saved_path 
                print( product['image_url']) 
       
    return render_template('shop_myntra.html', outfits=product_details)

if __name__ == "__main__":
    socketio.run(app, debug=True)
