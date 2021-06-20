import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { environment } from '../environments/environment';

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
    // import the module into the application, with environment configuration
    AuthModule.forRoot({
      domain: environment.auth.domain,
      clientId: environment.auth.clientID,
      audience: environment.auth.audience,
      scope: 'openid',
      httpInterceptor: {
        allowedList: [
          {
            uri: environment.auth.uri,
            tokenOptions: {
              audience: environment.auth.audience,
              scope: environment.auth.scope,
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

  apiEndPoint:string="";
  domain:string="";
  clientID:string="";
  audience:string="";
  redirect:string="";
  scope:string="";
  uri:string="";

  constructor() {
    this.apiEndPoint = environment.apiEndPoint;
    this.domain = environment.auth.domain;
    this.clientID = environment.auth.clientID;
    this.audience = environment.auth.audience;
    this.redirect = environment.auth.redirect;
    this.scope = environment.auth.scope;
    this.uri = environment.auth.uri;
 }
}