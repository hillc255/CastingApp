import { Injectable } from '@angular/core';
import { HttpClient, HttpEvent, HttpInterceptor, HttpHandler, HttpRequest } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthService } from './services/auth.service';

@Injectable()
export class TokenInterceptor implements HttpInterceptor {

  constructor(
    private http: HttpClient,
    private authService: AuthService
  ) { }

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    console.log("Token interceptor", this.authService)
    const modifiedReq = request.clone({ 
      headers: request.headers.set('Authorization', `Bearer ${this.authService.accessToken}`),
    });
    return next.handle(modifiedReq);
  }
}