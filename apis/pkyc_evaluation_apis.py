import json
from main import app, Depends, get_api_key
from pydantic import BaseModel

''' 
    POST API CALL Params (Input Validator)

    - This model describes what payload your POST API is expects.
    - This model is requrired to generate an OpenAPI spec file with proper input definition.
'''

class UserDetails(BaseModel):
    name: str
    description: str
    country: str

''' 
    API CALL SUCCESS VALIDATOR MODELS (Output Validator)

    - This model describe what to expect in case of a successful response.
    - This model is requrired to generate an OpenAPI spec file with proper output definition.
'''

class PostValidatorSuccess(BaseModel):
    name: str
    pep: str
    georisk: str

''' 
    API CALL ERROR VALIDATOR MODELS (Error Validator)
    
    - These models describe what output to expect in case of an error.
    - These models are required to generate an OpenAPI spec file with proper error handling definition.
'''

class PostValidatorError(BaseModel):
    detail: str = 'Validation Error Occurred'


class PostValidatorError2(BaseModel):
    detail: str = 'Invalid credentials'


''' 
    HANDLE RESPONSES 

    - Define how 2xx, 3xx, 4xx, 5xx responses look like.
    - The OpenAPI spec json will have these details.
'''

def handleResponse():
    return {
        200: {
            'model': PostValidatorSuccess,
            'description': 'A successful response will look something like this'
        },
        400: {
            'model': PostValidatorError2,
            'description': 'A response with invalid username/password will look something like this'
        },
        422: {
            'model': PostValidatorError,
            'description': 'A failed response will look something like this'
        }
    }

''' 
    API ROUTES 

    - Define the API routes
'''
api_url = "/api/v1/getpep"
api_details = "API to check PEP & GEO Risk"
api_tags = ["watsonx.ai"]

@app.post(api_url, tags=api_tags, responses=handleResponse(), summary=api_details)
async def PostMethod(req: UserDetails, api_key_valid: bool = Depends(get_api_key)):
    
    # Here 'req' holds values from class UserDetails(BaseModel) defined on line no 12. We can covert it to Json to handle it better in the backend.
    requestObject = req.model_dump(mode='json')
    
    # -------------- Invoke Business Logic here and get output --------------
    from src.pkyc_evaluation import WatsonX
    obj = WatsonX() 
    output = obj.generate(
        input_object=requestObject
    )
    # -----------------------------------------------------------------------
    
    
    return output
