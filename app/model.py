from datetime import date
from typing import Optional

import sqlalchemy as sa
from pydantic import BaseModel


class TaskBase(BaseModel):
    project_id: int
    description: str
    due_to: Optional[date]


class TaskDB(TaskBase):
    id: int
    is_complete: bool


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    id: Optional[int]
    project_id: Optional[int]
    description: Optional[str]
    due_to: Optional[date]
    is_complete: Optional[bool]


class ProjectBase(BaseModel):
    project_name: str


class ProjectDB(ProjectBase):
    id: int


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    project_name: Optional[str]
    project_description: Optional[str]


metadata = sa.MetaData()

tasks = sa.Table(
    "tasks",
    metadata,
    sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
    sa.Column(
        "project_id",
        sa.ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
    ),
    sa.Column("is_complete", sa.Boolean(), nullable=False, server_default=sa.false()),
    sa.Column("due_to", sa.DateTime(), nullable=True),
    sa.Column("description", sa.Text(), nullable=False),
)

projects = sa.Table(
    "projects",
    metadata,
    sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
    sa.Column("project_name", sa.String(length=255), nullable=False),
    sa.Column("project_description", sa.Text()),
)
