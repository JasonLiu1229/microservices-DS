CREATE TABLE "participations" (
  "participation_id" INT SERIAL PRIMARY KEY,
  "event_id" INT NOT NULL,
  "participant_id" INT NOT NULL,
  "status" ENUM('accepted', 'maybe', 'declined') NOT NULL,
  FOREIGN KEY (event_id) REFERENCES events(event_id),
  FOREIGN KEY (participant_id) REFERENCES users(user_id)
);
