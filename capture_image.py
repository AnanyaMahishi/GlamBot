import cv2
import sys

def capture_image(save_path):
    # Open the camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        sys.exit(1)

    print("Press 'c' to capture the image.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            sys.exit(1)
        
        # Display the camera feed
        cv2.imshow('Camera', frame)
        
        # Wait for 'c' key to capture the image
        if cv2.waitKey(1) & 0xFF == ord('c'):
            cv2.imwrite(save_path, frame)
            print(f"Image saved to {save_path}")
            break
    
    # Release the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python capture_image.py <save_path>")
        sys.exit(1)

    save_path = sys.argv[1]
    capture_image(save_path)
