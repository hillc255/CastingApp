import { Component, OnInit } from '@angular/core';
import { Movie } from 'src/app/models/movie.model';
import { MovieService } from 'src/app/services/movie.service';
import { AuthService } from '@auth0/auth0-angular';
import { environment } from 'src/environments/environment';

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
  isDirector: boolean = false; //isDirector is a property of component

  constructor(
    private movieService: MovieService,
    public auth0: AuthService) { }

  async ngOnInit() {
    this.checkRoles() ; //function whenever page loads
  }

  saveMovie(form: any): void {
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

  //method called after component loads to check the roles
  checkRoles() {
    console.log('checkRoles()');
    this.auth0.isAuthenticated$  //observable which returns the authenticated status
      .subscribe(
        isAuthenticated=>{
          if(isAuthenticated) {  //if authenticated then gets the user
            console.log('checkRoles(): authenticated getting user');
            this.auth0.user$  //observable which returns the user
              .subscribe(
                user=>{  // returns the user
                  console.log('checkRoles(): user', user);
                  const roles: Array<string> = user[ environment.userRole ]; //fetch roles from user
                  console.log("checkRoles(): user roles: ", roles);
                  this.isDirector = roles.some(elem => elem=="director")
                },
                err=>{
                  console.log('checkRoles(): error getting user', err);
                }
              );
          } else {
            console.log('checkRoles(): not authenticated ');
          }
        },
        err=>{
          console.log('checkRoles(): error getting authentication status', err);
        }
      );
  }

}
