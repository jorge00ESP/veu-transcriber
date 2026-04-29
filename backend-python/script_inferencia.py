import sys
import os

sys.path.insert(0, "./")

import torch
import torchaudio
import torchvision
import argparse
from lightning import ModelModule
from datamodule.transforms import AudioTransform, VideoTransform

class InferencePipeline(torch.nn.Module):
    def __init__(self, args, ckpt_path, detector="mediapipe"):
        super(InferencePipeline, self).__init__()
        self.modality = args.modality
        if self.modality == "audio":
            self.audio_transform = AudioTransform(subset="test")
        elif self.modality == "video":
            if detector == "mediapipe":
                from preparation.detectors.mediapipe.detector import LandmarksDetector
                from preparation.detectors.mediapipe.video_process import VideoProcess
                self.landmarks_detector = LandmarksDetector()
                self.video_process = VideoProcess(convert_gray=False)
            elif detector == "retinaface":
                from preparation.detectors.retinaface.detector import LandmarksDetector
                from preparation.detectors.retinaface.video_process import VideoProcess
                self.landmarks_detector = LandmarksDetector(device="cuda:0")
                self.video_process = VideoProcess(convert_gray=False)
            self.video_transform = VideoTransform(subset="test")

        ckpt = torch.load(ckpt_path, map_location=lambda storage, loc: storage)
        self.modelmodule = ModelModule(args)
        self.modelmodule.model.load_state_dict(ckpt)
        self.modelmodule.eval()

    def load_video(self, data_filename):
        import cv2
        import numpy as np
        cap = cv2.VideoCapture(data_filename)
        frames = []
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(frame)
        cap.release()
        return np.array(frames)

    def forward(self, data_filename):
        data_filename = os.path.abspath(data_filename)
        assert os.path.isfile(data_filename), f"El archivo: {data_filename} no existe."

        if self.modality == "video":
            video = self.load_video(data_filename)
            landmarks = self.landmarks_detector(video)
            video = self.video_process(video, landmarks)
            video = torch.tensor(video)
            video = video.permute((0, 3, 1, 2))
            video = self.video_transform(video)
            with torch.no_grad():
                transcript = self.modelmodule(video)

        return transcript

# ==========================================
# CONFIGURACIÓN DEL MVP
# ==========================================
model_path = "vsr_trlrs2lrs3vox2avsp_base.pth"
video_path = "../english_video.mp4" 

if __name__ == "__main__":
    print("⚙️ Iniciando el motor de Lectura de Labios con IA...")
    
    parser = argparse.ArgumentParser()
    args, _ = parser.parse_known_args(args=[])
    setattr(args, 'modality', 'video')

    pipeline = InferencePipeline(args, model_path, detector="mediapipe")

    print(f"🎥 Analizando los labios en el vídeo: {video_path}")
    print("⏳ Por favor, espera. Esto puede tardar unos segundos...")
    
    transcript = pipeline(video_path)

    print("\n" + "="*50)
    print("✅ TRANSCRIPCIÓN DETECTADA (SOLO VIDEO):")
    print("🗣️  " + str(transcript[0] if isinstance(transcript, list) else transcript))
    print("="*50 + "\n")