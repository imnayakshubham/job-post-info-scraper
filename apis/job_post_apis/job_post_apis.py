from fastapi import APIRouter, Request, HTTPException
from apis.job_post_apis.job_post_apis_schema import SummarizeJobPostSchema
from core.summarizer import Summarizer
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException
import time
import re
import random
from fake_useragent import UserAgent

CREATE_SUMMARY = f"/create_job_post_summary"

def clean_text(text):
    # Remove HTML tags
    text = re.sub(r'<[^>]*?>', '', text)
    text = re.sub(r'/', ' or ', text)
    # Remove URLs
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    # Remove special characters
    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)
    # Replace multiple spaces with a single space
    text = re.sub(r'\s{2,}', ' ', text)
    # Trim leading and trailing whitespace
    text = text.strip()
    # Remove extra whitespace
    text = ' '.join(text.split())
    return text


router = APIRouter()
ua = UserAgent()


def get_webdriver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"user-agent={ua.random}")
    chrome_options.add_argument("--window-size=1920,1080")
    # chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
    
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })
    return driver
    

@router.post(CREATE_SUMMARY)
async def create_job_post_summary(request: Request, payload:SummarizeJobPostSchema):
    url = payload.job_post_url
    driver = get_webdriver()
    try: 
        driver.set_page_load_timeout(30)
        driver.get(url)
        time.sleep(random.uniform(2, 10))
        body_content = driver.find_element("tag name", "body").text
        
        if not body_content:
            raise HTTPException(status_code=404, detail="No content found on the page or Unable to fetch Content")
        
        cleaned_content = clean_text(body_content)
        
        if cleaned_content:
            llm = Summarizer()
            job_page_content = llm.extract_job_information(cleaned_content)
        
        return {
            "url": url,
            "content": job_page_content,
        }
        
    except TimeoutException:
        raise HTTPException(status_code=504, detail="Request timed out while loading the page")
        
    except WebDriverException as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve content")
        
    finally:
        driver.quit()