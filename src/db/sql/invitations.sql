CREATE TABLE invitations (
  invitation_id INT AUTO_INCREMENT PRIMARY KEY,
  event_id INT NOT NULL,
  invitee_id INT NOT NULL,
  status ENUM('pending', 'accepted', 'maybe', 'declined') NOT NULL DEFAULT 'pending',
  FOREIGN KEY (event_id) REFERENCES events(event_id),
  FOREIGN KEY (invitee_id) REFERENCES users(user_id)
);
