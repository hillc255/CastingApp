export const environment = {
  production: true,
  title: 'Production Environment Heading',
  userRole: 'https://cast-app.herokuapp.com/roles',
  baseUrl: 'https://cast-app.herokuapp.com/api/movies',
  baseUrl2: 'https://cast-app.herokuapp.com/api/actors',
  auth: {
    clientID: 'f7ZLU2DmWeRcLuikyEKjqk0893KA2Mbj',
    domain: 'autumn-voice-0666.us.auth0.com',
    audience: 'https://cast-app.herokuapp.com/api',
    redirect: 'https://cast-app.herokuapp.com',
    scope: 'openid profile email',
    uri: 'https://cast-app.herokuapp.com/*'
  }
};
