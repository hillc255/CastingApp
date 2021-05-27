// import { Component } from '@angular/core';

// // Import the AuthService type from the SDK
// import { AuthService } from '@auth0/auth0-angular';

// @Component({
//   selector: 'app-auth-button',
//   template: '<button (click)="auth.loginWithRedirect()">Log in</button>'
// })
// export class AuthButtonComponent {
//   // Inject the authentication service into your component through the constructor
//   constructor(public auth: AuthService) {}
// }


// import { AuthService } from './../auth.service';
// import { Component, OnInit } from '@angular/core';

// @Component({
//   selector: 'todo-auth',
//   template: `
//     <div class="todo-auth">
//       <button
//         *ngIf="!authService.isLoggedIn"
//         (click)="authService.login()"
//         class="btn">Log In</button>
//       <ng-template [ngIf]="authService.isLoggedIn">
//         <img [src]="authService.userProfile?.picture" />{{authService.userProfile?.name}}
//         <button
//           (click)="authService.logout()"
//           class="btn btn-red">Log Out</button>
//       </ng-template>
//     </div>
//   `,
//   styleUrls: ['./auth.component.css']
// })
// export class AuthComponent implements OnInit {

//   constructor(public authService: AuthService) { }

//   ngOnInit() {
//   }

// }