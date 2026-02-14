import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { BackendService } from './services/backend.service';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('Leaflet Calorie Tracker');
  protected readonly statusMessage = signal<string>('');

  constructor(private backendService: BackendService) {}

  checkBackendHealth() {
    console.log('Checking backend API health...');
    this.statusMessage.set('Checking...');

    this.backendService.getStatus().subscribe({
      next: (response) => {
        console.log('Backend API status:', response.status);
        this.statusMessage.set(`Backend status: ${response.status}`);
      },
      error: (error) => {
        console.error('Error checking backend:', error);
        this.statusMessage.set('Error: Could not connect to backend');
      }
    });
  }
}
