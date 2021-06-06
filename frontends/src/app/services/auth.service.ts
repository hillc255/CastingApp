import { Injectable } from '@angular/core';
import { tokenNotExpired } from 'angular2-jwt';
//import decode from 'jwt-decode';
import * as auth0 from 'auth0-js';
//import * as Auth0 from 'auth0-web';


@Injectable()
export class AuthService {
  public getToken(): string {
    return localStorage.getItem('token');
  }
  public isAuthenticated(): boolean {
    // get the token
    const token = this.getToken();
    // return a boolean reflecting 
    // whether or not the token is expired
    return tokenNotExpired(null, token);
  }
}