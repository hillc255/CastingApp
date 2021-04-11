import { Component, OnInit } from '@angular/core';
import { ActorService } from 'src/app/services/actor.service';
import { ActivatedRoute, Router } from '@angular/router';
import { Actor } from 'src/app/models/actor.model';

@Component({
  selector: 'app-actor-details',
  templateUrl: './actor-details.component.html',
  styleUrls: ['./actor-details.component.css']
})
export class ActorDetailsComponent implements OnInit {
  currentActor: Actor = {
    first_name: '',
    last_name: '',
    birth_date: '',
    actor_img: '',
    actor_publish: false
  };
  message = '';

  constructor(
    private actorService: ActorService,
    private route: ActivatedRoute,
    private router: Router) { }

  ngOnInit(): void {
    this.message = '';
    this.getActor(this.route.snapshot.params.id);
  }

  getActor(id: string): void {
    this.actorService.get(id)
      .subscribe(
        data => {
          this.currentActor = data;
          console.log(data);
        },
        error => {
          console.log(error);
        });
  }

  updatePublished(status: boolean): void {
    const data = {
      first_name: this.currentActor.first_name,
      last_name: this.currentActor.last_name,
      birth_date: this.currentActor.birth_date,
      gender: this.currentActor.gender,
      actor_img: this.currentActor.actor_img,
      actor_publish: status
    };

    this.message = '';

    this.actorService.update(this.currentActor.id, data)
      .subscribe(
        response => {
          this.currentActor.actor_publish = status;
          console.log(response);
          this.message = this.message = response.message ? response.message : 'This actor was updated successfully!';
        },
        error => {
          console.log(error);
        });
  }

  updateActor(): void {
    this.message = '';

    this.actorService.update(this.currentActor.id, this.currentActor)
      .subscribe(
        response => {
          console.log(response);
          this.message = response.message ? response.message: 'This actor was updated successfully!';
        },
        error => {
          console.log(error);
        });
  }

  deleteActor(): void {
    this.actorService.delete(this.currentActor.id)
      .subscribe(
        response => {
          console.log(response);
          this.router.navigate(['/actors']);
        },
        error => {
          console.log(error);
        });
  }
}
