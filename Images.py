
import streamlit as st
from deepface import DeepFace
import os
from PIL import Image

def find_matching_photos(reference_image_path, folder_path):
    """
    Finds all photos in a folder that match the reference image.
    """
    if not os.path.isdir(folder_path):
        st.error("The specified folder does not exist.")
        return []

    try:
        # Use DeepFace to find matching photos
        results = DeepFace.find(
            img_path=reference_image_path,
            db_path=folder_path,
            detector_backend="opencv",
            align=True
        )
        matching_photos = results[0]['identity'].tolist()
        return matching_photos
    except Exception as e:
        st.error(f"Error during face matching: {e}")
        return []

def display_photos(photo_paths):
    """
    Displays photos in a grid using Streamlit.
    """
    if not photo_paths:
        st.warning("No matching photos found.")
        return

    st.info(f"Found {len(photo_paths)} matching photos:")
    cols = st.columns(3)  # Create 3 columns for the grid
    for i, photo_path in enumerate(photo_paths):
        with cols[i % 3]:
            try:
                image = Image.open(photo_path)  # Load the image
                st.image(image, caption=os.path.basename(photo_path), use_column_width=True)
            except Exception as e:
                st.error(f"Could not load image {photo_path}: {e}")

def main():
    st.title("Face Matching Application")
    st.write("This app allows you to find photos of a specific person in a folder.")

    # Step 1: Choose input method (upload image or use camera)
    option = st.radio("Choose An Option:", ("Upload Image", "Use Camera"))

    if option == "Use Camera":
        # Capture reference image using Streamlit camera input
        st.header("Step 1: Capture Reference Image")
        reference_image = st.camera_input("Take a photo")

        if reference_image:
            # Save the captured image to a temporary file
            reference_image_path = "captured_reference.jpg"
            with open(reference_image_path, "wb") as f:
                f.write(reference_image.getbuffer())
            st.success("Reference image captured successfully!")
            st.image(reference_image, caption="Captured Reference Image", use_column_width=True)

    elif option == "Upload Image":
        # Upload reference image using Streamlit file uploader
        st.header("Step 1: Upload Reference Image")
        uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

        if uploaded_image:
            # Save the uploaded image to a temporary file
            reference_image_path = "uploaded_reference.jpg"
            with open(reference_image_path, "wb") as f:
                f.write(uploaded_image.getbuffer())
            st.success("Reference image uploaded successfully!")
            st.image(uploaded_image, caption="Uploaded Reference Image", use_column_width=True)

    # Step 2: Select folder containing photos
    st.header("Step 2: Select Folder Containing Photos")
    folder_path = st.text_input("Enter the path to the folder containing photos:")

    if folder_path and st.button("Find Matching Photos"):
        if not os.path.isdir(folder_path):
            st.error("Invalid folder path. Please check and try again.")
            return

        st.info("Finding matching photos...")
        matching_photos = find_matching_photos(reference_image_path, folder_path)

        # Step 3: Display matching photos
        st.header("Step 3: Matching Photos")
        if matching_photos:
            display_photos(matching_photos)
        else:
            st.warning("No matching photos found.")

if __name__ == "__main__":
    main()
