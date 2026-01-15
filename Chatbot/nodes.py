import os
from typing import List
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.document_loaders import WebBaseLoader
from pydantic import BaseModel, Field

# Load keys (assumed loaded in main or via dotenv load_dotenv call before this runs, 
# but good practice to explicitly load if running standalone).
from dotenv import load_dotenv
load_dotenv()

# --- LLM Setup ---
llm = ChatGroq(model="llama-3.3-70b-versatile") # Using a capable model available on Groq

# --- State Definition (Shared with graph.py, but useful to have reference or definitions here if independent) ---
# For nodes, we just need to know the dict types.

# --- Node 1: Query Optimizer ---
class QueryOutput(BaseModel):
    queries: List[str] = Field(description="List of 2-3 specific search queries")

def query_optimizer(state):
    company = state['company']
    print(f"--- Optimizing Queries for {company} ---")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a research expert. Generate 2-3 specific, high-value search queries to gather comprehensive intelligence on the given company. Focus on: latest product launches, financial reports, strategic acquisitions, and market sentiment. Return JSON."),
        ("human", "Company: {company}")
    ])
    
    chain = prompt | llm.with_structured_output(QueryOutput)
    response = chain.invoke({"company": company})
    
    return {"queries": response.queries}

# --- Node 2: Information Retrieval (Tavily) ---
def information_retrieval(state):
    queries = state['queries']
    print(f"--- Searching Tavily for: {queries} ---")
    
    # We can perform searches in parallel or sequential. Sequential for simplicity here.
    # search_depth="advanced" is a param for TavilyClient, usually exposed via wrapper or args.
    # TavilySearchResults tool wraps the client.
    
    tavily_tool = TavilySearchResults(max_results=2, search_depth="advanced") 
    
    all_results = []
    urls = set()
    
    for q in queries:
        try:
            results = tavily_tool.invoke({"query": q})
            for r in results:
                if r['url'] not in urls:
                    all_results.append(r)
                    urls.add(r['url'])
        except Exception as e:
            print(f"Error searching for {q}: {e}")
            
    # Limit to top 3 unique URLs to avoid overloading scraper
    top_urls = list(urls)[:3]
    return {"search_results": all_results, "urls": top_urls}

# --- Node 3: Content Scraper ---
def content_scraper(state):
    urls = state['urls']
    print(f"--- Scraping URLs: {urls} ---")
    
    scraped_content = []
    
    # Using WebBaseLoader
    try:
        loader = WebBaseLoader(urls)
        # Verify ssl=True/False depending on environment, usually True is fine.
        # Set requests kwargs if needed.
        docs = loader.load()
        
        for doc in docs:
            # Accumulate content until we hit a safe limit for the 12k TPM Tier
            # 12,000 tokens ~= 48,000 chars. We need to leave room for prompts and generation.
            # Let's limit the TOTAL input context to ~15,000 chars (approx 3,750 tokens).
            
            current_length = sum(len(c) for c in scraped_content)
            if current_length > 15000:
                break
                
            # Take a chunk from this doc
            remaining_space = 15000 - current_length
            chunk_size = min(2000, remaining_space)
            
            if chunk_size <= 0:
                break
                
            content = doc.page_content[:chunk_size]
            if content.strip():
                scraped_content.append(f"Source: {doc.metadata.get('source', 'Unknown')}\nContent: {content}\n")
            
    except Exception as e:
        print(f"Error scraping: {e}")
        scraped_content.append(f"Error scraping content.")

    return {"scraped_content": "\n\n".join(scraped_content)}

# --- Node 4: Information Synthesizer ---
def information_synthesizer(state):
    raw_text = state['scraped_content']
    company = state['company']
    print(f"--- Synthesizing Information for {company} ---")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an intelligence analyst. Analyze the following raw text about {company}. Extract key facts, financial data, and strategic moves. Discard fluff. specific focus: Recent News, Strategic Moves, Sentiment."),
        ("human", "Raw Content:\n\n{raw_text}")
    ])
    
    chain = prompt | llm | StrOutputParser()
    synthesis = chain.invoke({"company": company, "raw_text": raw_text})
    
    return {"synthesis": synthesis}

# --- Node 5: Report Generator ---
def report_generator(state):
    synthesis = state['synthesis']
    company = state['company']
    print(f"--- Generating Report for {company} ---")
    
    # Sleep to avoid hitting Rate Limits (TPM)
    import time
    time.sleep(2)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a senior business consultant. Format the provided analysis into a professional report for {company}. \nSections required:\n1. Recent News\n2. Strategic Moves\n3. SWOT Analysis (derive this)\n4. Sentiment Analysis\n\nOutput in Markdown."),
        ("human", "Analysis:\n{synthesis}")
    ])
    
    chain = prompt | llm | StrOutputParser()
    report = chain.invoke({"company": company, "synthesis": synthesis})
    
    return {"report": report}
