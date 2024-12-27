KNOWN_PEOPLE = {person1, person2, ...} 

function train_model_on(pictures) 
  # Train a facial recognition model on the provided pictures 
  # of known people 

function is_known_person(person) 
  # Use the trained model to check if the person is in KNOWN_PEOPLE 

function walking_towards(house) 
  # Determine if the person is moving towards the house 
  # (e.g., using motion detection and object tracking)

function in_view(person) 
  # Check if the person is currently within the camera's field of view

function duration_in_view(person) 
  # Calculate the total time the person has been in view

function save_recording() 
  # Save the recorded video or images of the person

function send_email_via_smtp(subject, body, timeout) 
  # Send an email using SMTP with the given subject and body 
  # Return the response received within the timeout period

function delete_recording() 
  # Delete the saved recording 

# Main logic
if not is_known_person(somebody) and walking_towards(house):
  while in_view(somebody):
    # Record the activity of the person 
  if duration_in_view(somebody) > 15: 
    save_recording()
    response = send_email_via_smtp("family_guard: someone was in view for 15s, please review and respond delete y/n", timeout=30)
    if not response.delete: 
      delete_recording()