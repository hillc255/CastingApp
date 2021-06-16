import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Movie } from '../models/movie.model';
import { AuthService } from '@auth0/auth0-angular';

const baseUrl = 'https://cast-app.herokuapp.com/movies';

@Injectable({
  providedIn: 'root'
})
export class MovieService {

  constructor(private http: HttpClient, private auth0: AuthService) { }

  getAllMovies(): Observable<Movie[]> {
    return this.http.get<Movie[]>(baseUrl);
  }

  getMovie(id: any): Observable<any> {
    return this.http.get(`${baseUrl}/${id}`);
  }

  addMovie(data: any): Observable<any> {
    return this.http.post(baseUrl, data);
  }

  updateMovie(id: any, data: any): Observable<any> {
    return this.http.patch(`${baseUrl}/${id}`, data);
  }

  publishMovie(id: any): Observable<any> {
    return this.http.patch(`${baseUrl}/${id}/publish`, {});
  }

  unpublishMovie(id: any): Observable<any> {
    return this.http.patch(`${baseUrl}/${id}/unpublish`, {});
  }

  deleteMovie(id: any): Observable<any> {
    return this.http.delete(`${baseUrl}/${id}`);
  }

  findMovieByTitle(title: any): Observable<Movie[]> {
    return this.http.get<Movie[]>(`${baseUrl}/search?title=${title}`);
  }

}