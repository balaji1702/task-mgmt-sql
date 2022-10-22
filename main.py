from http.client import HTTPException
from sqlalchemy.sql import text
import sqlalchemy as db
from database_config import engine
from enum import Enum
from typing import Optional
from fastapi import FastAPI, HTTPException,status
from pydantic import BaseModel
conn=engine.connect()
metadata = db.MetaData()
to_do_tb = db.Table("to_do", metadata, autoload=True, autoload_with=engine)
app = FastAPI()

class Priority(Enum):
    High="HIGH PRIORITY"
    Low="LOW PRIORITY"
class Status(Enum):
    pending="PENDING"
    completed="COMPLETED"
    
class Task(BaseModel):
    task_name: str
    description: str  
    priority :Priority
    status: Status

@app.post("/create-task")
def create_task(new_task:Task):
    task=new_task.dict()
    
    try:
        query=text("insert into to_do (taskname,descriptionS,priority,statuss) VALUES (:taskname,:desc,:pr,:sts)")
        conn.execute(query,taskname=task["task_name"],desc=task["description"],pr=task["priority"].value,sts=task["status"].value)
        return {"msg":"suceesfully added"}
    except Exception as error:
          print(type(error))
          
          raise HTTPException(status_code=status.HTTP_411_LENGTH_REQUIRED, detail= {"msg":"cannot perform the task debug it",
          "error":str(error)})


@app.get("/task")
def get_task():
    try:
        result=conn.execute("select * from to_do")
        return result.fetchall()
    except Exception as error:
          print(type(error))
          
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= {"msg":"cannot perform the task debug it",
          "error":str(error)})


@app.get("/filter-task-by-PRIORITY")
def filter_by_priority(q: Priority):
     try:
        query=text("select * from to_do where priority = :pr")
        result=conn.execute(query,pr=q.value)
        return  result.fetchall()
     except Exception as error:
          print(type(error))
          
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= {"msg":"cannot perform the task debug it",
          "error":str(error)})
     
     
     
            
        
    

@app.get("/filter-task-by-status")
def filter_by_status(q:Status):
    try:
        query=text("select * from to_do where statuss = :sts")
        result=conn.execute(query,sts=q.value)
        return  result.fetchall()
    except Exception as error:
          
          
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= {"msg":"cannot perform the task debug it",
          "error":str(error)})


@app.put("/task_update_status/{taskname}")
def update_status(taskname:str,q:Status):
    try:
        query=text("update to_do set statuss=:sts where taskname=:task_name")
        conn.execute(query,sts=q.value,task_name=taskname)
        return {"msg":"task updated sucessfully"}
    except Exception as error:
        
          
          raise HTTPException( status_code=status.HTTP_417_EXPECTATION_FAILED,detail= {"msg":"cannot perform the task debug it",
          "error":str(error)})

@app.put("/task_update_priority/{taskname}")
def update_priority(taskname:str,q:Priority):
    try:
        query=text("update to_do set priority=:pir where taskname=:task_name")
        conn.execute(query,pir=q.value,task_name=taskname)
        return {"msg":"task updated sucessfully"}
    except Exception as error:
        
          
          raise HTTPException( status_code=status.HTTP_417_EXPECTATION_FAILED,detail= {"msg":"cannot perform the task debug it",
          "error":str(error)})

@app.delete("/delete-task")
def delete_task(task_name:str):
    try:
        query=text("delete from to_do where taskname=:taskname")
        conn.execute(query,taskname= task_name)
        return  {"msg":"task deleted sucessfully"}
    except Exception as error:
          print(type(error))
          
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= {"msg":"cannot perform the task debug it",
          "error":str(error)})
@app.delete("/delet-all-task")
def delete_all():
    try:
        conn.execute("truncate to_do")
        return {"msg":"deleted all values in table"}
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= {"msg":"cannot perform the task debug it",
          "error":str(error)})

    








