from fastapi import APIRouter, Request, HTTPException, UploadFile,File
from apis.job_post_apis.job_post_apis_schema import SummarizeJobPostSchema,RandomQuestionsSchema
from core.summarizer import Prediction
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
from selenium_stealth import stealth
from selenium.webdriver.common.action_chains import ActionChains
from datetime import date
import os
import uuid
import json

import PyPDF2
from pdfminer.high_level import extract_text
from io import BytesIO

CREATE_SUMMARY = f"/create_job_post_summary"
CREATE_QUESTIONS = f"/create_questions"




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


def random_window_size(max_width=1920, max_height=1080):
    width = random.randint(800, max_width)  # Set a reasonable minimum width
    height = random.randint(600, max_height)  # Set a reasonable minimum height
    return f"{width},{height}"


def random_mouse_movements(driver, num_movements=10):
    action = ActionChains(driver)
    for _ in range(num_movements):
        # Generate random x and y positions within the window
        x = random.randint(0, driver.execute_script("return window.innerWidth") - 1)
        y = random.randint(0, driver.execute_script("return window.innerHeight") - 1)
        
        # Move to the random location
        action.move_by_offset(x, y)
        action.perform()
        
        # Wait a random amount of time between movements
        time.sleep(random.uniform(0.1, 0.5))
        
        # Reset the offset to avoid cumulative movement
        action.move_by_offset(-x, -y)


def get_webdriver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"--window-size={random_window_size()}")
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
    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )
    
    try: 
        driver.set_page_load_timeout(30)
        driver.get(url)

        time.sleep(random.uniform(1, 5))
        random_mouse_movements(driver, num_movements=20)
        
        for _ in range(random.randint(5, 10)):
            scroll_height = random.randint(100, 800)
            driver.execute_script(f"window.scrollBy(0, {scroll_height})")
            time.sleep(random.uniform(0.5, 1.5))

        body_content = driver.find_element("tag name", "body").text
                
        if not body_content:
            raise HTTPException(status_code=404, detail="No content found on the page or Unable to fetch Content")
        
        cleaned_content = clean_text(body_content)
        
        if cleaned_content:
            llm = Prediction()
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
        
        

def get_todays_date():
    today = date.today()
    formatted_date = today.strftime("%d-%m-%Y")
    return formatted_date


def setup_json_data(base_dir, topic, complexity_level):
    todays_date = get_todays_date()
    key = f"{todays_date}____{topic}____{complexity_level}"
    json_file_path = os.path.join(base_dir, f"{todays_date}.json")

    if os.path.exists(json_file_path):
        with open(json_file_path, "r") as json_file:
            existing_data = json.load(json_file)
            print(existing_data)
    else:
        print("JSON file does not exist. Creating new file...")
        existing_data = {}
        with open(json_file_path, "w") as json_file:
            json.dump(existing_data, json_file)

    existing_data.update({
        random.randint(1, 200): {
            "id": 2,
            "data": "kasdjflfkj"
        }
    })

    with open(json_file_path, "w") as json_file:
        json.dump(existing_data, json_file, indent=4)

    print("Updated data saved:", existing_data)

        
         
@router.post(CREATE_QUESTIONS)
async def create_random_questions(request: Request, payload:RandomQuestionsSchema):
    payload = payload.model_dump()
    topic = payload.get("topic").strip()
    complexity_level= payload.get("complexity_level")
    try: 
        if topic: 
            llm = Prediction()
            base_dir = "database"
            todays_date = get_todays_date()
            key=f"{todays_date}____{topic}____{complexity_level}"
            json_file_path = os.path.join(base_dir,f"{todays_date}.json")
            
            if not os.path.exists(os.path.dirname(json_file_path)):
                os.makedirs(os.path.dirname(json_file_path))
                
                
            if not os.path.exists(json_file_path):
                with open(json_file_path, "w") as json_file:
                    data = {
                        key: {
                            "result":  llm.create_random_questions(topic,complexity_level),
                            "id": str(uuid.uuid4())
                            }
                    }
                    json_object = data
                    json.dump(json_object, json_file)
            else:
                with open(json_file_path, "r+") as json_file:
                    json_object = json.load(json_file)
                    if key in json_object:
                        return {
                            "data": {
                                key:json_object[key]
                            }
                        }
                        
                    data = {
                        key: {
                            "result":  llm.create_random_questions(topic,complexity_level),
                            "id": str(uuid.uuid4())
                            }
                    }
                    json_object.update(data)
                    json_file.seek(0)
                    json.dump(json_object, json_file,indent=4)
                    json_file.truncate()
                
            return {
                "data": data
            }
    except TimeoutException:
        raise HTTPException(status_code=500, detail="Something went Wrong")
        
     
@router.post("/read_pdf")
async def read_pdf(file: UploadFile = File(...)):
    pdf_reader = PyPDF2.PdfReader(file.file)

    bio = BytesIO()
    file.file.seek(0)
    bio.write(file.file.read())
    file.file.seek(0)
    pdf_reader = PyPDF2.PdfReader(bio)
    text = extract_text_data(bio)
    return {"text": text}


def extract_text_data(file):
    return extract_text(file)