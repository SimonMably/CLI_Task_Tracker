import argparse
import datetime
import json
from pathlib import Path


def create_json_file_if_not_exist(file):
    filename = Path(file)

    if not filename.exists():
        filename.touch()

        with open(file, mode="w", encoding="utf-8") as fp:
            json.dump([], fp)


def read_json(file):
    with open(file, "r", encoding="utf-8") as fp:
        return json.load(fp)


def add_task(args):
    # TODO: Find a way to increment id number

    tasks = "tasks.json"
    task_list = []

    with open(tasks, "r", encoding="utf-8") as fp:
        task_list = json.load(fp)
        last_id = task_list[-1]["id"]

    new_id = last_id + 1

    task_list.append(
        {
            "id": new_id,
            "description": args.description,
            "status": "todo",
            "created_at": datetime.datetime.now().strftime("%d/%m/%Y %I:%M %p %Z"),
            "updated_at": datetime.datetime.now().strftime("%d/%m/%Y %I:%M %p %Z"),
        }
    )

    with open(tasks, mode="w", encoding="utf-8") as json_file:
        json.dump(task_list, json_file, indent=4)

    print("Successfully appended to the JSON file.")


def update_task(
    id,
    description=None,
    status=None,
    updated_at=datetime.datetime.now().strftime("%d/%m/%Y %I:%M %p %Z"),
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
    elif status == "todo":
        with open("tasks.json", mode="r", encoding="utf-8") as f:
            for task in f:
                pass

    # TODO: list tasks that are in progress
    # TODO: list tasks that are done


def main():
    parser = argparse.ArgumentParser(
        prog="tasl-cli",
        description="CLI Task Tracker",
        epilog="Thanks for using %(prog)s!",
        # argument_default=argparse.SUPPRESS,
    )
    subparsers = parser.add_subparsers(
        title="commands",
        dest="command",
        required=True,
    )

    # Add task command
    add_subparser = subparsers.add_parser("add", help="add a new task.")
    add_subparser.add_argument("description", help="description of the task")
    add_subparser.set_defaults(func=add_task)

    # Update task command
    update_subparser = subparsers.add_parser("update", help="update an existing task.")
    update_subparser.set_defaults(func=update_task)

    # Delete task command
    delete_subparser = subparsers.add_parser(
        "delete", help="delete a task by specifying a task id."
    )
    delete_subparser.set_defaults(func=delete_task)

    # Mark task command (mark in-progress, mark done, mark todo (mark todo can be set as default when adding the task))
    mark_subparser = subparsers.add_parser(
        "mark",
        help="Mark a task as 'done' or 'in-progress'. All tasks are marked as 'todo' by default when created.",
    )
    mark_subparser.add_argument("--in-progress", help="Mark a task as 'in-progress'.")
    mark_subparser.add_argument("--done", help="Mark a task as 'done'.")
    mark_subparser.set_defaults(func=mark_task_as_by_status)

    # List task command (List: list all tasks, List done, List todo, List in-progress)
    list_subparser = subparsers.add_parser(
        "list",
        help="list: list all tasks. Or use optional args; --done: list all tasks marked as done, --in-progress: list all tasks marked as in-progress, --todo: list all taskes marked as todo.",
    )
    list_subparser.add_argument("--done", help="List all tasks marked as 'done'.")
    list_subparser.add_argument("--todo", help="List all tasks marked as 'todo'.")
    list_subparser.add_argument(
        "--in-progress", help="List all tasks marked as 'in-progress'."
    )
    list_subparser.set_defaults(func=list_tasks_by_status)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    create_json_file_if_not_exist("tasks.json")
    main()
