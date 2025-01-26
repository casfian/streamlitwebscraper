import streamlit as st
import requests
from bs4 import BeautifulSoup
import ollama

# Function to scrape the website
def scrape_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extracting the text of the first <h1> tag for demonstration
    heading = soup.find('h1').get_text() if soup.find('h1') else 'No H1 tag found'
    
    # Extracting the first paragraph text
    paragraph = soup.find('p').get_text() if soup.find('p') else 'No paragraph found'
    
    return heading, paragraph

# Function to query the local LLM using Ollama
def query_llm(prompt):
    response = ollama.chat(model="llama2", messages=[{"role": "user", "content": prompt}])
    return response['text']

# Streamlit app layout
st.title("Web Scraper with Local LLM")

# Input URL
url = st.text_input("Enter the URL to scrape:")

if url:
    try:
        # Scrape data from the website
        heading, paragraph = scrape_website(url)
        
        # Show scraped data
        st.subheader("Scraped Content")
        st.write(f"Heading: {heading}")
        st.write(f"Paragraph: {paragraph}")
        
        # Process the scraped content using Ollama
        prompt = f"Summarize the following content:\nHeading: {heading}\nParagraph: {paragraph}"
        st.subheader("LLM Response")
        llm_response = query_llm(prompt)
        st.write(llm_response)
        
    except Exception as e:
        st.error(f"Error while scraping the website: {e}")
