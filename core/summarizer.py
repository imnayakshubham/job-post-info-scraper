
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from configuration.config import settings


class Prediction:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, groq_api_key=settings.GROQ_API_KEY, model_name="llama-3.2-90b-text-preview")

    def extract_job_information(self, job_page_content):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {job_page_content}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website or a job post. 
            Extract job postings from the input text and return them in valid JSON format with the following keys: `job_role`, `job_experience`, `required_skills`, `job_description`, `job_salary`, `company_culture`, `company_info`, `is_job_post`. If any key has no data, set its value to None. Set `is_job_post` to `true` if it's a valid job post, otherwise `false` and also add a key `reason` to know the actual reason make sure it does not sound like this was done by automated script. 
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"job_page_content": job_page_content})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]
    
    def create_random_questions(self, topic, complexity_level="easy"):
        prompt_extract = PromptTemplate.from_template(
            """
            You are an expert question generator. Your task is to create a list of 20 unique challenging multiple-choice questions on the topic of {topic}, at a {complexity_level} complexity level.
            Such that it should return a json object containing two keys questions, answers
            
            ### In questions 
            Each question should be formatted as valid JSON, including the following fields:
            id: A uuid for uniquely identifying the question
            question: A string containing the question.
            options: An object with four options as key-value pairs (keys: "A", "B", "C", "D").
            
            ### In result object:
            uuid as the key and nested value of the key to be  
            answer: The correct option (one of "A", "B", "C", or "D").
            explanation: A brief explanation of why the answer is correct.
            
            Each question should have exactly one correct answer, with the other options being plausible but incorrect.
            
            ### STRICT Return Format:
            Output as a valid json object containing two keys questions, answers, without any additional text or preamble.

            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"topic": topic, "complexity_level":complexity_level})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res