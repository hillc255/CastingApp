import { Component, OnInit } from '@angular/core';
import { Movie } from 'src/app/models/movie.model';
import { MovieService } from 'src/app/services/movie.service';
import { AuthService } from '@auth0/auth0-angular';
import { environment } from 'src/environments/environment';

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
  isAssistant: boolean = false; //added as a property of component
  isDirector: boolean = false; //added as a property of component

  constructor(
    private movieService: MovieService,
    public auth0: AuthService) { }

  async ngOnInit() {
    this.retrieveMovies();
    this.checkRoles() ; //function whenever page loads
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
                  this.isAssistant = roles.some(elem => elem=="assistant")
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
