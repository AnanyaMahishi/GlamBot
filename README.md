# GlamBot

GlamBot is an AI-powered fashion recommendation system. This platform leverages advanced image processing, image segmentation, and large language model (LLM) technologies to provide personalized fashion recommendations based on a user's skin color, eye color, and hair color. The recommendations are curated specifically from Myntra's vast collection, helping users find the best outfits that match their unique color profile.

[https://www.canva.com/design/DAGJhe2XXNo/MVcVsDVd2t34Nf0EHBPivQ/edit?utm_content=DAGJhe2XXNo&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton] (Link to Product Description slides)



# Contributors 
Ananya Mahishi
Ananya Jha
Ananya J

# Features

- **Image Upload and Capture**: Users can upload a photo or capture an image using their device's camera.
- **Image Segmentation and Color Extraction**: The system segments the image and extracts the hex codes for skin, eye, and hair colors.
- **Personalized Color Analysis**: Uses the Gemini LLM to perform an in-depth color analysis and determine the best color palette for the user.
- **Fashion Recommendations**: Suggests outfits from Myntra based on the user's color profile.
- **Real-time Results**: Displays the color analysis results and recommended outfits in real-time.

# How To Run

- Clone the repository:
    
    ```
    shCopy code
    git clone https://github.com/yourusername/glambot.git
    cd glambot
    
    ```
    
- Create a virtual environment and activate it:
    
    ```
    shCopy code
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    
    ```
    
- Install the required packages:
    
    ```
    shCopy code
    pip install -r requirements.txt
    
    ```
    

Set up environment variables:

- Create a `.env` file in the root directory.
- Add your Gemini API key to the `.env` file:
    
    ```makefile
    makefileCopy code
    API_KEY=your_gemini_api_key
    
    ```
    

Run the Flask application:

```
shCopy code
python app.py

```

## Code Overview

### `app.py`

- Defines routes for the application (`/`, `/photo_pick`, `/loading`, `/color_analysis_results`, `/shop_myntra`).
- Handles image upload and capture, redirects to the loading page, and initiates color analysis.

### `color_analysis.py`

- Contains functions for interacting with the Gemini LLM to perform color analysis.
- Extracts recommended colors and color palettes from the LLM's response.

### `search_outfits.py`

- Contains functions to search for outfits on Myntra based on the user's color profile.
- Downloads and saves outfit images for display in the application.

### `seg_hex_model.py`

- Implements facial segmentation and color extraction using the FACER library.
- Saves segmented facial parts and extracts hex codes for skin, eye, and hair colors.

# tech stack

Majorly coded in **Python**

**Web framework (To create a lightweight and responsive web application interface)**:

- Flask, HTML and CSS

**ML components used ( To segment images and get colour recommendations) :**

- FACER ( A toolkit built on FaRL model) , Gemini API , Pytorch

**Web Scraping (Extracts data from websites to gather outfit links from Myntra based on recommended colors):**

- Requests , Beautiful Soup

I**mage processing libraries (To preprocess and analyze facial images for color extraction) :**

- ****Pillow and Open CV
