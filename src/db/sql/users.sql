
CREATE TABLE "users" (
  "user_id" INT PRIMARY KEY,
  "username" VARCHAR(50) UNIQUE NOT NULL,
  "password" VARCHAR(255) NOT NULL
);

CREATE TABLE "tokens" (
  "token_id" INT PRIMARY KEY,
  "user_id" INT NOT NULL,
  "token" VARCHAR(255) NOT NULL,
  "valid" BOOLEAN NOT NULL,
  FOREIGN KEY ("user_id") REFERENCES "users"("user_id") ON DELETE CASCADE ON UPDATE CASCADE
);
