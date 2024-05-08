from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from fastapi_utils.tasks import repeat_every
import os
import io
import requests

app = FastAPI()


@app.on_event("startup")
@repeat_every(seconds=60 * 12)  # 1 hour
async def refresh_the_api():
    
    url = "https://research-project-h4fb.onrender.com/refresh_api"
    
    payload = {}
    headers = {
      'accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    print(response.text)
    return response.text


@app.get("/test")
async def read_root():
    return {"message":"running"}
    

@app.get("/start_model_trigger")
async def model_trigger(page: int):
    while True:
        try:
            page_str = str(page)
            url = f"https://api-ai-service.transexpress.lk/trigger_the_data_fecher?page={page_str}&paginate=10000"
            print(url, page_str)

            payload = {}
            headers = {
                'accept': 'application/json'
            }

            response = requests.request("GET", url, headers=headers, data=payload)

            # Check if the response status code is 200
            if response.status_code != 200:
                break

            page += 1
            print(response.text)

        except Exception as e:
            print(f"An error occurred: {e}")
            break

    return {"last_processed_page": page}


