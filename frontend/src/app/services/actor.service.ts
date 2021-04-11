import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Actor } from '../models/actor.model';

const baseUrl = 'http://localhost:8080/api/actors';

@Injectable({
  providedIn: 'root'
})
export class ActorService {

  constructor(private http: HttpClient) { }

  getAll(): Observable<Actor[]> {
    return this.http.get<Actor[]>(baseUrl);
  }

  get(id: any): Observable<Actor> {
    return this.http.get(`${baseUrl}/${id}`);
  }

  create(data: any): Observable<any> {
    return this.http.post(baseUrl, data);
  }

  update(id: any, data: any): Observable<any> {
    return this.http.put(`${baseUrl}/${id}`, data);
  }

  delete(id: any): Observable<any> {
    return this.http.delete(`${baseUrl}/${id}`);
  }

  deleteAll(): Observable<any> {
    return this.http.delete(baseUrl);
  }

  findByFirstName(first_name: any): Observable<Actor[]> {
    return this.http.get<Actor[]>(`${baseUrl}?first_name=${first_name}`);
  }
}