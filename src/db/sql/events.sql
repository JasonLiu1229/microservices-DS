CREATE TABLE "events" (
  "event_id" SERIAL PRIMARY KEY,
  "organizer_id" INT NOT NULL,
  "title" VARCHAR(100) NOT NULL,
  "description" TEXT,
  "event_date" DATE NOT NULL,
  "is_public" BOOLEAN NOT NULL DEFAULT false,
);
