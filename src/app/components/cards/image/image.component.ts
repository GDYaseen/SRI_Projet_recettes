import { Component, Input } from '@angular/core';
import { Image } from 'src/app/models/Image';

@Component({
  selector: 'app-image',
  templateUrl: './image.component.html',
  styleUrls: ['./image.component.css']
})
export class ImageComponent {

  @Input()
  image : Image = { id: 0, path: '' };
}
