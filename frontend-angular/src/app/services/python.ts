import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { firstValueFrom } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class Python {

  private http = inject(HttpClient);
  private readonly url: string = 'http://localhost:8000';

  constructor() {}

  public helloworld(): Promise<string> {
    return firstValueFrom(this.http.get<string>(`${this.url}`));
  }

  public sendVideo(file: File): Promise<string> {
    const formData = new FormData();
    formData.append('video', file);
    return firstValueFrom(this.http.post<string>(`${this.url}/transcribe`, formData));
  }
}
