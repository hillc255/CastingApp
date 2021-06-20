import { Component, OnInit } from '@angular/core';
import { Actor } from 'src/app/models/actor.model';
import { ActorService } from 'src/app/services/actor.service';
import { AuthService } from '@auth0/auth0-angular';

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
  isDirector: boolean = false; //isDirector is a property of component

  constructor(
    private actorService: ActorService,
    public auth0: AuthService) { }

  async ngOnInit() {
    this.checkRoles() ; //function whenever page loads
  }

  saveActor(form: any): void {
    const data = {
      first_name: this.actor.first_name,
      last_name: this.actor.last_name,
      birth_date: this.actor.birth_date,
      gender: this.actor.gender,
      actor_img: this.actor.actor_img,
      actor_publish: this.actor.actor_publish
    };

    this.actorService.addActor(data)
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
                  const roles: Array<string> = user["https://cast-app.herokuapp.com/roles"]; //fetch roles from user
                  console.log("checkRoles(): user roles: ", roles);
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
