from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastrtc import RTCPeerConnection, MediaStreamTrack, RTCConfiguration, RTCSessionDescription
from fastrtc.contrib.media import MediaPlayer
import cv2
import asyncio
from aiortc.contrib.media import MediaRelay
import json

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Replace with your IP camera URL
IP_CAMERA_URL = "http://<your_ip_camera>/video"

class VideoStreamTrack(MediaStreamTrack):
    kind = "video"

    def __init__(self, camera_url):
        super().__init__()
        self.cap = cv2.VideoCapture(camera_url)
        self.relay = MediaRelay()

    async def recv(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        
        # Convert frame to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = self.relay.frame_from_ndarray(frame)
        return frame

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/offer")
async def offer(request: Request):
    params = await request.json()
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

    pc = RTCPeerConnection(RTCConfiguration(
        iceServers=[{"urls": ["stun:stun.l.google.com:19302"]}]
    ))
    pc_id = "PeerConnection{}".format(id(pc))

    def log_info(msg, *args):
        print(pc_id + " " + msg, *args)

    @pc.on("connectionstatechange")
    async def on_connectionstatechange():
        log_info("Connection state is %s", pc.connectionState)
        if pc.connectionState == "failed":
            await pc.close()

    # Create video track
    video = VideoStreamTrack(IP_CAMERA_URL)
    pc.addTrack(video)

    # Handle offer
    await pc.setRemoteDescription(offer)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
