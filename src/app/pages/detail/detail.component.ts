import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Detail } from 'src/app/models/Detail';
import { DetailService } from 'src/app/services/detail.service';

@Component({
  selector: 'app-detail',
  templateUrl: './detail.component.html',
  styleUrls: ['./detail.component.css']
})
export class DetailComponent {

  constructor(private detailService : DetailService, private activatedRoute : ActivatedRoute, private router : Router) { }
    
  post : Detail = {
    id: 0,
    title: '',
    text: '',
    image: ''
  }
  
  ngOnInit() {
    this.activatedRoute.queryParams.subscribe(params => {
      this.post.id = params['id'];
      this.detailService.getDetail(this.post.id ?? 0).subscribe((data : any) => {
        this.post.title = data.title;
        this.post.text = data.text;
        this.post.image = data.image;
      })
    });
  }

}
