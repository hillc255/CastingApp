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
  currentMovieImg: string;
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

  get defaultPic(): string {
    return (this.currentMovie && this.currentMovieImg)?
      this.currentMovieImg:"https://i.ibb.co/6v84Gpq/no-image.png";
  }

  setDefaultPic() {
    this.currentMovieImg = null;
  }

  refreshList(): void {
    this.retrieveMovies();
    this.currentMovie = undefined;
    this.currentIndex = -1;
  }

  setActiveMovie(movie: Movie, index: number): void {
    this.currentMovieImg = null;
    
    setTimeout(()=>{
      this.currentMovieImg = (movie)? movie.movie_img: null;
      this.currentMovie = movie;
      this.currentIndex = index;
    }, 100);
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

}
