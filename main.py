import tkinter as tk
from PIL import Image, ImageTk
import image_processing
import os
import subprocess

# List to store photo file names in the input folder
photo_files = []
current_index = 0

# Path to the input and output folders
input_folder = "Input"
output_folder = "Output"


def load_photos(folder):
    global photo_files
    photo_files = [file for file in os.listdir(folder) if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]


def display_photo():
    global current_index, photo_files, input_img_label, output_img_label, output_filename_label

    if 0 <= current_index < len(photo_files):
        current_photo = photo_files[current_index]
        input_image_path = os.path.join(input_folder, current_photo)
        output_image_path = os.path.join(output_folder, current_photo)

        # Display the input photo
        input_img = Image.open(input_image_path)
        input_img = input_img.resize((300, 300), Image.LANCZOS)
        input_img = ImageTk.PhotoImage(input_img)
        input_img_label.config(image=input_img)
        input_img_label.image = input_img

        # Update the output filename label
        if os.path.exists(output_image_path):
            output_filename_label.config(text=current_photo)
        else:
            output_filename_label.config(text="Output file not available")

        # Display the output photo if it exists, otherwise display an empty image
        if os.path.exists(output_image_path):
            output_img = Image.open(output_image_path)
        else:
            output_img = Image.new("RGB", (300, 300), color="white")
        output_img = output_img.resize((300, 300), Image.LANCZOS)
        output_img = ImageTk.PhotoImage(output_img)
        output_img_label.config(image=output_img)
        output_img_label.image = output_img


def next_photo():
    global current_index
    current_index = (current_index + 1) % len(photo_files)
    display_photo()


def prev_photo():
    global current_index
    current_index = (current_index - 1) % len(photo_files)
    display_photo()


def open_input_folder():
    subprocess.Popen(f'explorer "{input_folder}"')


def open_output_folder():
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    subprocess.Popen(f'explorer "{output_folder}"')


def process_all_images():
    cropping_area = float(cropping_area_entry.get())
    saturation_factor = float(saturation_factor_entry.get())
    image_processing.process_all_images(input_folder, output_folder, cropping_area, saturation_factor)
    # Display the first photo after processing
    display_photo()


def process_current_image():
    global current_index
    if 0 <= current_index < len(photo_files):
        current_photo = photo_files[current_index]
        input_image_path = os.path.join(input_folder, current_photo)
        output_image_path = os.path.join(output_folder, current_photo)

        cropping_area = float(cropping_area_entry.get())
        saturation_factor = float(saturation_factor_entry.get())

        image_processing.process_current_image(input_image_path, output_image_path, cropping_area, saturation_factor)

        # Display the processed photo
        display_photo()



def create_gui_window():
    global cropping_area_entry, saturation_factor_entry, rename_entry  # Make the entries global

    # Create the Tkinter window
    window = tk.Tk()
    window.title("PhotoProcessor")

    # Load photos from the input folder
    load_photos(input_folder)

    # Create a panel for the top section (input image, renaming, output image)
    top_panel = tk.Frame(window)
    top_panel.pack(side=tk.TOP, pady=10)

    # Create a panel for the input image
    input_panel = tk.Frame(top_panel)
    input_panel.pack(side=tk.LEFT, padx=10)

    # Add a label to display the input photo
    global input_img_label
    input_img_label = tk.Label(input_panel)
    input_img_label.pack()

    # Create a panel for the renaming functionality
    name_panel = tk.Frame(top_panel)
    name_panel.pack(side=tk.LEFT, padx=10)

    # Add a button to run the image processing for the current photo
    process_button = tk.Button(name_panel, text="Process Current Image", command=process_current_image)
    process_button.pack(side=tk.LEFT, padx=10)
  
    # Add a label to display the output image filename
    global output_filename_label
    output_filename_label = tk.Label(name_panel, text="")
    output_filename_label.pack()

    # Create a panel for the output image
    output_panel = tk.Frame(top_panel)
    output_panel.pack(side=tk.LEFT, padx=10)

    # Add a label to display the output photo
    global output_img_label
    output_img_label = tk.Label(output_panel)
    output_img_label.pack()

    # Create a panel for the bottom section (navigation, processing, folders)
    bottom_panel = tk.Frame(window)
    bottom_panel.pack(side=tk.BOTTOM, pady=10)

    # Add buttons to navigate through photos
    prev_button = tk.Button(bottom_panel, text="Previous", command=prev_photo)
    prev_button.pack(side=tk.LEFT, padx=10)

    next_button = tk.Button(bottom_panel, text="Next", command=next_photo)
    next_button.pack(side=tk.LEFT, padx=10)

    # Add text fields for cropping area and saturation factor
    cropping_area_label = tk.Label(bottom_panel, text="Cropping Area:")
    cropping_area_label.pack(side=tk.LEFT)
    cropping_area_entry = tk.Entry(bottom_panel, width=10)
    cropping_area_entry.insert(tk.END, "2.5")
    cropping_area_entry.pack(side=tk.LEFT)

    saturation_factor_label = tk.Label(bottom_panel, text="Saturation Factor:")
    saturation_factor_label.pack(side=tk.LEFT)
    saturation_factor_entry = tk.Entry(bottom_panel, width=10)
    saturation_factor_entry.insert(tk.END, "0.15")
    saturation_factor_entry.pack(side=tk.LEFT)

    # Add a button to run the image processing for all images
    process_all_button = tk.Button(bottom_panel, text="Process All Images", command=process_all_images)
    process_all_button.pack(side=tk.LEFT, padx=10)

    # Add buttons to open input and output folders
    open_input_button = tk.Button(bottom_panel, text="Open Input Folder", command=open_input_folder)
    open_input_button.pack(side=tk.LEFT, padx=10)

    open_output_button = tk.Button(bottom_panel, text="Open Output Folder", command=open_output_folder)
    open_output_button.pack(side=tk.LEFT, padx=10)

    # Display the first photo
    display_photo()

    # Run the Tkinter event loop
    window.mainloop()


def main():
    # Call the function to create the GUI window
    create_gui_window()


# First name Last name ID number all of which are found in the file itself
if __name__ == "__main__":
    main()
