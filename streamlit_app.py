import streamlit as st
from streamlit_option_menu import option_menu
import os
from PIL import Image

from pdfminer.high_level import extract_text
import nltk
import nltk
nltk.download('stopwords')
nltk.download('punkt')


#sumy package for extractive summary
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

from transformers import pipeline
from concurrent.futures import ThreadPoolExecutor

import re


# Set the title of the web app
st.title("Welcome to Future Minds Tutoring")

# Sidebar with navigation options
with st.sidebar:
    option = option_menu("Menu",
                        options=["About Us","Chapter Summary"],
                        icons=['house-fill','search'])

if option == "About Us":
    # st.image("D:/MBA/Capstone Project/Capstone Project 2 Text Summarization OCR/code/Future min1.jpg", use_column_width=True)
    # img = Image.open("D:/MBA/Capstone Project/Capstone Project 2 Text Summarization OCR/code/Future min.jpg")
    # img = img.resize((600, int(img.height * 600 / img.width)))  # Adjust the width to 600px and maintain aspect ratio
    # st.image(img, use_column_width=False)

    # Load and resize the image
    img = Image.open("D:\MBA\Capstone Project\Capstone Project 2 Text Summarization OCR\streamlit_code\logo\Future min.jpg")
    
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
        if uploaded_file.type == "application/pdf":
            st.success("File uploaded successfully! Please wait for the summary...")
        else:
            st.error("Please upload a valid PDF file.")
    else:
        st.warning("Please upload a file.")


##
# raw_text =''
# cleaned_text=''
# title=''
# # Function to extract text from PDF using PDFMiner
# def extract_text_from_pdf(pdf_path):
#     return extract_text(pdf_path)

   
# #Function to get the title
# def get_title(text):
#     match = re.search(r"\d+\s*\n\n(.*?)\n", text, re.DOTALL)
#     if match:
#         return match.group(1).strip()
#     else:
#         return None

# #function for preprocessing text
# def preprocess_text(text):
#   processed_text = re.sub(r'Reprint 2024-25|\d|\d+\s+Footprints without Feet|Footprints without Feet|A Triumph of Surgery\s\d|READ AND FIND OUT[\s\S]*?(?:•\s.*\n)+', '', text)
  
#   # Replace multiple spaces with a single space
#   processed_text = re.sub(r'\s+', ' ', processed_text)

#   author_pattern = r'\b[A-Z]+\s+[A-Z]+\b'
#   processed_text = re.sub(author_pattern, '', processed_text)

#   # Strip leading and trailing whitespace
#   processed_text = processed_text.strip()

#   return processed_text

# #function to multiple occurrences of the title
# def remove_subsequent_occurrences(text, phrase):
#     parts = text.split(phrase)
#     return phrase + parts[1] + "".join(parts[2:])


# #function to get separate sections from the extracted text
# def separate_sections(text):
#   # Define the regex patterns to extract the sections
#   glossary_pattern = re.compile(r'GLOSSARY(.*?)Think about it', re.DOTALL)
#   think_about_it_pattern = re.compile(r'Think about it(.*?)Talk about it', re.DOTALL)
#   talk_about_it_pattern = re.compile(r'Talk about it(.*?)Suggested reading', re.DOTALL)
#   suggested_reading_pattern = re.compile(r'Suggested reading(.*)', re.DOTALL)


#   # Extract the sections using the patterns
#   main_content = re.split(r'GLOSSARY|Think about it|Talk about it|Suggested reading', text)[0].strip()
#   glossary = glossary_pattern.search(text)
#   think_about_it = think_about_it_pattern.search(text)
#   talk_about_it = talk_about_it_pattern.search(text)
#   suggested_reading = suggested_reading_pattern.search(text)

#   glossary = glossary.group(1).strip() if glossary else ''
#   think_about_it = think_about_it.group(1).strip() if think_about_it else ''
#   talk_about_it = talk_about_it.group(1).strip() if talk_about_it else ''
#   suggested_reading = suggested_reading.group(1).strip() if suggested_reading else ''

#   # Return the extracted sections
#   return main_content, glossary, think_about_it, talk_about_it, suggested_reading


# # Function to summarize text with sumy (extractive)
# def summarize_text_sumy(text, sentences_count=5):
#     parser = PlaintextParser.from_string(text, Tokenizer("english"))
#     summarizer = LexRankSummarizer()
#     summary = summarizer(parser.document, sentences_count)
#     return " ".join([str(sentence) for sentence in summary])


# # Load summarization pipeline
# summarizer = pipeline('summarization',model="Falconsai/text_summarization")

# # Function to split text into chunks
# def split_text(text, chunk_size=1024):
#     return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

# # Function to summarize text with transformers (abstractive)
# # def summarize_with_transformers(text, default_max_length=130, min_length=30):
# #     chunks = split_text(text)
# #     summaries = []
# #     for chunk in chunks:
# #         # Adjust max_length based on the length of the chunk
# #         chunk_length = len(chunk)
# #         max_length = min(default_max_length, chunk_length // 2)  # Ensure max_length is not greater than half the chunk size
# #         summary = summarizer(chunk, max_length=max_length, min_length=min_length, do_sample=False)
# #         summaries.append(summary[0]['summary_text'])
# #     return " ".join(summaries)

# # Function to summarize a single chunk
# def summarize_chunk(chunk, default_max_length=130, min_length=30):
#     chunk_length = len(chunk)
#     max_length = min(default_max_length, chunk_length // 2)
#     summary = summarizer(chunk, max_length=max_length, min_length=min_length, do_sample=False)
#     return summary[0]['summary_text']

# def summarize_with_transformers(text, default_max_length=130, min_length=30):
#     chunks = split_text(text)
#     summaries = []

#     # Use ThreadPoolExecutor to process chunks concurrently
#     with ThreadPoolExecutor() as executor:
#         results = list(executor.map(lambda chunk: summarize_chunk(chunk, default_max_length, min_length), chunks))

#     return " ".join(results)

# if uploaded_file is not None:
#     if uploaded_file.type == "application/pdf":
#         # Ensure the directory exists
#         upload_dir = "uploaded_files"
#         if not os.path.exists(upload_dir):
#             os.makedirs(upload_dir)
#         # Save the uploaded file
#         save_path = os.path.join("uploaded_files", uploaded_file.name)
#         with open(save_path, "wb") as f:
#             f.write(uploaded_file.getbuffer())

#         raw_text = extract_text_from_pdf(save_path) 
#         title = get_title(raw_text)
#         cleaned_text = preprocess_text(raw_text)
#         cleaned_text = remove_subsequent_occurrences(cleaned_text, title)
#         main_content, glossary, think_about_it, talk_about_it, suggested_reading = separate_sections(cleaned_text)
#         # summary_sumy = summarize_text_sumy(main_content)
#         # st.text_area("Extracted Text from PDF:", summary_sumy, height=300)
#         summary_transformers = summarize_with_transformers(main_content)
#         st.text_area(f"Summary of {title}:", summary_transformers, height=300)










# Footer
st.markdown("***")
st.write("© 2024 Future Minds Tutoring. All rights reserved.")
