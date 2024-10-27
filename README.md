Here's the content rewritten as a Markdown file:


# Job Post Info Scraper

## Project Description

The **Job Post Info Scraper** is a web scraping tool designed to extract job postings from career pages or job postings. It intelligently parses the scraped text, organizes the information, and returns it in a valid JSON format.

### How It Works

1. **Input**: The application accepts URL of website's career page or job post.
2. **Output**: The app returns the extracted information in a structured JSON format.

### Use Cases

This application is ideal for job boards, recruitment agencies, or companies seeking to aggregate job listings from multiple sources efficiently. It streamlines the process of converting unstructured job postings into structured data, making it easier to analyze and present to potential candidates.(This might not work for some websites)

## Technologies Used

* **FastAPI**: For building the web application.
* **Python**: The programming language used for the application.
* **Selenium**: For automating web browsers to navigate and interact with web pages.
* **Groq Cloud**: Leveraging the powerful **LLAMA 3.2 model (llama-3.2-90b-text-preview)** provided by Groq Cloud, enabling advanced natural language processing capabilities.

## Setup Instructions

### 1. Create a Virtual Environment

To avoid package conflicts, create a virtual environment for the project:

```bash
python -m venv venv
```

### 2. Activate the Virtual Environment

Activate the virtual environment using the following command:

**On Windows:**
```bash
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

Once the virtual environment is activated, install the required dependencies:

```bash
pip install requirements.txt
```

### 4. Run the Application

To start the FastAPI application, run the following command:

```bash
uvicorn main:app --reload
```
**Note:** Ensure that your `main.py` file contains the FastAPI app instance named `app`.
```