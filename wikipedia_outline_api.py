from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"] , # Allows all methods
    allow_headers=["*"]   # Allows all headers
)

@app.get("/")
def read_root():
    return {"message": "FastAPI is working!"}

@app.get("/api/outline")
def get_country_outline(country: str = Query(..., title="Country Name")):
    url = f"https://en.wikipedia.org/wiki/{country.replace(' ', '_')}"
    response = requests.get(url)
    
    if response.status_code != 200:
        return {"error": "Could not fetch Wikipedia page"}
    
    soup = BeautifulSoup(response.text, "html.parser")
    headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
    
    markdown_outline = "## Contents\n\n"
    
    for heading in headings:
        level = int(heading.name[1])  # Extract heading level (h1-h6)
        markdown_outline += "#" * level + " " + heading.text.strip() + "\n\n"
    
    return {"country": country, "outline": markdown_outline, "source": url}
