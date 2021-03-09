-- Create the user and grant privileges
CREATE USER 'castapp'@'localhost' IDENTIFIED BY 'picasso0';
GRANT
    INSERT, SELECT, UPDATE, DELETE
    , SHOW VIEW
ON
    castapp.*
TO
    'castapp'@'localhost';

FLUSH PRIVILEGES;


CREATE DATABASE castapp;

