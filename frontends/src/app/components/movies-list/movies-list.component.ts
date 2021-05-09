import { Component, OnInit } from '@angular/core';
import { Movie } from 'src/app/models/movie.model';
import { MovieService } from 'src/app/services/movie.service';


@Component({
  selector: 'app-movies-list',
  templateUrl: './movies-list.component.html',
  styleUrls: ['./movies-list.component.css']
})
export class MoviesListComponent implements OnInit {
  movies?: Movie[];
  currentMovie?: Movie;
  currentIndex = -1;
  title = '';

  constructor(private movieService: MovieService) { }

  ngOnInit(): void {
    this.retrieveMovies();
  }

  retrieveMovies(): void {
    this.movieService.getAllMovies()
      .subscribe(
        data => {
          this.movies = data;
          console.log(data);
        },
        error => {
          console.log(error);
        });
  }

  setDefaultPic() {
    this.currentMovie.movie_img = "https://i.ibb.co/6v84Gpq/no-image.png";
  }

  refreshList(): void {
    this.retrieveMovies();
    this.currentMovie = undefined;
    this.currentIndex = -1;
  }

  setActiveMovie(movie: Movie, index: number): void {
    this.currentMovie = movie;
    this.currentIndex = index;
  }

  searchTitle(): void {
    this.currentMovie = undefined;
    this.currentIndex = -1;

    this.movieService.findMovieByTitle(this.title)
      .subscribe(
        data => {
          this.movies = data;
          console.log(data);
        },
        error => {
          console.log(error);
        });
  }

  get currentMovieReleaseDate(): Date {
    console.log('this.currentMovie.release_date', this.currentMovie.release_date)
    return new Date(this.currentMovie.release_date);
  }
}
