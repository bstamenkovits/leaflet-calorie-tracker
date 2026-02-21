import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface FoodLog {
  id: number;
  meal: string;
  ingredient: string;
  quantity: string;
  unit: string;
  calories: number;
}

@Injectable({
  providedIn: 'root'
})
export class DataService {
  private readonly apiUrl = '/api';

  constructor(private http: HttpClient) {}

  getFoodLogs(): Observable<FoodLog[]> {
    return this.http.get<FoodLog[]>(`${this.apiUrl}/food-logs`);
  }
}
