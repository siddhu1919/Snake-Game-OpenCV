import cv2

# Initialize the webcam (use 0 as the parameter to select the default camera, change it if you have multiple cameras)
cap = cv2.VideoCapture(1)

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # If frame is read c-ṇorrectly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Our operations on the frame come here
    # Display the resulting frame
    cv2.imshow("Webcam", frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# When everything is done, release the capture and destroy all windows
cap.release()
cv2.destroyAllWindows()
