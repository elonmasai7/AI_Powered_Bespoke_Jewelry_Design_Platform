from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import base64
import os
import logging
from dotenv import load_dotenv


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Load Environment Variables
load_dotenv()

# Initialize Flask App
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# API Keys
MESHY_API_KEY = os.getenv('MESHY_API_KEY')
STABILITY_API_KEY = os.getenv('STABILITY_API_KEY')

# API Endpoints
SD_API_URL = "https://api.stability.ai/v2beta/stable-image/generate/core"
MESHY_API_URL = "https://api.meshy.ai/openapi/v2/text-to-3d"

# Jewelry Design Defaults
JEWELRY_PARAMS = {
    'ring': {'density': 19.3, 'min_thickness': 1.5},
    'necklace': {'density': 10.5, 'min_chain_size': 0.8},
    'bracelet': {'density': 10.5, 'min_width': 2.0},
    'earrings': {'density': 10.5, 'min_post_size': 0.8}
}

# Validate API Keys on Startup
if not STABILITY_API_KEY or not STABILITY_API_KEY.startswith("sk-"):
    logger.error("Invalid or missing Stability AI API key.")
    exit(1)

if not MESHY_API_KEY:
    logger.error("Missing Meshy API key.")
    exit(1)

@app.route('/verify-keys')
def verify_keys():
    """Endpoint to check if API keys are configured correctly."""
    return jsonify({
        "stability_key_exists": bool(STABILITY_API_KEY),
        "meshy_key_exists": bool(MESHY_API_KEY),
        "stability_key_prefix": STABILITY_API_KEY.startswith("sk-") if STABILITY_API_KEY else False
    })

@app.route('/')
def home():
    """Render the homepage."""
    return render_template('index.html')

@app.route('/generate-2d', methods=['POST'])
def generate_2d():
    """Generate a 2D jewelry design using Stability AI."""
    try:
        data = request.json
        if not data or 'prompt' not in data:
            return jsonify({"error": "Missing 'prompt' in request"}), 400

        logger.info(f"2D Generation Request: {data}")

        headers = {
            "Authorization": f"Bearer {STABILITY_API_KEY}",
            "Accept": "image/*"
        }
        payload = {
            "prompt": f"{data['prompt']}, jewelry design, ultra-detailed, 8k",
            "model": "sd3",
            "output_format": "webp",
            "negative_prompt": "blurry, low quality, sketch"
        }

        response = requests.post(SD_API_URL, headers=headers, files={"none": ''}, data=payload)

        if response.status_code == 200:
            return jsonify({
                "image": base64.b64encode(response.content).decode('utf-8'),
                "format": "webp"
            })

        error_data = response.json()
        logger.error(f"Stability AI Error: {response.status_code} - {error_data}")
        return jsonify(error_data), response.status_code

    except Exception as e:
        logger.error(f"2D Generation Error: {str(e)}")
        return jsonify({"error": "Failed to generate 2D image"}), 500

@app.route('/generate-3d', methods=['POST'])
def generate_3d():
    try:
        data = request.json
        logger.info(f"3D Generation Request: {data}")

        headers = {
            'Authorization': f'Bearer {MESHY_API_KEY}',
            'Content-Type': 'application/json'
        }

        payload = {
            'prompt': data['prompt'],
            'output_format': 'glb',
            'mode': 'preview',
            'art_style': 'realistic',
            'should_remesh': True
        }

        response = requests.post(MESHY_API_URL, headers=headers, json=payload)

        logger.info(f"Meshy API Response Code: {response.status_code}")
        logger.info(f"Meshy API Response Text: {response.text}")

        if response.status_code == 200:
            model_data = response.json()
            return jsonify({
                'model_url': model_data.get('model_url'),
                'thumbnail': model_data.get('thumbnail_url')
            })

        logger.error(f"Meshy API Error: {response.status_code} - {response.text}")
        return jsonify({'error': response.text}), response.status_code

    except Exception as e:
        logger.error(f"3D Generation Error: {str(e)}")
        return jsonify({'error': str(e)}), 500


# Run Flask Server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
