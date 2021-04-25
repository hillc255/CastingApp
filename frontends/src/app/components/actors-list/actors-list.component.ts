import { Component, OnInit } from '@angular/core';
import { Actor } from 'src/app/models/actor.model';
import { ActorService } from 'src/app/services/actor.service';

@Component({
  selector: 'app-actors-list',
  templateUrl: './actors-list.component.html',
  styleUrls: ['./actors-list.component.css']
})
export class ActorsListComponent implements OnInit {
  actors?: Actor[];
  currentActor?: Actor;
  currentIndex = -1;
  first_name = '';

  constructor(private actorService: ActorService) { }

  ngOnInit(): void {
    this.retrieveActors();
  }

  retrieveActors(): void {
    this.actorService.getAll()
      .subscribe(
        data => {
          this.actors = data;
          console.log(data);
        },
        error => {
          console.log(error);
        });
  }

  refreshList(): void {
    this.retrieveActors();
    this.currentActor = undefined;
    this.currentIndex = -1;
  }

  setActiveActor(actor: Actor, index: number): void {
    this.currentActor = actor;
    this.currentIndex = index;
  }

  removeAllActors(): void {
    this.actorService.deleteAll()
      .subscribe(
        response => {
          console.log(response);
          this.refreshList();
        },
        error => {
          console.log(error);
        });
  }

  searchFirstName(): void {
    this.actorService.findByFirstName(this.first_name)
      .subscribe(
        data => {
          this.actors = data;
          console.log(data);
        },
        error => {
          console.log(error);
        });
  }

}
