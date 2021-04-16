import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Observable } from 'rxjs';
import { Movie } from '../models/movie.model';

const baseUrl = 'http://127.0.0.1:5000/movies';

@Injectable({
  providedIn: 'root'
})

export class MovieService {

  constructor(private http: HttpClient) { }

  /** GET: movies from the server */
  getAll(): Observable<Movie[]> {
    return this.http.get<Movie[]>(baseUrl);
  }

  /** GET: movie by id. Will 404 if id not found */
  get(id: any): Observable<Movie> {
    return this.http.get(`${baseUrl}/${id}`);
  }

  /** POST: add a new movie to the server */
  create(data: any): Observable<any> {
    return this.http.post(baseUrl, data);
  }

  /** PUT: update the movie to the server */
  update(id: any, data: any): Observable<any> {
    return this.http.put(`${baseUrl}/${id}`, data);
  }

  /** DELETE: delete movie from the server */
  delete(id: any): Observable<any> {
    return this.http.delete(`${baseUrl}/${id}`);
  }

  deleteAll(): Observable<any> {
    return this.http.delete(baseUrl);
  }

  findByTitle(title: any): Observable<Movie[]> {
    return this.http.get<Movie[]>(`${baseUrl}?title=${title}`);
  }
}
