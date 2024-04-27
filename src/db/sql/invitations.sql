CREATE TYPE invitation_status AS ENUM ('pending', 'accepted', 'maybe', 'declined');

CREATE TABLE "invitations" (
  "invitation_id" SERIAL PRIMARY KEY,
  "event_id" INT NOT NULL,
  "invitee_id" INT NOT NULL,
  "status" invitation_status NOT NULL DEFAULT 'pending'
);
