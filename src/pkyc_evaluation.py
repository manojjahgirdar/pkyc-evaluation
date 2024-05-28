import os
import json
from ibm_watsonx_ai.foundation_models import Model

class WatsonX():

    # Constructor
    def __init__(self) -> None:
        self.ibm_cloud_api_key=os.getenv('IBM_CLOUD_API_KEY')
        self.project_id=os.getenv('PROJECT_ID')
    
    # Methods
    def generate(self, input_object):
        input_text = json.dumps(input_object, indent=2)
        print("[DEBUG]: Received input_object:\n", input_text)
        
        response = {
            "name": input_object.get('name'),
            "pep": self.getPep(input_object.get('description')),
            "georisk": self.getGeoRisk(input_object.get('country'))
        }
        
        return response

    def getPep(self, input_text):

        model_id = "mistralai/mixtral-8x7b-instruct-v01"

        parameters = {
            "decoding_method": "greedy",
            "max_new_tokens": 3,
            "repetition_penalty": 1
        }

        model = Model(
            model_id = model_id,
            params = parameters,
            credentials = {
                "url": "https://us-south.ml.cloud.ibm.com",
                "apikey" : self.ibm_cloud_api_key
            },
            project_id = self.project_id
        )

        prompt_input = """Act as a Legal advocate for a bank. It is the year 2024. Evaluate the person's details provided by the user and classify whether the person is Politically Exposed Person (PEP) or not. Refer to the examples provided to understand the context. Generate the output as Yes or No. Don't add anything additional.

Input: Mark Pettingill is the former Member of Parliament since 2012 - 2017.
Output: No

Input: """ + input_text + """
Output: """

        response = model.generate_text(prompt=prompt_input, guardrails=False)
        response = response.replace("\n", "")
        response = response.strip()
        return response
    
    def getGeoRisk(self, input_text):

        model_id = "mistralai/mixtral-8x7b-instruct-v01"

        parameters = {
            "decoding_method": "greedy",
            "max_new_tokens": 7,
            "stop_sequence": ["\n"],
            "repetition_penalty": 1
        }

        model = Model(
            model_id = model_id,
            params = parameters,
            credentials = {
                "url": "https://us-south.ml.cloud.ibm.com",
                "apikey" : self.ibm_cloud_api_key
            },
            project_id = self.project_id
        )

        prompt_input = """Classify the given country as High, Medium or Low based on FATF Geographical risk. Generate the output as Low, Medium or High.

Don't add anything additional.

Input: """ + input_text + """
Output: """

        response = model.generate_text(prompt=prompt_input, guardrails=False)
        response = response.split('\n\n')[0]
        response = response.replace("\n", "")
        response = response.strip()
        return response