import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

//https://auth0.com/docs/quickstart/spa/angular/02-calling-an-api

import { FormsModule } from '@angular/forms';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
// Import the HTTP interceptor from the Auth0 Angular SDK
import { AuthHttpInterceptor, HttpMethod } from '@auth0/auth0-angular';
//import { AuthInterceptor } from './components/auth/auth.interceptor';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import { MoviesListComponent } from './components/movies-list/movies-list.component';
import { MovieDetailsComponent } from './components/movie-details/movie-details.component';
import { AddMovieComponent } from './components/add-movie/add-movie.component';

import { ActorsListComponent } from './components/actors-list/actors-list.component';
import { ActorDetailsComponent } from './components/actor-details/actor-details.component';
import { AddActorComponent } from './components/add-actor/add-actor.component';

// Import the module from the SDK and ApiService
import { AuthModule } from '@auth0/auth0-angular';
import { AuthButtonComponent } from './components/auth/auth.component';
import{ UserProfileComponent }  from './components/profile/profile.component';
//import {ApiService} from './services/api.service';


@NgModule({
  declarations: [
    AppComponent,
    AddMovieComponent,
    MovieDetailsComponent,
    MoviesListComponent,
    AddActorComponent,
    ActorDetailsComponent,
    ActorsListComponent,
    AuthButtonComponent,
    UserProfileComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule,
    // Import the module into the application, with configuration
    AuthModule.forRoot({
      domain: 'autumn-voice-0666.us.auth0.com',
      clientId: 'f7ZLU2DmWeRcLuikyEKjqk0893KA2Mbj',
      httpInterceptor: {
        allowedList: [
          '/*',
          {
            uri:'/movies/*',
            httpMethod: HttpMethod.Delete,
            allowAnonymous: true,
            tokenOptions: {
              scope: 'openid'
            }
          },
          {
            uri: 'http://localhost:8081/movies/*'
          }
        ]
      }
    }),
  ],
  providers: [
    {
      provide : HTTP_INTERCEPTORS,
      useClass: AuthHttpInterceptor,
      multi   : true,
    }
  ],

  bootstrap: [AppComponent]
})
export class AppModule {
  constructor() {
 }
}