import cv2
import shutil
import os

# cascade_path = "pathlib.Path(cv2.__file__).parent.absolute() / "data/haarcascade_frontalface_default.xml"
cascade_path = r"Cascade\haarcascade_frontalface_default.xml"
clf = cv2.CascadeClassifier(str(cascade_path))


def reduce_saturation(image, saturation_factor):
    # Convert the image to the HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Reduce the saturation channel (S) by a factor
    hsv_image[..., 1] = hsv_image[..., 1] * saturation_factor

    # Convert the image back to the BGR color space
    processed_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

    return processed_image


def detect_and_process_faces(image, cropping_area, saturation_factor):
    try:
        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect faces in the grayscale image
        faces = clf.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) > 0:
            x, y, w, h = faces[0]

            # Calculate the cropping area
            crop_size = int(min(w, h) * cropping_area)

            # Calculate the center coordinates of the face
            center_x = x + w // 2
            center_y = y + h // 2

            # Calculate the top-left coordinates for cropping
            crop_left = center_x - crop_size // 2
            crop_top = center_y - crop_size // 2

            # Calculate the bottom-right coordinates for cropping
            crop_right = crop_left + crop_size
            crop_bottom = crop_top + crop_size

            # Adjust cropping area to stay within image boundaries
            height, width = image.shape[:2]
            crop_top = max(0, crop_top)
            crop_bottom = min(height, crop_bottom)
            crop_left = max(0, crop_left)
            crop_right = min(width, crop_right)

            # Perform cropping around the detected face
            cropped_image = image[crop_top:crop_bottom, crop_left:crop_right]

            # Reduce the saturation of the cropped image
            processed_image = reduce_saturation(cropped_image, saturation_factor)

            return processed_image
        else:
            return None
    except Exception as e:
        print("Error occurred in detect_and_process_faces:", e)
        return None


def process_all_images(input_folder, output_folder, cropping_area, saturation_factor):
    # Delete the output folder if it exists
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)

    # Create the new output folder
    os.makedirs(output_folder)

    # Get a list of all files in the input folder
    files = os.listdir(input_folder)

    # Loop through each file
    for file in files:
        # Check if the file is an image
        if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
            # Read the image using OpenCV
            image_path = os.path.join(input_folder, file)
            image = cv2.imread(image_path)

            # Process the image and get the result
            processed_image = detect_and_process_faces(image, cropping_area, saturation_factor)

            if processed_image is not None:
                # Save the processed image to the output folder
                output_path = os.path.join(output_folder, file)
                cv2.imwrite(output_path, processed_image)

                print(f"Cropped and processed image saved: {output_path}")
            else:
                print(f"No faces detected in {file}")


def process_current_image(input_image_path, output_image_path, cropping_area, saturation_factor):
    # Create the output folder if it doesn't exist
    os.makedirs(os.path.dirname(output_image_path), exist_ok=True)

    # Read the input image using OpenCV
    input_image = cv2.imread(input_image_path)

    # Process the image and get the result
    processed_image = detect_and_process_faces(input_image, cropping_area, saturation_factor)

    if processed_image is not None:
        # Save the processed image to the output path
        cv2.imwrite(output_image_path, processed_image)
        print(f"Cropped and processed image saved: {output_image_path}")
    else:
        print(f"No faces detected in {input_image_path}")
