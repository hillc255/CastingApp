import { Component, Inject } from '@angular/core';
import { DOCUMENT } from '@angular/common';

// Import the AuthService type from the SDK
import { AuthService } from '@auth0/auth0-angular';

@Component({
  selector: 'app-auth-button',
  template: `
    <ng-container *ngIf="auth.isAuthenticated$ | async; else loggedOut">
      <button (click)="auth.logout({ returnTo: document.location.origin })">
        Log out
      </button>
    </ng-container>

    <ng-template #loggedOut>
      <button (click)="auth.loginWithRedirect()">Authorized Login</button>
    </ng-template>
  `,
  styles: [],
})
export class AuthButtonComponent {
  constructor(@Inject(DOCUMENT) public document: Document, public auth: AuthService) {}
}