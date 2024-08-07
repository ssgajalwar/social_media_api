from typing import Union
from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def read_root():
    return {'message':'Hello World !!'}

@app.get('/posts')
def get_post():
    return {'posts':'All posts'}


@app.get('/posts/id')
def get_specific_post():
    return {'posts':'post with id 1 returned'}

@app.post('/posts')
def add_post():
    return {'posts':'Added post'}