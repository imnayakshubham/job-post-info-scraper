
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from configuration.config import settings


class Summarizer:
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