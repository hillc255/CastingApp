import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpErrorResponse, HttpEvent, HttpInterceptor, HttpHandler, HttpRequest } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthService } from './services/auth.service';
import { from } from 'rxjs'
import { Auth0Client } from '@auth0/auth0-spa-js';


@Injectable()
export class TokenInterceptor implements HttpInterceptor {

  constructor(
    private http: HttpClient,
    private authService: AuthService
  ) { }

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const modifiedReq = request.clone({ 
      headers: request.headers.set('Authorization', `Bearer ${this.authService.accessToken}`),
    });
    return next.handle(modifiedReq);
  }
}