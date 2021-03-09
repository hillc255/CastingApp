DROP DATABASE IF EXISTS castapp;
REVOKE ALL PRIVILEGES ON castapp.* FROM 'castapp'@'localhost';
DROP USER 'castapp'@'localhost';
FLUSH PRIVILEGES;

