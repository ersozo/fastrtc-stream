# FastRTC Stream

A real-time video streaming application using FastAPI and WebRTC. This application allows you to stream video from an IP camera through a web interface using WebRTC for low-latency streaming.

## Prerequisites

- Python 3.7+
- Virtual environment (recommended)
- IP camera with accessible video stream URL

## Installation

1. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Open `main.py` and replace the IP camera URL placeholder with your actual IP camera URL:
```python
IP_CAMERA_URL = "http://<your_ip_camera>/video"  # Replace with your camera URL
```

## Running the Application

1. Make sure your virtual environment is activated

2. Start the FastAPI server:
```bash
uvicorn main:app --reload
```

3. Open your web browser and navigate to:
```
http://localhost:8000
```

The application will start streaming video from your IP camera through the web interface.

## Project Structure

- `main.py` - Main FastAPI application with WebRTC implementation
- `templates/` - Contains HTML templates
- `static/` - Static files (JavaScript, CSS)
- `requirements.txt` - Project dependencies

## Troubleshooting

- If you can't connect to your IP camera, verify that the URL is correct and the camera is accessible from your network
- Make sure all required ports are open if you're running behind a firewall
- Check that your browser supports WebRTC (most modern browsers do)

## License

MIT License
