
# AI-Powered Bespoke Jewelry Design Platform

![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Stability AI](https://img.shields.io/badge/API-Stability_AI-ff6b6b)
![Meshy AI](https://img.shields.io/badge/API-Meshy_AI-4ecdc4)

A web-based platform that enables customers and designers to create custom jewelry designs using AI-generated 2D/3D models with material optimization.

## Features ✨

- **AI-Powered Design Generation**
  - 🖼️ Text-to-2D Image Conversion (Stable Diffusion 3)
  - 🎨 Text-to-3D Model Generation (Meshy API)
  - ⚙️ Material Optimization Algorithms

- **Interactive Visualization**
  - 🔍 WebGL 3D Viewer (Three.js)
  - 🖱️ Orbit Controls for Model Manipulation
  - 📐 Real-time Material Estimates

- **Production-Ready Features**
  - 🔒 API Key Configuration
  - 🚦 Error Handling & Logging
  - 📱 Responsive UI

## Tech Stack 🛠️

**Backend**
- Python 3.9+
- Flask
- REST API Integration

**Frontend**
- Three.js (WebGL)
- Modern CSS Grid/Flex Layouts
- Interactive Form Validation

**APIs**
- [Stability AI](https://platform.stability.ai/) - 2D Image Generation
- [Meshy](https://www.meshy.ai/) - 3D Model Generation


1. **Set Up Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Configuration**
Create `.env` file:
```env
STABILITY_API_KEY=your_stability_key
MESHY_API_KEY=your_meshy_key
```

## Usage 🚀

1. **Start Server**
```bash
python app.py
```

2. **Access Web Interface**
```
http://localhost:5000
```

3. **Design Workflow**
1. Enter text description ("Victorian-style silver ring with floral patterns")
2. Select jewelry type and material
3. Generate 2D/3D designs
4. Interact with 3D model
5. View material estimates

## API Reference 📚

### POST `/generate-2d`
**Request**
```json
{
  "prompt": "Art Deco emerald ring",
  "style": "realistic"
}
```

**Response**
```json
{
  "image": "base64_encoded_image",
  "seed": "a1b2c3d4"
}
```

### POST `/generate-3d`
**Request**
```json
{
  "prompt": "Gold necklace with pearl accents",
  "type": "necklace"
}
```

**Response**
```json
{
  "model_url": "https://meshy.ai/models/xyz.glb",
  "materials": {
    "gold": 15.2,
    "volume": 0.8
  }
}
```

## Troubleshooting 🛠️

**Common Issues**
1. **404 Static File Errors**
   - Verify directory structure:
     ```
     /static
       /css
         style.css
       /js
         main.js
     ```

2. **API Key Errors**
   - Confirm keys in `.env`
   - Check provider dashboards for quota

3. **3D Model Loading Issues**
   - Ensure WebGL support in browser
   - Check console for CORS errors

**Sample cURL Test**
```bash
curl -X POST http://localhost:5000/generate-2d \
  -H "Content-Type: application/json" \
  -d '{"prompt": "test ring"}'
```

