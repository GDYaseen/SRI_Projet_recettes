import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class DetailService {

  private baseUrl = "http://localhost:5009/api";
  constructor(private httpClient: HttpClient) { }


  getDetail(id: number) {
    return this.httpClient.get(`${this.baseUrl}/details/${id}`);
  }

  
}
