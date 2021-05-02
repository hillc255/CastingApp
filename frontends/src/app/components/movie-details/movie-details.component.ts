import { Component, OnInit } from '@angular/core';
import { MovieService } from 'src/app/services/movie.service';
import { ActivatedRoute, Router } from '@angular/router';
import { Movie } from 'src/app/models/movie.model';

@Component({
  selector: 'app-movie-details',
  templateUrl: './movie-details.component.html',
  styleUrls: ['./movie-details.component.css']
})
export class MovieDetailsComponent implements OnInit {
  currentMovie: Movie = {
    title: '',
    release_date: '',
    movie_img: '',
    movie_publish: false
  };
  message = '';

  constructor(
    private movieService: MovieService,
    private route: ActivatedRoute,
    private router: Router) { }

  ngOnInit(): void {
    this.message = '';
    this.getMovie(this.route.snapshot.params.id);
  }

  getMovie(id: string): void {
    this.movieService.getMovie(id)
      .subscribe(
        data => {
          if(data && data.success === true) {
            this.currentMovie = data.movie;
            console.log(`getMovie(${id}): returned movie`, this.currentMovie);
          } else {
            console.error(`getMovie(${id}) failed`, data);
          }
        },
        error => {
          console.error(`getMovie(${id})`, error);
        });
  }

  publishMovie(): void {
    this.movieService.publishMovie(this.currentMovie.id)
      .subscribe(
        response => {
          this.getMovie(this.route.snapshot.params.id);
        },
        error => {
          console.log(error);
        });
  }

  unpublishMovie(): void {
    this.movieService.unpublishMovie(this.currentMovie.id)
      .subscribe(
        response => {
          this.getMovie(this.route.snapshot.params.id);
        },
        error => {
          console.log(error);
        });
  }

  updateMovie(): void {
    this.movieService.updateMovie(this.currentMovie.id, this.currentMovie)
      .subscribe(
        response => {
          console.log(response);
          this.message = (response.success)?"Movie updated successfully!":"Movie update unsuccessful";
        },
        error => {
          console.log(error);
          this.message = "Movie update unsuccessful";
        });
  }

  deleteMovie(): void {
    this.movieService.deleteMovie(this.currentMovie.id)
      .subscribe(
        response => {
          console.log(response);
          this.router.navigate(['/movies']);
        },
        error => {
          console.log(error);
        });
  }

}
