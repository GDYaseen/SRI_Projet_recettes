import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {

  query : string = '';

  constructor(private router : Router) { }

  search(event : any) {
    const query : string = this.query.trim();
    this.router.navigate(['/results'], { queryParams: { query: query } });
  }

}
