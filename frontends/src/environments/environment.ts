export const environment = {
  production: false,
  title: 'Local Environment Heading',
  userRole: 'https://cast-app.herokuapp.com/roles',
  baseUrl: 'https://cast-app.herokuapp.com/movies',
  baseUrl2: 'https://cast-app.herokuapp.com/actors',
  auth: {
    clientID: 'f7ZLU2DmWeRcLuikyEKjqk0893KA2Mbj',
    domain: 'autumn-voice-0666.us.auth0.com',
    audience: 'https://cast-app.herokuapp.com/api',
    redirect: 'http://localhost:8081',
    scope: 'openid profile email',
    uri: 'https://cast-app.herokuapp.com/*'
  }
};
