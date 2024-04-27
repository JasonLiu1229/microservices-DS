CREATE TABLE "calendar_shares" (
  "share_id" INT SERIAL PRIMARY KEY,
  "owner_id" INT NOT NULL,
  "shared_with_id" INT NOT NULL,
  FOREIGN KEY (owner_id) REFERENCES users(user_id),
  FOREIGN KEY (shared_with_id) REFERENCES users(user_id)
);
