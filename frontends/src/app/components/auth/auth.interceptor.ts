// import { Injectable } from '@angular/core';
// import { HttpEvent, HttpHandler, HttpInterceptor, HttpRequest } from '@angular/common/http';

// import { Observable } from 'rxjs';
// import { AuthService } from '@auth0/auth0-angular';

// @Injectable()
// export class AuthInterceptor implements HttpInterceptor {

//   constructor(public auth: AuthService) {}

//   intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
//     req = req.clone({
//       setHeaders: {
//         'Content-Type' : 'application/json; charset=utf-8',
//         'Accept'       : 'application/json',
//         'Authorization': 'Bearer $(this.auth0.getToken()}'
//         //'Authorization': `Bearer ${AuthService.getToken()}`,
//       }
//     });

//     return next.handle(req);
//   }
// }

//import { $ } from 'protractor';
//import { AuthService } from './auth.service';

// @Injectable({
//     providedIn: 'root'
//   })
//   export class AuthInterceptorService implements HttpInterceptor {
//     constructor(private _authService: AuthService) { }
  
//     intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
//       return from (
//         this._authService.getAccessToken()
//         .then(token => {
//           const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
//           const authRequest = req.clone({ headers });
//           return next.handle(authRequest).toPromise();
//         })
//       );
//     }
//   }