CREATE TABLE "calendar_shares" (
  "id" SERIAL PRIMARY KEY,
  "owner_id" INT NOT NULL,
  "shared_with_id" INT NOT NULL
);
