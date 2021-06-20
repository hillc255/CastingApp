import { Component, OnInit } from '@angular/core';
import { ActorService } from 'src/app/services/actor.service';
import { ActivatedRoute, Router } from '@angular/router';
import { Actor } from 'src/app/models/actor.model';
import { AuthService } from '@auth0/auth0-angular';
import { environment } from 'src/environments/environment';

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
  isAssistant: boolean = false; //added as a property of component
  isDirector: boolean = false; //added as a property of component

  constructor(
    private actorService: ActorService,
    private route: ActivatedRoute,
    private router: Router,
    public auth0: AuthService) { }

  async ngOnInit() {
    this.message = '';
    this.getActor(this.route.snapshot.params.id);
    this.checkRoles() ; //function whenever page loads
  }

  getActor(id: string): void {
    this.actorService.getActor(id)
      .subscribe(
        data => {
          if(data && data.success === true) {
            this.currentActor = data.actor;
            console.log(`getActor(${id}): returned actor`, this.currentActor);
          } else {
            console.error(`getActor(${id}) failed`, data);
          }
        },
        error => {
          console.error(`getActor(${id})`, error);
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
          this.message = (response.success)?"Successful Robot update!":"Unsuccessful Robot update";
        },
        error => {
          console.log(error);
          this.message = "Unsuccessful Robot update";
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

  //method called after component loads to check the roles
  checkRoles() {
    console.log('checkRoles()');
    this.auth0.isAuthenticated$  //observable which returns the authenticated status
      .subscribe(
        isAuthenticated=>{
          if(isAuthenticated) {  //if authenticated then gets the user
            console.log('checkRoles(): authenticated getting user');
            this.auth0.user$  //observable which returns the user
              .subscribe(
                user=>{  // returns the user
                  console.log('checkRoles(): user', user);
                  const roles: Array<string> = user[ environment.userRole ]; //fetch roles from user
                  //const roles: Array<string> = user["https://cast-app.herokuapp.com/roles"]; //fetch roles from user
                  console.log("checkRoles(): user roles: ", roles);
                  this.isAssistant = roles.some(elem => elem=="assistant")
                  this.isDirector = roles.some(elem => elem=="director")
                },
                err=>{
                  console.log('checkRoles(): error getting user', err);
                }
              );
          } else {
            console.log('checkRoles(): not authenticated ');
          }
        },
        err=>{
          console.log('checkRoles(): error getting authentication status', err);
        }
      );
  }
}
