import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class SearchService {

  constructor(private httpClient: HttpClient) { }

  private baseUrl = "http://localhost:5009/api";

  search(searchTerm: string) {
    return this.httpClient.get(`${this.baseUrl}/search?query=${searchTerm}`);
  }
}
