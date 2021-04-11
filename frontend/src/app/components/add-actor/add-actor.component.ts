import { Component, OnInit } from '@angular/core';
import { Actor } from 'src/app/models/actor.model';
import { ActorService } from 'src/app/services/actor.service';

@Component({
  selector: 'app-add-actor',
  templateUrl: './add-actor.component.html',
  styleUrls: ['./add-actor.component.css']
})
export class AddActorComponent implements OnInit {
  actor: Actor = {
    first_name: '',
    last_name: '',
    birth_date: '',
    gender: '',
    actor_img: '',
    actor_publish: false
  };
  submitted = false;

  constructor(private actorService: ActorService) { }

  ngOnInit(): void {
  }

  saveActor(): void {
    const data = {
      first_name: this.actor.first_name,
      last_name: this.actor.last_name,
      birth_date: this.actor.birth_date,
      gender: this.actor.gender,
      actor_img: this.actor.actor_img
    };

    this.actorService.create(data)
      .subscribe(
        response => {
          console.log(response);
          this.submitted = true;
        },
        error => {
          console.log(error);
        });
  }

  newActor(): void {
    this.submitted = false;
    this.actor = {
      first_name: '',
      last_name: '',
      birth_date: '',
      gender: '',
      actor_img: '',
      actor_publish: false
    };
  }
}