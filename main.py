import streamlit as st
from rembg import remove
from PIL import Image
import io

# Set page configuration
st.set_page_config(
    page_title="AI Background Remover",
    page_icon="✂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to improve the UI
st.markdown("""
    <style>
        /* Main container styling */
        .main {
            padding: 2rem;
        }
        
        /* Title styling */
        h1 {
            text-align: center;
            margin-bottom: 0.5rem;
        }
        
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 2rem;
        }
        
        /* Processing container styling */
        .processing-container {
            background-color: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 10px;
            padding: 1.5rem;
            margin: 1rem 0;
        }
        
        /* File uploader styling */
        .uploadedFile {
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 10px;
            border: 2px dashed #4c85f2;
        }
        
        /* Button styling */
        .stButton>button {
            width: 100%;
            background-color: #4c85f2;
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            border: none;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            background-color: #3666c4;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }
        
        /* Column header styling */
        .column-header {
            text-align: center;
            color: #333;
            font-size: 1.1rem;
            font-weight: bold;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #4c85f2;
        }
        
        /* Preview text styling */
        .preview-text {
            text-align: center;
            color: #666;
            padding: 1rem;
            border: 1px dashed #ccc;
            border-radius: 5px;
            margin: 1rem 0;
            background-color: white;
        }
        
        /* Image container styling */
        .image-display {
            background-color: white;
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            margin-bottom: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

def remove_background(image: Image.Image) -> Image.Image:
    """Remove background from an uploaded image using rembg."""
    return remove(image)

def create_thumbnail(image: Image.Image, size=(200, 200)) -> Image.Image:
    """Create a thumbnail while maintaining aspect ratio."""
    thumb = image.copy()
    aspect_ratio = thumb.width / thumb.height
    
    if aspect_ratio > 1:
        new_width = size[0]
        new_height = int(size[0] / aspect_ratio)
    else:
        new_height = size[1]
        new_width = int(size[1] * aspect_ratio)
    
    thumb = thumb.resize((new_width, new_height), Image.Resampling.LANCZOS)
    return thumb

# Simple title without container
st.markdown("# ✂️ AI Background Remover")
st.markdown('<p class="subtitle">Transform your images by removing backgrounds instantly using AI</p>', unsafe_allow_html=True)

# Progress placeholder
progress_placeholder = st.empty()

# Main processing section with three columns
with st.container():
    # Add the processing container style
    st.markdown('<div class="processing-container">', unsafe_allow_html=True)
    
    # Create three equal columns for the main workflow
    upload_col, preview_col, result_col = st.columns(3)

    # Column 1: Upload
    with upload_col:
        st.markdown('<div class="column-header">Upload Image</div>', unsafe_allow_html=True)
        uploaded_image = st.file_uploader(
            "Drop image here",
            type=["jpg", "jpeg", "png"],
            help="Supported formats: JPG, JPEG, PNG"
        )

    # Initialize session state for processed image if not exists
    if 'processed_image' not in st.session_state:
        st.session_state.processed_image = None

    # Column 2: Preview
    with preview_col:
        st.markdown('<div class="column-header">Preview</div>', unsafe_allow_html=True)
        
        if uploaded_image is not None:
            try:
                # Load and display thumbnail
                image = Image.open(uploaded_image)
                thumbnail = create_thumbnail(image)
                st.image(thumbnail, use_column_width=True)
                
                # Process button below preview
                if st.button("🪄 Remove Background", key="remove_bg"):
                    with st.spinner("🔮 Magic in progress... Please wait"):
                        # Show progress bar
                        progress_bar = progress_placeholder.progress(0)
                        for i in range(100):
                            progress_bar.progress(i + 1)
                        
                        # Process the image and store full resolution result
                        result_image = remove_background(image)
                        st.session_state.processed_image = result_image
                        
                        # Create thumbnail of processed image
                        result_thumbnail = create_thumbnail(result_image)
                        st.session_state.processed_thumbnail = result_thumbnail
                        
                        # Clear progress bar
                        progress_placeholder.empty()
                        
                        st.success("✨ Background removed successfully!")
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
        else:
            st.markdown("""
                <div class="preview-text">
                    Upload an image to see preview
                </div>
            """, unsafe_allow_html=True)

    # Column 3: Result
    with result_col:
        st.markdown('<div class="column-header">Result</div>', unsafe_allow_html=True)
        
        if st.session_state.processed_image is not None:
            # Display thumbnail version
            st.image(st.session_state.processed_thumbnail, use_column_width=True)
            
            # Add download button for the full resolution processed image
            buf = io.BytesIO()
            st.session_state.processed_image.save(buf, format="PNG")
            st.download_button(
                label="📥 Download Full Resolution Image",
                data=buf.getvalue(),
                file_name="processed_image.png",
                mime="image/png"
            )
        else:
            st.markdown("""
                <div class="preview-text">
                    Processed image will appear here
                </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # Close processing-container

# Footer
st.markdown("""
    <div style="text-align: center; margin-top: 2rem; padding: 1rem; background-color: #f0f2f6; border-radius: 10px;">
        <p style="color: #666; font-size: 0.8rem;">
            Made with ❤️ using Streamlit and rembg
        </p>
    </div>
""", unsafe_allow_html=True)