import {Component, OnInit, OnDestroy} from '@angular/core';
import {Subscription} from 'rxjs/Subscription';
import {MoviesApiService} from './movies/movies-api.service';
import {Movie} from './movies/movie.model';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit, OnDestroy {
  title = 'app';
  moviesListSubs: Subscription;
  moviesList: Movie[];

  constructor(private moviesApi: MoviesApiService) {
  }

  ngOnInit() {
    this.moviesListSubs = this.moviesApi
      .getAllMovies()
      .subscribe(res => {
          this.moviesList = res;
        },
        console.error
      );
  }

  ngOnDestroy() {
    this.moviesListSubs.unsubscribe();
  }
}
