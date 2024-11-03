import streamlit as st
from rembg import remove
from PIL import Image
import io
from datetime import datetime
import time

# Set page configuration
st.set_page_config(
    page_title="AI Background Remover",
    page_icon="✂️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Enhanced CSS with mobile responsiveness fixes
st.markdown("""
    <style>
        /* Viewport meta tag simulation */
        html {
            width: 100%;
            overflow-x: hidden;
        }
        
        body {
            width: 100%;
            overflow-x: hidden;
            margin: 0;
            padding: 0;
        }
        
        /* Container styling */
        .main {
            width: 100%;
            max-width: 100vw;
            padding: 0.5rem;
            box-sizing: border-box;
            overflow-x: hidden;
        }
        
        /* Header styling */
        h1 {
            text-align: center;
            margin-top: 0.4rem;
            font-size: clamp(2rem, 1vw, 5rem);
            color: #1f1f1f;
            word-wrap: break-word;
        }
        
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 2rem;
            margin-top: -0.8rem;
            font-size: clamp(0.875rem, 3vw, 1rem);
            word-wrap: break-word;
        }
        
        /* Main content container */
        .content-container {
            background-color: #ffffff;
            border-radius: 15px;
            padding: 1rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin: 0.5rem auto;
            width: 100%;
            max-width: min(600px, 95vw);
            box-sizing: border-box;
        }
        
        /* Upload area styling */
        .upload-area {
            border: 2px dashed #4c85f2;
            border-radius: 10px;
            padding: 1rem;
            text-align: center;
            background-color: #f8f9fa;
            transition: all 0.3s ease;
            width: 100%;
            box-sizing: border-box;
            
        }
        
        /* Image preview container */
        .image-preview {
            margin: 1rem 0;
            border-radius: 10px;
            overflow: hidden;
            background-color: #f8f9fa;
            max-width: 100%;
        }
        
        /* Image styling */
        img {
            max-width: 100%;
            height: auto;
        }
        
        /* Button container */
        .stButton {
            width: 100%;
            margin: 0;
        }
        
        .stButton > button {
            width: 100%;
            padding: 0.75rem;
            word-wrap: break-word;
            white-space: normal;
            height: auto;
            min-height: 46px;
        }
        
        /* File uploader modifications */
        .uploadedFile {
            padding: 0.5rem;
            margin: 0.5rem 0;
            border-radius: 10px;
            max-width: 100%;
        }
        
        /* Progress bar container */
        .stProgress {
            max-width: 100%;
        }
        
        /* Footer styling */
        .footer {
            
            text-align: center;
            padding: 0.5rem;
            background-color: #f8f9fa;
            border-radius: 10px;
            margin-top: 10rem;
            font-size: clamp(0.5rem, 1.5vw, 0.7rem);
            color: #666;
            width: 100%;
            box-sizing: border-box;
        }
        
        /* Streamlit specific fixes */
        .block-container {
            max-width: 60%;
            padding-left: 1rem;
            padding-right: 1rem;
            padding-top: 1rem;
        }
        
        .css-1d391kg {
            width: 100%;
        }
        
        /* Fix for download buttons */
        .stDownloadButton {
            width: 100%;
            margin-bottom: 0.5rem;
        }
        
        .stDownloadButton > button {
            width: 100%;
            word-wrap: break-word;
            white-space: normal;
        }
        
        @media (max-width: 768px) {
            .block-container {
            
                max-width: 100%;
                padding-left: 0.5rem;
                padding-right: 0.5rem;
            }
            
            .upload-area {
                padding: 0.75rem;
            }
            
            .stButton > button {
                padding: 0.5rem;
            }
        }
    </style>
""", unsafe_allow_html=True)

def remove_background(image: Image.Image) -> Image.Image:
    """Remove background from an uploaded image using rembg."""
    return remove(image)

def create_display_image(image: Image.Image, max_size=(800, 800)) -> Image.Image:
    """Create a display version of the image while maintaining quality and aspect ratio."""
    display_img = image.copy()
    
    # Calculate new size while maintaining aspect ratio
    aspect_ratio = display_img.width / display_img.height
    
    if aspect_ratio > 1:
        if display_img.width > max_size[0]:
            new_width = max_size[0]
            new_height = int(max_size[0] / aspect_ratio)
        else:
            return display_img
    else:
        if display_img.height > max_size[1]:
            new_height = max_size[1]
            new_width = int(max_size[1] * aspect_ratio)
        else:
            return display_img
    
    return display_img.resize((new_width, new_height), Image.Resampling.LANCZOS)

# Initialize session state
if 'processed_image' not in st.session_state:
    st.session_state.processed_image = None
if 'processing_complete' not in st.session_state:
    st.session_state.processing_complete = False

# Main content
st.markdown("# ✂️ AI Background Remover")
st.markdown('<p class="subtitle">Transform your images instantly</p>', unsafe_allow_html=True)


# File uploader
uploaded_image = st.file_uploader(
    "Drop your image here",
    type=["jpg", "jpeg", "png"],
    help="Supported formats: JPG, JPEG, PNG"
)

# Image processing and display
if uploaded_image is not None:
    # Reset processing state when new image is uploaded
    if 'current_image' not in st.session_state or st.session_state.current_image != uploaded_image:
        st.session_state.processing_complete = False
        st.session_state.current_image = uploaded_image
    
    image = Image.open(uploaded_image)
    display_image = create_display_image(image)
    
    # Create a placeholder for the image display
    image_placeholder = st.empty()
    
    # Show original image first
    image_placeholder.image(display_image, use_column_width=True)
    
    if not st.session_state.processing_complete:
        # Processing indicator
        progress_placeholder = st.empty()
        status_placeholder = st.empty()
        
        with status_placeholder:
            st.markdown('<div class="processing-text">✨ Magic in progress...</div>', 
                       unsafe_allow_html=True)
        
        # Show processing progress
        progress_bar = progress_placeholder.progress(0)
        for i in range(100):
            time.sleep(0.01)  # Simulate processing time
            progress_bar.progress(i + 1)
        
        # Process image
        result_image = remove_background(image)
        st.session_state.processed_image = result_image
        display_processed = create_display_image(result_image)
        st.success("✨ Background removed successfully!")
        # Update display with processed image
        image_placeholder.image(display_processed, use_column_width=True)
        
        # Clear progress indicators
        progress_placeholder.empty()
        status_placeholder.empty()
        
        st.session_state.processing_complete = True
    
    # Show download buttons only after processing is complete
    if st.session_state.processing_complete:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # PNG Download
        buf = io.BytesIO()
        st.session_state.processed_image.save(
            buf, 
            format="PNG",
            optimize=True
        )
        st.download_button(
            label="📥 Download as PNG",
            data=buf.getvalue(),
            file_name=f"erasebackgrond_{timestamp}.png",
            mime="image/png",
            use_container_width=True
        )
        
        # JPEG Download
        jpeg_buf = io.BytesIO()
        jpeg_image = st.session_state.processed_image.convert('RGB')
        jpeg_image.save(
            jpeg_buf, 
            format="JPEG",
            optimize=True
        )
        st.download_button(
            label="📥 Download as JPEG",
            data=jpeg_buf.getvalue(),
            file_name=f"erasebackground_{timestamp}.jpg",
            mime="image/jpeg",
            use_container_width=True
        )

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer">
        Made with ❤️ using Streamlit and rembg by Hari and Anup
    </div>
""", unsafe_allow_html=True)