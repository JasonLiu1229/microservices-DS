CREATE TABLE "users" (
  "id" SERIAL PRIMARY KEY NOT NULL,
  "username" VARCHAR(50) UNIQUE NOT NULL,
  "password" VARCHAR(255) NOT NULL
);
