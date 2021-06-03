import { Component, OnInit } from '@angular/core';
import { MovieService } from 'src/app/services/movie.service';
import { ActivatedRoute, Router } from '@angular/router';
import { Movie } from 'src/app/models/movie.model';
import { AuthService } from '@auth0/auth0-angular';

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
  isAssistant: boolean = false; //added as a property of component
  isDirector: boolean = false; //changed isDirector to a property of component

  constructor(
    private movieService: MovieService,
    private route: ActivatedRoute,
    private router: Router, 
    public auth0: AuthService) { }

  async ngOnInit() {
    this.message = '';
    this.getMovie(this.route.snapshot.params.id);
    this.checkRoles() ; //function whenever page loads
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

  //made function async and calls delete movie await response
  async deleteMovie() {
    try {
      //call service method and log as an error if error
      const response = await this.movieService.deleteMovie(this.currentMovie.id);
      console.log(response);
      this.router.navigate(['/movies']);
    } catch(error) {
      console.log(error);
    }
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
                  const roles: Array<string> = user["https://cast-app.herokuapp.com/roles"]; //fetch roles from user
                  console.log("checkRoles(): user roles: ", roles);
                  this.isAssistant = roles.some(elem => elem=="assistance")
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
