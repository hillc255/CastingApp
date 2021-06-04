import { Injectable } from '@angular/core';
import { HttpHeaders, HttpClient, HttpParams } from '@angular/common/http';
import { AuthService } from '@auth0/auth0-angular';

const baseUrl = 'https://cast-app.herokuapp.com';

//https://auth0.com/blog/using-python-flask-and-angular-to-build-modern-web-apps-part-3/#Handling-Authorization-Through-Roles
@Injectable()
export class ApiService {

  constructor(private http: HttpClient, private auth0: AuthService) {}

  //   deleteMovie(id: number) {
  //   const httpOptions = {
  //     headers: new HttpHeaders({
  //       'Authorization': 'Bearer $(this.auth.getToken()}'
  //       //'Authorization': `Bearer ${Auth0.getAccessToken()}`
  //     })
  //   };
  //   return this.http
  //     .delete(`${baseUrl}/movies/${id}`, httpOptions);
  // }

  async deleteMovie(id: number) {
    const accessToken = await this.auth0.getAccessTokenSilently().toPromise();
    //const accessToken = await this.auth0.getAccessTokenSilently().toPromise();
    const httpOptions = {
      headers: new HttpHeaders({
        'Authorization': 'Bearer $(this.auth0.getToken()}'
        //'Authorization': `Bearer ${accessToken}`
        //'Authorization': `Bearer ${Auth0.getAccessToken()}`
      })
    };
    return this.http
      .delete(`${baseUrl}/movies/${id}`, httpOptions);
  }
}