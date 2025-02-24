import streamlit as st
import pandas as pd
import os

def generate_llm_txt(df, business_description):
    """Generate an llm.txt file from the uploaded CSV data."""
    file_path = "llm.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"> Business Description: {business_description}\n\n")
        
        for _, row in df.iterrows():
            url = row["Address"]
            title = row["Title 1"]
            description = row["Meta Description 1"]
            f.write(f"- [{title}]({url}): {description}\n")
    return file_path

# Streamlit UI
st.title("LLM.txt Generator")
st.write("Upload a cleaned CSV file with 'Address', 'Title 1', and 'Meta Description 1'.")

# Input for Business Description
business_description = st.text_input("Enter a Business Description:")

# File uploader
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        required_columns = ["Address", "Title 1", "Meta Description 1"]
        
        # Check for missing columns
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            st.error(f"Missing columns: {', '.join(missing_columns)}")
        else:
            if st.button("Generate llm.txt"):
                file_path = generate_llm_txt(df, business_description)
                
                # Provide a download link
                with open(file_path, "rb") as f:
                    st.download_button(
                        label="Download llm.txt",
                        data=f,
                        file_name="llm.txt",
                        mime="text/plain"
                    )
                
                # Clean up the file
                os.remove(file_path)
    except Exception as e:
        st.error(f"Error processing file: {e}")

# Sidebar for app instructions
st.sidebar.title("Hello, My Good Friend")
st.sidebar.markdown("""

This tool helps you create LLM.txt files for your website

An llms.txt file is a standardized markdown file that helps LLMs like chagpt, llama, claude, gemini, grok etc  use your website at inference time. 

Once created the file should be embedded at the root folder of your site in the same way that sitemap and robots.txt files are embedded

How llm.txt files differ from sitemaps and robots.txt files
- **/sitemap.xml lists all indexable pages, but doesn’t help with content processing. AI systems would still need to parse complex HTML and handle extra info, cluttering up the context window**
- **/robots.txt suggests search engine crawler access, but doesn’t assist with content understanding either**
- **/llms.txt solves AI-related challenges. It helps overcome context window limitations, removes non-essential markup and scripts, and presents content in a structure optimized for AI processing**
""")
