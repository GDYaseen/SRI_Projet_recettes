import { Component, Input } from '@angular/core';
import { Document } from 'src/app/models/Document';

@Component({
  selector: 'app-link',
  templateUrl: './link.component.html',
  styleUrls: ['./link.component.css']
})
export class LinkComponent {

  @Input() 
  document: Document = {
    id: 0,
    title: '',
    partOfText: '',
    image: ''
  };

}
