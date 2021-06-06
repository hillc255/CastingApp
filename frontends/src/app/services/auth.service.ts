import { Injectable } from '@angular/core';
//import decode from 'jwt-decode';


@Injectable()
export class AuthService {
  public getToken(): string {
    return localStorage.getItem('token');
  }
  // public isAuthenticated(): boolean {
  //   // get the token
  //   const token = this.getToken();
  //   // return a boolean reflecting 
  //   // whether or not the token is expired
  //   return tokenNotExpired(null, token);
  // }
}




// import { Injectable } from '@angular/core';
// import * as auth0 from 'auth0-js';
// // //import * as Auth0 from 'auth0-web';


// @Injectable({
//   providedIn: 'root'
// })

// @Injectable()
// export class AuthService {
//   private AUTH0_DOMAIN = 'autumn-voice-0666.us.auth0.com', //'[AUTH0_DOMAIN]';
//   // Create Auth0 WebAuth instance
//   private _webAuth = new auth0.WebAuth({
//     domain: this.AUTH0_DOMAIN,
//     clientID: 'f7ZLU2DmWeRcLuikyEKjqk0893KA2Mbj', //'[AUTH0_CLIENT_ID]',
//     responseType: 'token',
//     redirectUri: 'http://localhost:8081',
//     audience: `https://${this.AUTH0_DOMAIN}/userinfo`, // This audience grants access to user profile data
//     scope: 'openid profile email'
//   });

  // // Store the user's profile locally once they log in
  // userProfile: any;
  // // Store access token to authorize an API (future)
  // accessToken: string;

//   constructor() {
//     // You should explore token renewal with checkSession() to restore user login when returning
//     // to an app with an unexpired session:
//     // https://auth0.com/docs/libraries/auth0js/v9#using-checksession-to-acquire-new-tokens
//   }

//   login(): void {
//     // Send Auth0 authorize request; opens the Auth0 login page
//     this._webAuth.authorize();
//   }

//   handleLoginCallback(): void {
//     // When Auth0 hash parsed, execute method to get user's profile and set session
//     this._webAuth.parseHash((err, authResult) => {
//       if (authResult && authResult.accessToken) {
//         window.location.hash = '';
//         this.getUserInfo(authResult);
//       } else if (err) {
//         console.error(`Error: ${err.error}`);
//       }
//     });
//   }

//   private getUserInfo(authResult): void {
//     // Use access token to retrieve user's profile and set session
//     this._webAuth.client.userInfo(authResult.accessToken,
//       (err, profile) => {
//         const expTime = authResult.expiresIn * 1000 + Date.now();
//         // Store auth data
//         this.accessToken = authResult.accessToken;
//         localStorage.setItem('expires_at', JSON.stringify(expTime));
//         this.userProfile = profile;
//       }
//     );
//   }

//   logout(): void {
//     // Remove tokens, profile, and expiration data
//     localStorage.removeItem('expires_at');
//     this.accessToken = undefined;
//     this.userProfile = undefined;
//   }

//   get isLoggedIn(): boolean {
//     // Check if current date is greater than expiration and an access token and profile are available.
//     // This is an accessor, so calling it does not require use of parens; e.g., isLoggedIn
//     const expiresAt = JSON.parse(localStorage.getItem('expires_at'));
//     return (Date.now() < expiresAt) && this.accessToken && this.userProfile;
//   }
// }