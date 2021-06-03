import { Component } from '@angular/core';
import { AuthService } from '@auth0/auth0-angular';

@Component({
  selector: 'app-user-profile',
  template: `
    <ul *ngIf="auth.user$ | async as user">
    <p></p>
      {{ user.email }}
    </ul>`
})
export class UserProfileComponent {
  constructor(public auth: AuthService) {}
}