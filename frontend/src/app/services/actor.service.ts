import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Actor } from '../models/actor.model';

const baseUrl2 = 'http://localhost:5000/actors';

@Injectable({
  providedIn: 'root'
})
export class ActorService {

  constructor(private http: HttpClient) { }

  getAll(): Observable<Actor[]> {
    return this.http.get<Actor[]>(baseUrl2);
  }

  get(id: any): Observable<Actor> {
    return this.http.get(`${baseUrl2}/${id}`);
  }

  create(data: any): Observable<any> {
    return this.http.post(baseUrl2, data);
  }

  update(id: any, data: any): Observable<any> {
    return this.http.put(`${baseUrl2}/${id}`, data);
  }

  delete(id: any): Observable<any> {
    return this.http.delete(`${baseUrl2}/${id}`);
  }

  deleteAll(): Observable<any> {
    return this.http.delete(baseUrl2);
  }

  findByFirstName(first_name: any): Observable<Actor[]> {
    return this.http.get<Actor[]>(`${baseUrl2}?first_name=${first_name}`);
  }
}