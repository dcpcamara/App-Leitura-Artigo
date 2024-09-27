# Daniel C. P. Câmara
# AI app designed to help busy researchers go through their crescent number of unread papers.

# conda env create -f environment.yml

# conda activate paper_app

# streamlit run app.py

# LIBRARIES AND SETUP
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.summarize import load_summarize_chain

import streamlit as st
import os
from tempfile import NamedTemporaryFile
import yaml

# Load API Key
OPENAI_API_KEY = yaml.safe_load(open('credentials.yml'))['openai']

# 1.0 LOAD AND SUMMARIZE FUNCTION
def load_summarize(file):
    with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(file.getvalue())
        file_path = tmp.name
    
    try:
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        model = ChatOpenAI(
            model="gpt-3.5-turbo", 
            temperature=0, 
            api_key=OPENAI_API_KEY
        )
        
        prompt_template = """
        You are a helpful research assistant. You are specialized in public health, epidemiology of transmissible diseases, and epidemiology of non-transmissible diseases. Write a report from the following peer-reviewed scientific paper:
        {paper}
        
        Use the following Markdown format:
        # Abstract
        Begin the section with the full title of the paper followed by the full name of the first author. If there is more than one author, mention them as colleagues. Then, copy and paste the abstract without changing a single word.
        
        ## Introduction
        Use 3 to 7 numbered bullet points
        
        ## Methodology
        Describe the whole methodology section, including statistical analysis and statistical modelling if available. Use 3 to 10 numbered bullet points.
        
        ## Results
        Describe the main findings of the paper. Use 3 to 10 numbered bullets.
        
        ## Discussion and conclusions
        Read and summarize the most important points in the discussion section. Conclude with any future steps that the authors might discuss. Use 3 to 10 numbered bullets. 
        
        ## Most cited papers
        Finish with 1 to 5 numbered bullet points showing the most cited references in the paper.
        """
        
        prompt = PromptTemplate(input_variables=["paper"], template=prompt_template)
        llm_chain = LLMChain(prompt=prompt, llm=model)
        stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="paper")
        response = stuff_chain.invoke(docs)
        
    finally:
        os.remove(file_path)
    
    return response["output_text"]

# 2.0 STREAMLIT INTERFACE
st.title("Busy Scientist App")
st.subheader("Upload a PDF document:")

uploaded_file = st.file_uploader("Choose a file", type="pdf")

if uploaded_file is not None:
    if st.button("Summarize paper"):
        with st.spinner("Summarizing..."):
            summary = load_summarize(uploaded_file)
            st.subheader("Summarization results:")
            st.markdown(summary)
            
else:
    st.write("No file uploaded. Please upload a PDF file.")
