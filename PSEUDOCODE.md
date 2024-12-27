# Design - PSEUDOCODE
```pseudocode
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
```

**Explanation:**

1. **Initialization:**
   - `KNOWN_PEOPLE`: A set containing the names or identifiers of known individuals.

2. **Training:**
   - `train_model_on(pictures)`: Trains a facial recognition model using the provided pictures of known people. This model will be used to identify individuals in subsequent frames.

3. **Core Logic:**
   - **Check if the person is unknown:** 
     - `if not is_known_person(somebody)`: If the person is not recognized as a known individual by the trained model.
   - **Check if the person is approaching the house:** 
     - `and walking_towards(house)`: If the person is moving in the direction of the house.
   - **Record while in view:** 
     - `while in_view(somebody)`: Continuously record the activity of the person as long as they are within the camera's view.
   - **Check duration:** 
     - `if duration_in_view(somebody) > 15`: If the person remains in view for more than 15 seconds.
   - **Save recording:** 
     - `save_recording()`: Save the recorded video or images of the person.
   - **Send email notification:** 
     - `response = send_email_via_smtp(...)`: Send an email with a subject and a message asking for confirmation on whether to delete the recording. The email includes a timeout of 30 seconds for a response.
   - **Delete recording (if not confirmed):** 
     - `if not response.delete`: If the user does not explicitly confirm that the recording should be kept, delete the recording.

**Note:**

- This pseudocode provides a basic framework. 
- You'll need to implement the specific functions (`is_known_person`, `walking_towards`, `in_view`, etc.) based on your chosen methods (e.g., object detection, motion tracking, machine learning algorithms).
- Consider adding error handling, security measures (e.g., password protection for email responses), and options for customization (e.g., adjustable recording duration thresholds, different notification methods).

This pseudocode should give you a solid starting point for developing your security system. Remember to prioritize privacy and ethical considerations throughout the development and deployment process.
