import { Component } from '@angular/core';
import { environment } from '../environments/environment';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  //added constructor for production which logs false for default environment
  constructor() {
    console.log(environment.production);
  }
  title = 'Movie-Robots';
}
