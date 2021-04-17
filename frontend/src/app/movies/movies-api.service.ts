import {Injectable} from '@angular/core';
import {HttpClient, HttpErrorResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import 'rxjs/add/operator/catch';
import {API_URL} from '../env';
import {Movie} from './movie.model';

@Injectable()
export class MoviesApiService {

  constructor(private http: HttpClient) {
  }

  private static _handleError(err: HttpErrorResponse | any) {
    return Observable.throw(err.message || 'Error: Unable to complete request.');
  }

  // GET list of public, future events
  // getAllMovies(): Observable<Movie[]> {
  //   return this.http
  //     .get(`${API_URL}/movies`)
  //     .catch(MoviesApiService._handleError);
   getAllMovies(): Observable<Movie[]> {
    return this.http.get<Movie[]>(`${API_URL}/movies`)
      .catch(MoviesApiService._handleError);
  }
}
