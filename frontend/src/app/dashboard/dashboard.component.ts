import { Component, OnInit } from '@angular/core';
import { AuthService } from 'auth.service';
import { HttpClient,HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  queries: any[] = [];

  constructor(private authService: AuthService, private http: HttpClient) {}

  ngOnInit(): void {
    this.fetchQueries();
  }

  fetchQueries() {
    const apiUrl = 'http://127.0.0.1:5000/queries';
    const token = this.authService.getToken();
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    });
  
    this.http.get(apiUrl, { headers }).subscribe(
      (data:any) => {
        this.queries = data;
      },
      (error) => {
        console.error('Error fetching user queries:', error);
      }
    );
  }
}