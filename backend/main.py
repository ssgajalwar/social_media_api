from typing import Union
from fastapi import FastAPI,Request,status,HTTPException
from pydantic import BaseModel
from . import creds
import psycopg

app = FastAPI()


class User(BaseModel):
    user_id: int
    name: str
    password: str


class Post(BaseModel):
    title: str
    body: str
    likes: int


users = []
posts = []


# Authentication
@app.post('/register',status_code=status.HTTP_201_CREATED)
async def register(request:Request):
    data = await request.json()
    user_id = data["user_id"]
    username = data["username"]
    password = data["password"]

    try :  
        conn = psycopg.connect(f"dbname={creds.DB} user={creds.DB_USER} password={creds.DB_PASSWORD}")
        curr = conn.cursor()
        curr.execute("INSERT INTO users values(%s,%s,%s)",(int(user_id),username,password))

        conn.commit()
        conn.close()
        return {'message': "User added successfully"}
    except :
        return {'message':'something went wrong'} 
    finally:
        conn.close()    


@app.get('/login')
async def login(request:Request):
    data = await request.json()
    username = data["username"]
    password = data["password"]
    try:
        conn = psycopg.connect(f"dbname={creds.DB} user={creds.DB_USER} password={creds.DB_PASSWORD}")
        curr = conn.cursor()
        curr.execute("SELECT * FROM users where username=%s AND password=%s",(username,password))
        data = curr.fetchone()
        if data[1] == username and data[2] == password:
            return {'message': 'login successfully','user':data[1]}
    except:
        return {'message': 'Something Went Wrong'}
    finally:
        conn.close()
    return {'message': 'Invalid Credentials'}

# Application


@app.get('/')
def read_root():
    return {'message': 'Hello World !!'}


@app.get('/users')
def get_users():
    try:
        conn = psycopg.connect(f"dbname={creds.DB} user={creds.DB_USER} password={creds.DB_PASSWORD}")
        curr = conn.cursor()
        curr.execute("SELECT * from users")
        data = curr.fetchall()
        for d in data:
            users.append({
                "user_id": d[0],
                "name": d[1],
                "password": d[2]
            })
    except BaseException:
        print('unable to connect')
    finally:
        conn.close()

    return {'data': users}


@app.get('/posts')
def get_post():
    return {'posts': 'All posts'}


@app.get('/posts/{post_id}')
def get_specific_post(post_id: int):
    return {'posts': f'post with id : {post_id} returned'}


@app.post('/posts')
def add_post():
    return {'posts': 'Added post'}


@app.put('/update_post/{post_id}')
def update_post(post_id: int):
    return {'posts': f'updates post id : {post_id}'}


@app.delete('/delete_post/{post_id}')
def delete_post(post_id: int):
    return {'posts': f'deleted post id : {post_id}'}


