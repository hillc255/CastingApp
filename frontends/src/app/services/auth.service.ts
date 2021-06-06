import { Injectable } from '@angular/core';
//import { tokenNotExpired } from 'angular2-jwt';
//import decode from 'jwt-decode';
import * as auth0 from 'auth0-js';
//import * as Auth0 from 'auth0-web';
import {JwtHelperService} from '@auth0/angular-jwt';

const helper = new JwtHelperService();

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
    return helper.isTokenExpired(token);
  }
}

  // export class AuthService {
  //   authToken : any;
  //   constructor(private http: HttpClient, private jwtHelper: JwtHelperService) { }
  //   loadToken(){
  //       const token = localStorage.getItem('id_token');
  //       this.authToken = token;
  //       return this.authToken;
  //   }
  //   // Check if the token is Valid
  //   loggedIn(){
  //       this.authToken = this.loadToken();
  //       console.log(this.jwtHelper.isTokenExpired(this.authToken));
  // export class AuthService {
    // authToken : any;
    // constructor(private http: HttpClient, private jwtHelper: JwtHelperService) { }
    // loadToken(){
    //     const token = localStorage.getItem('id_token');
    //     this.authToken = token;
    //     return this.authToken;
    // }
    // // Check if the token is Valid
    // loggedIn(){
    //     this.authToken = this.loadToken();
    //     console.log(this.jwtHelper.isTokenExpired(this.authToken));
    //     return this.jwtHelper.isTokenExpired(this.authToken);
    // }
  //   }