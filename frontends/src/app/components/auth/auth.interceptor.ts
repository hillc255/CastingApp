// import { Injectable } from '@angular/core';
// import { HttpEvent, HttpHandler, HttpInterceptor, HttpRequest } from '@angular/common/http';

// //import { Observable } from 'rxjs/Observable';  //old format
// import { Observable } from 'rxjs';
// import { AuthService } from '@auth0/auth0-angular';
// //import { $ } from 'protractor';
// //import { AuthService } from './auth.service';

// @Injectable()
// export class AuthInterceptor implements HttpInterceptor {

//   constructor(public auth: AuthService) {}

//   intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
//     req = req.clone({
//       setHeaders: {
//         'Content-Type' : 'application/json; charset=utf-8',
//         'Accept'       : 'application/json',
//         'Authorization': 'Bearer $(this.auth.getToken()}'
//         //'Authorization': `Bearer ${AuthService.getToken()}`,
//       }
//     });

//     return next.handle(req);
//   }
// }