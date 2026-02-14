import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

interface StatusResponse {
  status: string;
}

@Injectable({
  providedIn: 'root'
})
export class BackendService {
  private readonly apiUrl = '/api';

  constructor(private http: HttpClient) {}

  getStatus(): Observable<StatusResponse> {
    return this.http.get<StatusResponse>(`${this.apiUrl}/status`);
  }
}
