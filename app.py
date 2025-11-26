import streamlit as st
from rembg import remove
from PIL import Image
import io
import cv2
import numpy as np
import os

# Set page configuration
st.set_page_config(
    page_title="Background Remover",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .upload-section {
        border: 2px dashed #ccc;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        margin-bottom: 2rem;
    }
    .download-btn {
        background-color: #4CAF50;
        color: white;
        padding: 0.5rem 1rem;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        text-decoration: none;
        display: inline-block;
    }
    .success-msg {
        color: #4CAF50;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">🎨 Background Remover</h1>', unsafe_allow_html=True)
    st.markdown("### Remove backgrounds from your images with AI!")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        st.markdown("---")
        
        # Model selection
        model_options = {
            "u2net": "General Purpose (Recommended)",
            "u2netp": "Lightweight",
            "u2net_human_seg": "Human Segmentation",
            "u2net_cloth_seg": "Clothing Segmentation"
        }
        
        selected_model = st.selectbox(
            "Select AI Model:",
            options=list(model_options.keys()),
            format_func=lambda x: model_options[x],
            help="Choose the appropriate model for your image type"
        )
        
        # Additional options
        st.markdown("---")
        st.subheader("Additional Options")
        
        post_process = st.checkbox(
            "Post-processing",
            value=True,
            help="Apply additional processing to improve results"
        )
        
        bg_color = st.color_picker(
            "Background Color (for preview):",
            "#FFFFFF"
        )
        
        st.markdown("---")
        st.info("""
        **How to use:**
        1. Upload an image
        2. Wait for processing
        3. Download the result
        """)

    # Main content area
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📤 Upload Image")
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=['png', 'jpg', 'jpeg', 'webp'],
            help="Supported formats: PNG, JPG, JPEG, WEBP"
        )
        
        if uploaded_file is not None:
            # Display original image
            original_image = Image.open(uploaded_file)
            st.image(original_image, caption="Original Image", use_column_width=True)
            
            # Image info
            st.info(f"""
            **Image Details:**
            - Format: {original_image.format}
            - Size: {original_image.size}
            - Mode: {original_image.mode}
            """)

    with col2:
        st.subheader("📥 Result")
        
        if uploaded_file is not None:
            with st.spinner("🔄 Removing background... This may take a few seconds."):
                try:
                    # Process image
                    input_image = Image.open(uploaded_file)
                    
                    # Remove background
                    output_image = remove(
                        input_image, 
                        session=selected_model,
                        post_process_mask=post_process
                    )
                    
                    # Convert to RGBA if needed
                    if output_image.mode != 'RGBA':
                        output_image = output_image.convert('RGBA')
                    
                    # Display result
                    st.image(output_image, caption="Background Removed", use_column_width=True)
                    
                    # Success message
                    st.success("✅ Background removed successfully!")
                    
                    # Download section
                    st.markdown("---")
                    st.subheader("📥 Download Result")
                    
                    # Convert to bytes for download
                    buf = io.BytesIO()
                    output_image.save(buf, format="PNG", quality=100)
                    byte_im = buf.getvalue()
                    
                    # Download button
                    st.download_button(
                        label="⬇️ Download PNG",
                        data=byte_im,
                        file_name=f"background_removed_{uploaded_file.name.split('.')[0]}.png",
                        mime="image/png",
                        help="Download the image with transparent background"
                    )
                    
                    # Additional format options
                    col_format1, col_format2 = st.columns(2)
                    
                    with col_format1:
                        # JPG with white background
                        jpg_bg = Image.new("RGB", output_image.size, bg_color)
                        jpg_bg.paste(output_image, mask=output_image.split()[-1])
                        jpg_buf = io.BytesIO()
                        jpg_bg.save(jpg_buf, format="JPEG", quality=95)
                        
                        st.download_button(
                            label="⬇️ Download JPG",
                            data=jpg_buf.getvalue(),
                            file_name=f"background_removed_{uploaded_file.name.split('.')[0]}.jpg",
                            mime="image/jpeg",
                            help="Download as JPG with selected background color"
                        )
                    
                    with col_format2:
                        # WEBP format
                        webp_buf = io.BytesIO()
                        output_image.save(webp_buf, format="WEBP", quality=95)
                        
                        st.download_button(
                            label="⬇️ Download WEBP",
                            data=webp_buf.getvalue(),
                            file_name=f"background_removed_{uploaded_file.name.split('.')[0]}.webp",
                            mime="image/webp",
                            help="Download as WEBP format"
                        )
                    
                except Exception as e:
                    st.error(f"❌ Error processing image: {str(e)}")
                    st.info("💡 Try using a different image or model")
        
        else:
            # Placeholder when no image is uploaded
            st.info("👆 Upload an image to see the result here")
            st.image("https://via.placeholder.com/400x300?text=Result+Will+Appear+Here", 
                    use_column_width=True)

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center'>
            <p>Built with ❤️ using Streamlit & Rembg</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
