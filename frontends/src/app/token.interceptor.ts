import { Injectable } from '@angular/core';
import { HttpEvent, HttpInterceptor, HttpHandler, HttpRequest } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthService } from './services/auth.service';
//import { AuthService } from '@auth0/auth0-angular';


@Injectable()
export class TokenInterceptor implements HttpInterceptor {

  constructor(public auth: AuthService) {}

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {

//  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    //const userToken = 'secure-user-token';
    //const userToken = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkJpc1RBYmdXS1YtXzEyeXpkNE1PVSJ9.eyJodHRwczovL2Nhc3QtYXBwLmhlcm9rdWFwcC5jb20vcm9sZXMiOlsiZGlyZWN0b3IiXSwiaXNzIjoiaHR0cHM6Ly9hdXR1bW4tdm9pY2UtMDY2Ni51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjBiMTI2NDg5MjNmZTIwMDZmMDgwOWZlIiwiYXVkIjpbImh0dHBzOi8vY2FzdC1hcHAuaGVyb2t1YXBwLmNvbS9hcGkiLCJodHRwczovL2F1dHVtbi12b2ljZS0wNjY2LnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2MjI5NDM5MjIsImV4cCI6MTYyMzAzMDMyMiwiYXpwIjoiZjdaTFUyRG1XZVJjTHVpa3lFS2pxazA4OTNLQTJNYmoiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.f5f0kQxp7DVB-Jx2MPphfBt8v93JQooZJbkG6y9UvnECIuetW1cJqNzgGljW1E_gOrbHTRK12iFGDBq66YPpMQ97U1XqGSyJTtYykXj2NH95ELqx0CQbSnbLd6S-_hMroZGdkAu_nIKjJubkAVomORtVKB-WUu55p6uOpXne5wmUIJ8Qb7O6_jdHqVOTCWTeYgy8-fTg2D4rCZyNwNgRse9FoMQw7JoUO_Ce7I-Eb6bPjXB_f9ijL7obJ_7hRDmIu9G1rb3kFsNesKChPJvAZPB0lGLe-PWrb6kaF9nYa61L_WdlWy9qfgf491SHXac6Ks-BUyfvWsyJocaQKQRp3g';
    ////const userToken = this.token.getToken();
    ////const userToken = this.auth.accessToken;

    const accessToken = 'secure-token';


    const modifiedReq = request.clone({ 
      headers: request.headers.set('Authorization', `Bearer ${accessToken}`),
    });
    return next.handle(modifiedReq);

    // request = request.clone({
    //   setHeaders: {
    //     Authorization: `Bearer ${this.auth.getToken()}`
    //   }
    // });
    // return next.handle(request);

  } 
}