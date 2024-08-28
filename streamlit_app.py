import streamlit as st
from streamlit_option_menu import option_menu
import os
from PIL import Image

from preprocess import extract_text_from_pdf, preprocess_text_chap8, preprocess_text, get_title, remove_subsequent_occurrences, separate_sections
from summarization import summarize_text_sumy, summarize_text_bert, summarize_text_bart, summarize_text_t5_large, summarize_text_t5_base

# nltk.download('punkt')
# nltk.download('stopwords')

# Set the title of the web app
st.title("Welcome to Future Minds Tutoring")

# Sidebar with navigation options
with st.sidebar:
    option = option_menu("Menu",
                        options=["About Us","Chapter Summary"],
                        icons=['house-fill','search'])

if option == "About Us":
    # Load and resize the image
    img = Image.open("data/Future min.jpg")
    
    # Specify the desired height
    desired_height = 250
    # Calculate the width to maintain the aspect ratio
    width, height = img.size
    aspect_ratio = width / height
    new_width = int(desired_height * aspect_ratio)
    
    # Resize the image
    img = img.resize((new_width, desired_height))
    
    # Display the resized image
    st.image(img, use_column_width=True)

    st.header("About Us")
    st.write("""
    At Future Minds Tutoring, we deliver outstanding educational support to students in grades 10, 11, and 12. Our innovative methodology blends conventional pedagogy with state-of-the-art artificial intelligence technologies to provide all-encompassing and customized learning experiences.

    Our professional educators and AI specialists collaborate to generate chapter-specific content that is simplified and easy to understand, allowing students to grasp and retain information more quickly. Our dedication lies in providing specialized resources and support to kids with exceptional needs, enabling them to overcome obstacles and excel academically.
    """)

    st.header("Mission")
    st.write("""
    Our mission is to provide high-quality, inclusive education to students of classes 10, 11, and 12, fostering an environment where every student, including those with special needs, can excel. We leverage advanced AI technology to deliver personalized and effective learning experiences that help students understand and retain complex concepts.
    """)
    
    st.header("Vision")
    st.write("""
    Our vision is to be a leading educational institution recognized for our commitment to academic excellence and inclusivity. We aim to transform traditional learning by integrating innovative AI solutions, ensuring that every student, regardless of their challenges, has the opportunity to succeed and achieve their full potential.
    """)
    
    

elif option == "Chapter Summary":
    st.subheader("Chapter Summary")
    # File upload section
        
    uploaded_file = st.file_uploader("Upload your file :", type=["pdf"])

    if uploaded_file is not None:
        filename = uploaded_file.name

        if uploaded_file.type == "application/pdf":

            # st.write(f"File Name: {filename}")
            st.success("File uploaded successfully! Please wait for the summary...")
            if filename == 'jefp108.pdf':
                # Extract text from the uploaded PDF file
                raw_text = extract_text_from_pdf(uploaded_file)

                preprocessed_text = preprocess_text_chap8(raw_text)
                title='Bholi'
                
                 # Remove subsequent occurrences of the title
                clean_text = remove_subsequent_occurrences(preprocessed_text, title)

                # Separate sections of the text
                main_content, glossary, think_about_it, talk_about_it, suggested_reading = separate_sections(clean_text)

                # st.write('Main Content:\n',main_content)
                # Summarize the main content using different models
                summary_sumy = summarize_text_sumy(main_content)
                # summary_bert = summarize_text_bert(main_content)
                # summary_bart = summarize_text_bart(main_content)
                # summary_t5_large = summarize_text_t5_large(main_content)
                # summary_t5_base = summarize_text_t5_base(main_content)

                tab1, tab2, tab3, tab4, tab5 = st.tabs(['Summary 1 - Sumy','Summary 2 - BERT', 'Summary 3 - BART', 'Summary 4 - T5-base', 'Summary 5 - T5-large' ])
                with tab1:
                    st.subheader(f'Summary1 of {title}:')
                    st.write(summary_sumy)
            else:
                st.write("Please upload other file....")        

        else:
            st.error("Please upload a valid PDF file.")
            

    else:
        st.warning("Please upload a file.")



# Footer
st.markdown("***")
st.write("© 2024 Future Minds Tutoring. All rights reserved.")
