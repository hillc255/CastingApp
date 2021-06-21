./background/src/database
./backend/src/auth

#running python locally

export DATABASE_URL=localhost:5432

waitress-serve --port=$PORT app:app