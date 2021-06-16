import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Actor } from '../models/actor.model';
import { AuthService } from '@auth0/auth0-angular';

const baseUrl = 'https://cast-app.herokuapp.com/actors';

@Injectable({
  providedIn: 'root'
})
export class ActorService {

  constructor(private http: HttpClient, private auth0: AuthService) { }

  getAllActors(): Observable<Actor[]> {
    return this.http.get<Actor[]>(baseUrl);
  }

  getActor(id: any): Observable<any> {
    return this.http.get(`${baseUrl}/${id}`);
  }

  addActor(data: any): Observable<any> {
    return this.http.post(baseUrl, data);
  }

  updateActor(id: any, data: any): Observable<any> {
    return this.http.patch(`${baseUrl}/${id}`, data);
  }

  publishActor(id: any): Observable<any> {
    return this.http.patch(`${baseUrl}/${id}/publish`, {});
  }

  unpublishActor(id: any): Observable<any> {
    return this.http.patch(`${baseUrl}/${id}/unpublish`, {});
  }

  deleteActor(id: any): Observable<any> {
    return this.http.delete(`${baseUrl}/${id}`);
  }

  findActorByFirstName(first_name: any): Observable<Actor[]> {
    return this.http.get<Actor[]>(`${baseUrl}/search?first_name=${first_name}`);
  }
}