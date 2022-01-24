from typing import List

from databases import Database
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from fastapi.routing import APIRouter

from .db import get_database
from .model import ProjectCreate, ProjectDB, ProjectUpdate, TaskCreate, TaskDB, TaskUpdate, projects, tasks

router = APIRouter()


async def get_task_or_404(task_id: int, database: Database = Depends(get_database)) -> TaskDB:
    query = tasks.select().filter(tasks.c.id == task_id)
    task = await database.fetch_one(query)
    if task is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Task with id {task_id} does not exist.")

    return TaskDB(**task)


async def get_project_or_404(project_id: int, database: Database = Depends(get_database)) -> ProjectDB:
    query = projects.select().filter(projects.c.id == project_id)
    project = await database.fetch_one(query)
    if project is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Project with id {project_id} does not exist.")

    return ProjectDB(**project)


@router.get("/tasks")
async def list_tasks(database: Database = Depends(get_database)) -> List[TaskDB]:
    select_query = tasks.select()
    rows = await database.fetch_all(select_query)

    _tasks = [TaskDB(**row) for row in rows]
    return _tasks


@router.post("/tasks", status_code=status.HTTP_201_CREATED, response_model=TaskDB)
async def create_task(task_create: TaskCreate, database: Database = Depends(get_database)):
    query = tasks.insert().values(task_create.dict())
    task_id = await database.execute(query)
    created_task = await get_task_or_404(task_id, database)

    return created_task


@router.get("/tasks/{task_id}")
async def get_task(task: TaskDB = Depends(get_task_or_404)) -> TaskDB:
    return task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task: TaskDB = Depends(get_task_or_404), database: Database = Depends(get_database)) -> None:
    query = tasks.delete().where(tasks.c.id == task.id)
    await database.execute(query)


@router.patch("/tasks/{task_id}")
async def update_task(
    task_update: TaskUpdate, task: TaskDB = Depends(get_task_or_404), database: Database = Depends(get_database)
) -> TaskDB:
    query = tasks.update().where(tasks.c.id == task.id).values(task_update.dict(exclude_unset=True))
    task_id = await database.execute(query)

    updated_task = await get_task_or_404(task_id, database)

    return updated_task


@router.get("/projects")
async def list_projects(database: Database = Depends(get_database)) -> List[ProjectDB]:
    rows = await database.fetch_all(projects.select())
    _projects = [ProjectDB(**row) for row in rows]

    return _projects


@router.get("/projects/{project_id}")
async def get_project(project: ProjectDB = Depends(get_project_or_404)) -> ProjectDB:
    return project


@router.delete("/projects/{project_id}")
async def delete_project(project: ProjectDB = Depends(get_project_or_404), database: Database = Depends(get_database)):
    query = projects.delete().where(projects.c.id == project.id)
    await database.execute(query)


@router.post("/projects", status_code=status.HTTP_201_CREATED)
async def create_project(project_to_create: ProjectCreate, database: Database = Depends(get_database)) -> ProjectDB:
    query = projects.insert().values(project_to_create.dict())
    project_id = await database.execute(query)

    project = await get_project_or_404(project_id, database)

    return project


@router.patch("/projects/{project_id}")
async def update_project(
    project_update: ProjectUpdate,
    project: ProjectDB = Depends(get_project_or_404),
    database: Database = Depends(get_database),
) -> ProjectDB:
    query = projects.update().where(projects.c.id == project.id).values(project_update.dict(exclude_unset=True))
    project_id = await database.execute(query)

    _project = await get_project_or_404(project_id, database)

    return _project
