import argparse
import datetime
import json
from pathlib import Path


def create_file_if_not_exist(path):
    filename = Path(path)

    if not filename.exists():
        filename.touch()

        with open(path, mode="w", encoding="utf-8") as fp:
            json.dump([], fp)


def add_task(
    task_id,
    description,
    status,
    created_at=datetime.datetime.now().strftime("%d/%m/%Y %I:%M %p %Z"),
    updated_at=datetime.datetime.now().strftime("%d/%m/%Y %I:%M %p %Z"),
):
    tasks = "tasks.json"
    task_list = []

    with open(tasks) as fp:
        task_list = json.load(fp)

    task_list.append(
        {
            "id": task_id,
            "description": description,
            "status": status,
            "created_at": created_at,
            "updated_at": updated_at,
        }
    )

    with open(tasks, "w") as json_file:
        json.dump(task_list, json_file, indent=4)

    print("Successfully appended to the JSON file.")


def update_task(
    id,
    description=None,
    status=None,
    updates_at=datetime.datetime.now().strftime("%d/%m/%Y %I:%M %p %Z"),
):
    pass


def delete_task(id):
    pass


def mark_task_as_by_status(id, status="todo"):
    # TODO: mark task as "todo"
    # TODO: mark task as "in-progress"
    # TODO: mark task as "done"
    pass


# TODO: List all tasks that are not done (not actively in progress??).
def list_tasks_by_status(status=None):
    # TODO: list all tasks
    if status is None:
        with open("tasks.json", mode="r", encoding="utf-8") as f:
            for line in f:
                print(line)

    # TODO: list tasks todo
    # TODO: list tasks that are in progress
    # TODO: list tasks that are done


parser = argparse.ArgumentParser(
    prog="tasl-cli",
    description="CLI Task Tracker",
    epilog="Thanks for using %(prog)s!",
    # argument_default=argparse.SUPPRESS,
)
subparsers = parser.add_subparsers(
    title="subcommands",
    dest="subcommand",
    help="task operations",
)

# Add task subcommand
add_parser = subparsers.add_parser("add", help="Add a new task")
add_parser.add_argument(
    "-d", "--description", help="a description of the task", required=True
)
add_parser.add_argument(
    "-s",
    "--status",
    type=str,
    help="the status of the task (todo, in-progress, done)",
    required=True,
)
add_parser.set_defaults(func=add_task)

# Update task command


# Delete task command


if __name__ == "__main__":
    create_file_if_not_exist("tasks.json")

    add_task(1, "a task", "todo")
    list_tasks_by_status()
