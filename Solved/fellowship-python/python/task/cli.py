"""This module provides the task CLI."""
# task/cli.py
from pathlib import Path
from typing import List, Optional
import typer
from task import (    ERRORS, __app_name__, __version__,  config,   database,   task )
import os

app = typer.Typer(help=" Once run .task init command first to initialise database")

def get_todoer() -> task.Todoer:
    if config.CONFIG_FILE_PATH.exists():
        db_path = database.get_database_path(config.CONFIG_FILE_PATH)
    else:
        typer.secho(
            'Config file not found. Please run .\task init or run the task.bat file again',
        )
        raise typer.Exit(1)
    if db_path.exists():
        return task.Todoer(db_path)
    else:
        typer.secho(
            'Database not found. Please run .\task init or run the task.bat file again',
        )

        return task.Todoer(db_path)

@app.command(name="init")
def init(db_path: str = str(database.DEFAULT_DB_FILE_PATH)) -> None:
    """Initialize the task database."""
    app_init_error = config.init_app(db_path)
    if app_init_error:
        typer.secho(
            f'Creating config file failed with "{ERRORS[app_init_error]}"',
        )
        raise typer.Exit(1)
    db_init_error = database.init_database(Path(db_path))
    if db_init_error:
        typer.secho(
            f'Creating database failed with "{ERRORS[db_init_error]}"',
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"The task database is {db_path}")

@app.command(name="report")
def report() -> None:
    """Remove a task using its TODO_ID."""
    todoer = get_todoer()
    todo_list = todoer.get_todo_list()
    lis=[]
    ulis=[]
    for i in todo_list:
        desc, priority, don=i.values()
        if(don==False):
            lis.append(i)
        else:
            ulis.append(i)

    typer.secho(
                f'Pending : {len(lis)}',
                fg=typer.colors.RED,
            )
    os.system(" python -m task ls")
    typer.secho()
    typer.secho(
                f'Completed : {len(ulis)}',
                
            )
    if len(ulis) == 0:
        typer.secho(
            "There are no tasks in the task list yet", fg=typer.colors.RED
        )
        raise typer.Exit()

    for id, todo in enumerate(ulis, 1):
        desc, priority, done = todo.values()
        typer.secho(            f"{id}. {desc}",fg=typer.colors.BLUE,        )

@app.command(name="add")
def add(
    priority: int = typer.Argument(...),
    description: List[str] = typer.Argument(...),
    ) -> None:
    """Add a new task with a DESCRIPTION."""
    todoer = get_todoer()
    todo, error = todoer.add(description, priority)
    if error:
        typer.secho(
            f'Adding task failed with "{ERRORS[error]}"', 
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"""Added task: "{todo['Description']}" """
            f"""with priority {priority}""",
            
        )
    
def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
    ) -> None:
    return

@app.command(name="help")
def help() -> None:
    """Shows the help text"""
    os.system(" python -m task --help")

@app.command(name="ls")
def ls(done: bool =False) -> None:
    """List all tasks."""
    todoer = get_todoer()
    
    todo_list = todoer.get_todo_list()
    lis=[]
    for i in todo_list:
        desc, priority, don=i.values()
        if(don==done):
            lis.append(i)

    if len(lis) == 0:
        typer.secho(
            "There are no tasks in the task list yet", fg=typer.colors.RED
        )
        raise typer.Exit()

    for id, todo in enumerate(lis, 1):
        desc, priority, done = todo.values()
        typer.secho(            f"{id}. {desc} [{priority}]",fg=typer.colors.BLUE,        )

@app.command(name="del")
def remove(
    todo_id: int = typer.Argument(...),
    ) -> None:
    """Remove a task using its TASK_ID."""
    todoer = get_todoer()

    def _remove():
        todo, error = todoer.remove(todo_id)
        if error:
            typer.secho(
                f'Removing task # {todo_id} failed with "{ERRORS[error]}"',
                fg=typer.colors.RED,
            )
            raise typer.Exit(1)
        else:
            typer.secho(
                f"""Deleted task #{todo_id}""",
                fg=typer.colors.GREEN,
            )
    _remove()
 
@app.command(name="done")
def set_done(todo_id: int = typer.Argument(...)) -> None:
    """Complete a task by setting it as done using its TODO_ID."""
    todoer = get_todoer()
    todo, error = todoer.set_done(todo_id)
    if error:
        typer.secho(
            f'Completing task # "{todo_id}" failed with "{ERRORS[error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"""Marked item as done.""",
            fg=typer.colors.GREEN,
        )
