# BUSINESS SCIENCE UNIVERSITY
# PYTHON FOR GENERATIVE AI COURSE
# FIRST AI-POWERED BUSINESS APP: PART 2
# ***
# GOAL: Exposure to using LLM's, Document Loaders, and Prompts

# streamlit run 02_document_summarizer_app.py


import yaml
import subprocess

from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain 
from langchain.chains.combine_documents.stuff import StuffDocumentsChain

import streamlit as st
import subprocess
import shutil
import os
from tempfile import NamedTemporaryFile

# Load API Key
#'''Use when credentials are specified in dict format'''
#OPENAI_API_KEY = yaml.safe_load(open('credentials.yml'))['openai']
OPENAI_API_KEY = yaml.safe_load(open('credentials.yml'))
model = ChatOpenAI(
    model = "gpt-4o-mini",
    temperature=0,
    api_key=OPENAI_API_KEY
    )

def generate_pdf_with_quarto(markdown_text): 
    with NamedTemporaryFile(delete=False, suffix=".qmd", mode='w') as md_file:
        md_file.write(markdown_text)
        md_file_path = md_file.name

    pdf_file_path = md_file_path.replace(".qmd",".pdf")

    subprocess.run(["quarto","render",md_file_path,"--to","pdf"], check=True)

    os.remove(md_file_path)
    return pdf_file_path

def move_file_to_downloads(pdf_file_path):
    downloads_path = os.path.join(os.path.expanduser('~'),'Downloads')
    destination_path = os.path.join(downloads_path, os.path.basename(pdf_file_path))
    shutil.move(pdf_file_path,destination_path)
    return destination_path



# 1.0 LOAD AND SUMMARIZE FUNCTION
def load_summarize(file, user_template=False):
    with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(file.getvalue())
        file_path = tmp.name 

    


    try:
        loader = PyPDFLoader(file_path)
        docs = loader.load()


        if user_template: 
            #Bullet
            prompt_template = """
            Write a concise summary of the following 
            {text} 

           Use the following Markdown format:
                   # Insert Descriptive Report Title
           
                   ## Earnings Call Summary
                   Use 3 to 7 numbered bullet points
           
                   ## Important Financials:
                   Describe the most important financials discussed during the call. Use 3 to 5 numbered bullet points.
           
                   ## Key Business Risks
                   Describe any key business risks discussed on the call. Use 3 to 5 numbered bullets.
           
                   ## Conclusions
                   Conclude with any overaching business actions that the company is pursuing that may have a positive or negative implications and what those implications are. 
            """

            prompt = PromptTemplate.from_template(prompt_template)
            llm_chain =LLMChain(prompt=prompt, llm = model)
            stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")

            response = stuff_chain.invoke(docs)

        else:
            #No Bullets
            summarizer_chain = load_summarize_chain(llm=model, chain_type ="stuff")

            response = summarizer_chain.invoke(docs)

    finally:
        os.remove(file_path)

    return response['output_text']







# 2.0 STREAMLIT INTERFACE  
st.set_page_config(layout='wide',page_title="Pdf Summarizer")
st.title("PDF Summarizer") 
col1, col2 = st.columns(2)

with col1:
    st.subheader('Upload a PDF document:')
    uploaded_file = st.file_uploader("Choose a file", type="pdf", key="file_uploader")
    if uploaded_file:
        summarize_flag = st.button('Summarize Document', key="summarize_button")



if uploaded_file is not None: 
    with col1:
        use_template = st\
            .checkbox("Use numbered bullet points? (if not paragraph will be returned)")
    with col2:    
    
        with st.spinner('Summarizing...'):
            summary = load_summarize(uploaded_file, use_template)
            st.subheader('Summarization Result:')
            st.markdown(summary)
                    
            pdf_file = generate_pdf_with_quarto(summary)
            download_path = move_file_to_downloads(pdf_file)
            st.markdown(f"**PDF Downloaded to your Downloads folder: {download_path}**")
        

           

else: 
    with col2:
        st.write("No file uploaded. Please Upload a Pdf file.")



# CONCLUSIONS:
#  1. WE CAN SEE HOW APPLICATIONS LIKE STREAMLIT ARE A NATURAL INTERFACE TO AUTOMATING THE LLM TASKS
#  2. BUT WE CAN DO MORE. 
#     - WHAT IF WE HAD A FULL DIRECTORY OF PDF'S?
#     - WHAT IF WE WANTED TO DO MORE COMPLEX ANALYSIS?
