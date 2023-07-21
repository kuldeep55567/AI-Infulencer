import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private baseUrl = 'http://127.0.0.1:5000'; 
  constructor(private http: HttpClient) {}
  signup(name: string, email: string, password: string) {
    return this.http.post<any>(`${this.baseUrl}/signup`, { name, email, password });
  }

  login(email: string, password: string) {
    return this.http.post<any>(`${this.baseUrl}/login`, { email, password });
  }
  getToken(): string | null {
    return localStorage.getItem('token');
  }
}
