from typing import Union, List
from collections import defaultdict

from fastapi import FastAPI
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware

from model import predict_next_site

# start with uvicorn main:app --reload

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def format_link(link):
    link = link[1:]
    link = link.split("-")
    link = ' '.join([p.capitalize() for p in link])
    return link

class ClientData(BaseModel):
    uri: str
    client_id: str

class ResponseLink(BaseModel):
    href: str
    title: str

class Response(BaseModel):
    suggestions: List[ResponseLink]

def predict_results(user_history: List[str]) -> List[ResponseLink]:
    """
    TODO: Predict the next webpages for the user to visit,
    return them as a list of ResponseLink type
    """
    print("History for this client:")
    print(user_history)
    # Run some ML model here
    
    predictions = predict_next_site(user_history)
    
    return [
        ResponseLink(href=p, title=format_link(p)) for p in predictions
    ]


client_history = defaultdict(lambda: [])

@app.post("/")
async def get_navigation(client_data: ClientData) -> Response:
    # only add url if it is not the current one (dont add refreshing)
    if len(client_history[client_data.client_id]) == 0 or \
        client_history[client_data.client_id][-1] != client_data.uri:
        client_history[client_data.client_id].append(client_data.uri)
    suggestions = predict_results(client_history[client_data.client_id])
    return Response(suggestions=suggestions)
