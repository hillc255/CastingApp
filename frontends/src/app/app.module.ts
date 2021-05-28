import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import { MoviesListComponent } from './components/movies-list/movies-list.component';
import { MovieDetailsComponent } from './components/movie-details/movie-details.component';
import { AddMovieComponent } from './components/add-movie/add-movie.component';

import { ActorsListComponent } from './components/actors-list/actors-list.component';
import { ActorDetailsComponent } from './components/actor-details/actor-details.component';
import { AddActorComponent } from './components/add-actor/add-actor.component';

// Import the module from the SDK
import { AuthModule } from '@auth0/auth0-angular';
import { AuthButtonComponent } from './components/auth/auth.component';


@NgModule({
  declarations: [
    AppComponent,
    AddMovieComponent,
    MovieDetailsComponent,
    MoviesListComponent,
    AddActorComponent,
    ActorDetailsComponent,
    ActorsListComponent,
    AuthButtonComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule,
    // Import the module into the application, with configuration
    AuthModule.forRoot({
      domain: 'autumn-voice-0666.us.auth0.com',
      clientId: 'f7ZLU2DmWeRcLuikyEKjqk0893KA2Mbj'
    }),

  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
