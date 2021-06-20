import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

//source: https://auth0.com/docs/quickstart/spa/angular/02-calling-an-api

import { FormsModule } from '@angular/forms';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import { MoviesListComponent } from './components/movies-list/movies-list.component';
import { MovieDetailsComponent } from './components/movie-details/movie-details.component';
import { AddMovieComponent } from './components/add-movie/add-movie.component';

import { ActorsListComponent } from './components/actors-list/actors-list.component';
import { ActorDetailsComponent } from './components/actor-details/actor-details.component';
import { AddActorComponent } from './components/add-actor/add-actor.component';

// import the module from the SDK and ApiService
import { AuthModule } from '@auth0/auth0-angular';
import { AuthButtonComponent } from './components/auth/auth.component';
import{ UserProfileComponent }  from './components/profile/profile.component';
// import headers from tokens
import{ TokenInterceptor } from './token.interceptor';
import { AuthService } from './services/auth.service';

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
    UserProfileComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule,
    // import the module into the application, with configuration
    AuthModule.forRoot({
      domain: 'autumn-voice-0666.us.auth0.com',
      clientId: 'f7ZLU2DmWeRcLuikyEKjqk0893KA2Mbj',
      audience: 'https://cast-app.herokuapp.com/api',
      //responseType: 'token',
      scope: 'openid',
      httpInterceptor: {
        allowedList: [
          {
            uri: 'https://cast-app.herokuapp.com/*',
            tokenOptions: {
              audience: 'https://cast-app.herokuapp.com/api/',
              scope: 'openid profile email',
            }
          }
        ]
      }
    }),
  ],
  providers: [
    AuthService,
    {
      //get headers and access token
      provide: HTTP_INTERCEPTORS, 
      useClass: TokenInterceptor, 
      multi: true 
    }
  ],

  bootstrap: [AppComponent]
})
export class AppModule {
  constructor() {
 }
}