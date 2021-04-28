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
    gender: '',
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
    this.actorService.getActor(id)
      .subscribe(
        data => {
          this.currentActor = data;  
          console.log(data);
        },
        error => {
          console.error(error);
        });
  }

  publishActor(): void {
    this.actorService.publishActor(this.currentActor.id)
      .subscribe(
        response => {
          this.getActor(this.route.snapshot.params.id);
        },
        error => {
          console.log(error);
        });
  }

  unpublishActor(): void {
    this.actorService.unpublishActor(this.currentActor.id)
      .subscribe(
        response => {
          this.getActor(this.route.snapshot.params.id);
        },
        error => {
          console.log(error);
        });
  }

  updateActor(): void {
    this.actorService.updateActor(this.currentActor.id, this.currentActor)
      .subscribe(
        response => {
          console.log(response);
          this.message = response.message;
        },
        error => {
          console.log(error);
        });
  }

  deleteActor(): void {
    this.actorService.deleteActor(this.currentActor.id)
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
