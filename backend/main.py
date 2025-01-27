from fastapi import FastAPI
import openai
import os
from dotenv import load_dotenv
from pydantic import BaseModel

class TextInput(BaseModel):
    text: str  # The field to accept unstructured text

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")  # Add your OpenAI API key here
client = openai.OpenAI()
app = FastAPI()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)

@app.get("/ok")
async def ok_endpoint():
    return {"message": "hello world"}

@app.post("/askchat")
async def askchat_endpoint(input: TextInput):
    #quant item, quant item, ....
    #cancel order num
    message = input.text
    prompt = f''' 
        You are a drive thru ordering system that allows customers to place or cancel their orders.
        There are three order items :  1) burgers, 2) fries, or 3) drinks.
        Orders can contain one or multiple items and 1 or multiple quantities of each item  
        If they are requesting an order please respond by stating the quantity followed by a space followed by the item name followed by a comma then a space.
        for example: 1 burger, 2 drinks, 3 fries
        If the user is requesting to cancel the item, expect a order number to cancel. Your response to cancellations should be the word cancel followed
        by a space followed by the word order followed by the order number. 
        for example: cancel order 4
        You are given the following request:"{message}", please respond accordingly
    '''
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "developer", "content": f"{prompt}"},
            {
                "role": "user",
                "content": f"{prompt}"
            }
        ]
    )

    return {"message": f"{completion.choices[0].message}"}