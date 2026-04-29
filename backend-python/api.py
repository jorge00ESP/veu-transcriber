import sys
import os
import shutil
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import torch
import torchvision
import argparse
from lightning import ModelModule
from datamodule.transforms import AudioTransform, VideoTransform

sys.path.insert(0, "./")

class InferencePipeline(torch.nn.Module):
    def __init__(self, args, ckpt_path, detector="mediapipe"):
        super(InferencePipeline, self).__init__()
        self.modality = args.modality
        if self.modality == "video":
            from preparation.detectors.mediapipe.detector import LandmarksDetector
            from preparation.detectors.mediapipe.video_process import VideoProcess
            self.landmarks_detector = LandmarksDetector()
            self.video_process = VideoProcess(convert_gray=False)
            self.video_transform = VideoTransform(subset="test")

        ckpt = torch.load(ckpt_path, map_location=lambda storage, loc: storage)
        self.modelmodule = ModelModule(args)
        self.modelmodule.model.load_state_dict(ckpt)
        self.modelmodule.eval()

    # --- AQUÍ ESTÁ EL ARREGLO DE OPENCV ---
    def load_video(self, data_filename):
        import cv2
        import numpy as np
        
        cap = cv2.VideoCapture(data_filename)
        frames =[]
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(frame_rgb)
            
        cap.release()
        return np.array(frames)
    # -------------------------------------

    def forward(self, data_filename):
        data_filename = os.path.abspath(data_filename)
        video = self.load_video(data_filename)
        landmarks = self.landmarks_detector(video)
        video = self.video_process(video, landmarks)
        video = torch.tensor(video)
        video = video.permute((0, 3, 1, 2))
        video = self.video_transform(video)
        with torch.no_grad():
            transcript = self.modelmodule(video)
        return transcript

app = FastAPI(title="Lip Reading API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("⏳ Cargando el modelo...")
model_path = "vsr_trlrs2lrs3vox2avsp_base.pth"
parser = argparse.ArgumentParser()
args, _ = parser.parse_known_args(args=[])
setattr(args, 'modality', 'video')
pipeline = InferencePipeline(args, model_path, detector="mediapipe")
print("✅ ¡Modelo cargado y listo!")

@app.get("/")
async def root():
    return {"message": "Hello World! El backend de Andrei está dockerizado y funcionando."}

@app.post("/transcribe")
async def transcribe_video(video: UploadFile = File(...)):
    temp_video_path = f"temp_{video.filename}"
    with open(temp_video_path, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)
    
    try:
        transcript = pipeline(temp_video_path)
        resultado_texto = str(transcript[0] if isinstance(transcript, list) else transcript)
        os.remove(temp_video_path)
        return {"success": True, "text": resultado_texto}
    except Exception as e:
        if os.path.exists(temp_video_path):
            os.remove(temp_video_path)
        return {"success": False, "error": str(e)}