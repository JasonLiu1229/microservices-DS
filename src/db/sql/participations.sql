CREATE TYPE participation_status AS ENUM ('accepted', 'maybe', 'declined');

CREATE TABLE "participations" (
  "participation_id" SERIAL PRIMARY KEY,
  "event_id" INT NOT NULL,
  "participant_id" INT NOT NULL,
  "status" participation_status NOT NULL
);
