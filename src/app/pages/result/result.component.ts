import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Image } from 'src/app/models/Image';
import { Result } from 'src/app/models/Result';
import { Video } from 'src/app/models/Video';
import { SearchService } from 'src/app/services/search.service';

@Component({
  selector: 'app-result',
  templateUrl: './result.component.html',
  styleUrls: ['./result.component.css']
})
export class ResultComponent {

  constructor(private searchService : SearchService, private activatedRoute : ActivatedRoute, private router : Router) { }

  query : string = '';

  fetchedData : Result = {
    documents: [],
    videos: { description: '', sources: [], time_elapsed: '' },
  }
  images : Image[] = [];

  ngOnInit() {
    this.activatedRoute.queryParams.subscribe(params => {
      this.query = params['query'];
    });
    this.searchService.search(this.query).subscribe((data : any) => {
      this.fetchedData = data;
      this.images = this.fetchedData.documents.map((document : any) => {
        return {
          id: document.id,
          path: document.image
        };
      });
  });
  }

  search(event : any) {
    const query : string = this.query.trim();
    this.router.navigate(['/results'], { queryParams: { query: query } });
  }

}
