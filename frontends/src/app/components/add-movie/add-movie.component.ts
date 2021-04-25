import { Component, OnInit } from '@angular/core';
import { Movie } from 'src/app/models/movie.model';
import { MovieService } from 'src/app/services/movie.service';

@Component({
  selector: 'app-add-movie',
  templateUrl: './add-movie.component.html',
  styleUrls: ['./add-movie.component.css']
})
export class AddMovieComponent implements OnInit {
  movie: Movie = {
    title: '',
    release_date: '',
    movie_img: '',
    movie_publish: false
  };
  submitted = false;

  constructor(private movieService: MovieService) { }

  ngOnInit(): void {
  }

  saveMovie(): void {
    const data = {
      title: this.movie.title,
      release_date: this.movie.release_date,
      movie_img: this.movie.movie_img
    };

    this.movieService.addMovie(data)
      .subscribe(
        response => {
          console.log(response);
          this.submitted = true;
        },
        error => {
          console.log(error);
        });
  }

  newMovie(): void {
    this.submitted = false;
    this.movie = {
      title: '',
      release_date: '',
      movie_img: '',
      movie_publish: false
    };
  }

}
