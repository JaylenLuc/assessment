from fastapi import FastAPI, Response
import openai
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

class TextInput(BaseModel):
    text: str  # The field to accept unstructured text

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")  # Add your OpenAI API key here
client = openai.OpenAI()
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins in development
    allow_credentials=False,  # Changed to False since we're allowing all origins
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # Allow external connections
        port=8000,
        reload=True
    )


@app.get("/")
async def first_endpoint():
    return {"message": "app works"}


@app.get("/ok")
async def ok_endpoint():
    return {"message": "hello world"}

@app.options("/askchat")
async def options_handler():
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Max-Age": "3600",
        }
    )
@app.post("/askchat")
async def askchat_endpoint(input : TextInput):
    #quant item, quant item, ....
    #cancel order num
    #print("HERE")
    message = input.text
    #print("messsage: ", message)
    prompt = f''' 
        You are a drive thru ordering system that allows customers to place or cancel their orders.
        There are only three order items :  1) burgers, 2) fries, or 3) drinks.
        Orders can contain one or multiple items and 1 or multiple quantities of each item  
        If they are requesting an order please respond by stating the quantity followed by a space followed by the item name followed by a comma then a space.
        For the last item or if there is only one kind of item, omit the comma and space after it
        for example: 1 burger, 2 drinks, 3 fries
        If the user is requesting to cancel the item, expect a order number to cancel. Your response to cancellations should be the word cancel followed
        by a space followed by the word order followed by the order number. 
        for example: cancel order 4
        If the request does not meet any of these rules then please quickly respond with : "invalid".
        Users can request these orders in a wide range of ways so dont be too strict, it just has to imply that they want to either cancel an order number or order any number of those three items
        You are given the following request:"{message}", please respond accordingly
    '''
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"{prompt}"},
            {
                "role": "user",
                "content": f"{message}"
            }
        ]
    )
    #return {"message": f"{message}"}
    completion_obj = completion.choices[0].message.content
    print("order: ", completion_obj)
    return {"message": f"{completion_obj}"}