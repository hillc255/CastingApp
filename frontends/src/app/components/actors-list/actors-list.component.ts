import { Component, OnInit } from '@angular/core';
import { Actor } from 'src/app/models/actor.model';
import { ActorService } from 'src/app/services/actor.service';
import { AuthService } from '@auth0/auth0-angular';
import { environment } from 'src/environments/environment';

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
  isAssistant: boolean = false; //added as a property of component
  isDirector: boolean = false; //added as a property of component

  constructor(
    private actorService: ActorService,
    public auth0: AuthService) { }

  async ngOnInit() {
    this.retrieveActors();
    this.checkRoles() ; //function whenever page loads
  }

  retrieveActors(): void {
    this.actorService.getAllActors()
      .subscribe(
        data => {
          this.actors = data;
          console.log(data);
        },
        error => {
          console.log(error);
        });
  }

  setDefaultPic() {
    this.currentActor.actor_img = "https://i.ibb.co/6v84Gpq/no-image.png";
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

  searchFirstName(): void {
    this.actorService.findActorByFirstName(this.first_name)
      .subscribe(
        data => {
          this.actors = data;
          console.log(data);
        },
        error => {
          console.log(error);
        });
  }

  formatReleaseDate(): void {
    var parsedData;
    let dateString = this.currentActor.birth_date;
    parsedData = new Date(dateString);
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
