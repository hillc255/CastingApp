// This file can be replaced during build by using the `fileReplacements` array.
// `ng build --prod` replaces `environment.ts` with `environment.prod.ts`.
// The list of file replacements can be found in `angular.json`.

// export const environment = {
//   production: false
// };

// environment.ts
export const environment = {
  production: false,
  title: 'Local Environment Heading',
  auth: {
    clientID: 'f7ZLU2DmWeRcLuikyEKjqk0893KA2Mbj', //'YOUR-AUTH0-CLIENT-ID',
    domain: 'autumn-voice-0666.us.auth0.com', //'YOUR-AUTH0-DOMAIN', // e.g., you.auth0.com
    audience: 'https://cast-app.herokuapp.com/api', //'YOUR-AUTH0-API-IDENTIFIER', // e.g., http://localhost:3001
    redirect: 'http://localhost:8081', //http://localhost:4200/callback',
    scope: 'openid profile email',
    uri: 'https://cast-app.herokuapp.com/*'
  }
};

/*
 * For easier debugging in development mode, you can import the following file
 * to ignore zone related error stack frames such as `zone.run`, `zoneDelegate.invokeTask`.
 *
 * This import should be commented out in production mode because it will have a negative impact
 * on performance if an error is thrown.
 */
// import 'zone.js/dist/zone-error';  // Included with Angular CLI.
