CREATE TABLE "events" (
  "id" SERIAL PRIMARY KEY,
  "organizer_id" INT NOT NULL,
  "title" TEXT NOT NULL,
  "description" TEXT,
  "date" DATE NOT NULL,
  "is_public" BOOLEAN NOT NULL DEFAULT false
);
