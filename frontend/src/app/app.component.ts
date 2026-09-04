import { CommonModule } from '@angular/common';
import { HttpClient, provideHttpClient } from '@angular/common/http';
import { Component, inject } from '@angular/core';
import { FormControl, ReactiveFormsModule, Validators } from '@angular/forms';
import { firstValueFrom } from 'rxjs';

interface ExtractResponse {
  platform: string;
  url: string;
  description: string;
}

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  // providers: [provideHttpClient()],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
})
export class AppComponent {
  private readonly http = inject(HttpClient);
  readonly url = new FormControl('', { nonNullable: true, validators: [Validators.required] });
  result: ExtractResponse | null = null;
  loading = false;
  error = '';
  copied = false;

  async extract(): Promise<void> {
    if (this.url.invalid) {
      this.url.markAsTouched();
      return;
    }
    this.loading = true;
    this.error = '';
    this.result = null;
    this.copied = false;
    try {
      this.result = await firstValueFrom(
        this.http.post<ExtractResponse>('http://localhost:8000/api/extract', { url: this.url.value }),
      );
    } catch (error: any) {
      this.error = error?.error?.detail ?? 'Something went wrong while extracting the description.';
    } finally {
      this.loading = false;
    }
  }

  async copyDescription(): Promise<void> {
    if (!this.result) return;
    await navigator.clipboard.writeText(this.result.description);
    this.copied = true;
  }
}
