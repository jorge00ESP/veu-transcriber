import { Component, signal, OnDestroy } from '@angular/core';
import { Python } from './services/python';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [],
  templateUrl: './app.html',
  styleUrls: ['./app.scss']
})
export class App implements OnDestroy {

  videoUrl = signal<string | null>(null);
  videoName = signal<string>('');
  isVideoSelected = signal(false);
  isProcessing = signal(false);
  transcription = signal<string | null>(null);
  copied = signal(false);

  private selectedFile: File | null = null;

  constructor(private pythonService: Python) {}

  ngOnDestroy(): void {
    const videoUrl = this.videoUrl();
    if (videoUrl) {
      try { URL.revokeObjectURL(videoUrl); } catch {}
    }
  }

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files == null || input.files.length === 0) return;

    const file = input.files[0];
    if (!file.type.startsWith('video/')) {
      window.alert('Please select a video file');
      return;
    }

    URL.revokeObjectURL(this.videoUrl() ?? '');

    this.selectedFile = file;
    this.videoUrl.set(URL.createObjectURL(file));
    this.videoName.set(file.name);
    this.isVideoSelected.set(true);
    this.transcription.set(null);
  }

  public serviceFile(): void {
    if (!this.selectedFile) return;

    this.isProcessing.set(true);
    this.transcription.set(null);

    this.pythonService.sendVideo(this.selectedFile)
      .then((response: any) => {
        console.log('Transcription received:', response);
        this.transcription.set(response.text);
      })
      .catch((error) => {
        console.error('Error calling Python service:', error);
        window.alert('Error processing video. Make sure the backend is running.');
      })
      .finally(() => {
        this.isProcessing.set(false);
      });
  }

  public clearVideo(): void {
    URL.revokeObjectURL(this.videoUrl() ?? '');
    this.selectedFile = null;
    this.videoUrl.set(null);
    this.videoName.set('');
    this.isVideoSelected.set(false);
    this.transcription.set(null);
  }

  public copyTranscription(): void {
    const text = this.transcription();
    if (!text) return;
    navigator.clipboard.writeText(text).then(() => {
      this.copied.set(true);
      setTimeout(() => this.copied.set(false), 2000);
    });
  }
}
