import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { BackendService } from './services/backend.service';
import { DataService, FoodLog } from './services/data.service';


@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('Leaflet Calorie Tracker');
  protected readonly statusMessage = signal<string>('');
  protected readonly foodLogs = signal<FoodLog[]>([]);
  protected readonly foodLogsMessage = signal<string>('');

  constructor(
    private backendService: BackendService,
    private dataService: DataService
  ) {}

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

  getFoodLogs() {
    console.log('Fetching food logs...');
    this.foodLogsMessage.set('Loading...');

    this.dataService.getFoodLogs().subscribe({
      next: (logs) => {
        console.log('Food logs retrieved:', logs);
        this.foodLogs.set(logs);
        this.foodLogsMessage.set(`Retrieved ${logs.length} food log(s)`);
      },
      error: (error) => {
        console.error('Error fetching food logs:', error);
        this.foodLogsMessage.set('Error: Could not retrieve food logs');
      }
    });
  }
}
