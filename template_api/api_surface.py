from fastapi import FastAPI
from pydantic import BaseModel 
import uvicorn 
import json 


app = FastAPI()

class model_input(BaseModel): 

    Platform: str
    Project: str
    Dataset: str
    Table: str 
    Column: str 


def classify_column(x:str):
    return True 


@app.post("/")
async def api(input_parameters: model_input): 

    input_data = input_parameters.json()
    input_dict = json.loads(input_data)

    if "Column" not in input_dict.keys(): 
        return "Column name field is Empty"
    
    if input_dict["Column"] == "" : 
        return "Column name field is empty"

    LLM_response = classify_column (input_dict["Column"])

    input_dict.update({"PII": LLM_response, 
                       "PCI": None, 
                       "Description": None, 
                       "Security Classification": None})
    return input_dict 
    

if __name__ == "__main__": 
    host = "0.0.0.0"
    uvicorn.run(app, host=host, port=8000)

#go to http://127.0.0.1:8000