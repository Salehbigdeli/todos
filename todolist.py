
from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel


class Task(BaseModel):
    title: str
    done: bool


app = FastAPI()
tasks: list[Task] = []


@app.get('/api/v1/todos')
async def tasks_list() -> list[Task]:
    return tasks


@app.post("/api/v1/todos")
async def add_task(task: Task) -> Task:
    tasks.append(task)
    return task


@app.put("/api/v1/todos")
async def edit_task(task: Task) -> Task:
    found = False
    for t in tasks:
        if t.title == task.title:
            t.title = task.title
            t.done = task.done
            found = True
    if not found:
        raise HTTPException(404, detail='task not found')
    return t


@app.delete("/api/v1/todos")
async def delete_task(task: Task) -> Task:
    try:
        tasks.remove(task)
    except ValueError:
        raise HTTPException(404, detail='task not found')
    return task


if	__name__	== '__main__':
    uvicorn.run('todolist:app',host='127.0.0.1',port=8000,reload = True)