from fastapi import FastAPI, HTTPException

app = FastAPI()

tasks = []
counter = 1


@app.get("/tasks")
def get_tasks(priority: int = None):
    if priority is None:
        return tasks
    if priority > 3 or priority < 1:
        raise HTTPException(status_code=400, detail="Invalid priority filter")

    filtered_tasks = []
    for task in tasks:
        if task.get("priority") == priority:
            filtered_tasks.append(task)

    return filtered_tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@app.post("/tasks")
def add_task(task: dict):
    global counter
    priority = task.get("priority", 2)

    if type(priority) is not int or priority < 1 or priority > 3:
        raise HTTPException(
            status_code=400,
            detail="Priority must be an integer between 1 (high) and 3 (low)"
        )

    new_task = {
        "id": counter,
        "title": task.get("title"),
        "owner": task.get("owner"),
        "priority": priority
    }
    tasks.append(new_task)
    counter += 1
    return new_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return {"message": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")