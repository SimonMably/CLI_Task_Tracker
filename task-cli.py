import argparse
import datetime
import json
from pathlib import Path

TASK_FILE = "tasks.json"


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
    task_list = []

    with open(TASK_FILE, "r", encoding="utf-8") as fp:
        task_list = json.load(fp)
        if not len(task_list) == 0:
            last_id = task_list[-1]["id"]
        else:
            last_id = 0

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

    with open(TASK_FILE, mode="w", encoding="utf-8") as fp:
        json.dump(task_list, fp, indent=4)

    print("Successfully appended to the JSON file.")


def update_task(args):
    tasks_file = "tasks.json"

    with open(tasks_file, "r", encoding="utf-8") as fp:
        task_list = json.load(fp)

    for task in task_list:
        if str(task["id"]) == args.id:
            task["description"] = args.new_description
            task["updated_at"] = datetime.datetime.now().strftime(
                "%d/%m/%Y %I:%M %p %Z"
            )
            break
    else:
        print(f"Task with id {args.id} not found")

    with open(tasks_file, "w", encoding="utf-8") as fp:
        json.dump(task_list, fp, indent=4)

    print(f"Successfully updated task {args.id}")


def delete_task(args):

    with open(TASK_FILE, "r", encoding="utf-8") as fp:
        task_list = json.load(fp)

    for task in task_list:
        if task["id"] == args.id:
            task_list.remove(task)
            break
    else:
        print(f"Task with id {args.id} not found")
        return

    with open(TASK_FILE, "w", encoding="utf-8") as fp:
        json.dump(task_list, fp, indent=4)
        print(f"Successfully deleted task {args.id}.")


def mark_task_by_status(args):  # id, status="todo"):

    with open(TASK_FILE, "r", encoding="utf-8") as fp:
        task_list = json.load(fp)

    for task in task_list:
        if task["id"] == args.id:
            if task["status"] == args.status:
                print(f"This task has already been marked as {args.status}")
                return

            if args.status == "todo":
                task["status"] = "todo"
            elif args.status == "in-progress":
                task["status"] = "in-progress"
            elif args.status == "done":
                task["status"] = "done"
        else:
            print(f"Task with id {args.id} not found.")
            return

    with open(TASK_FILE, "w", encoding="utf-8") as fp:
        json.dump(task_list, fp, indent=4)

    print(f"Successfully status of task {args.id} to {args.status}")


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
    update_subparser.add_argument("id", help="The id of the task to update.")
    update_subparser.add_argument("new_description")
    # update_subparser.add_argument(
    #     "new description", help="The new description of the task"
    # )
    update_subparser.set_defaults(func=update_task)

    # Delete task command
    delete_subparser = subparsers.add_parser(
        "delete", help="delete a task by specifying a task id."
    )
    delete_subparser.add_argument("id", help="the id of the task to delete", type=int)
    delete_subparser.set_defaults(func=delete_task)

    # Mark task command (mark in-progress, mark done, mark todo (mark todo can be set as default when adding the task))
    mark_subparser = subparsers.add_parser(
        "mark",
        help="Mark a task as 'done' or 'in-progress'. All tasks are marked as 'todo' by default when created.",
    )
    mark_subparser.add_argument(
        "status",
        help="Mark a task as 'in-progress' or 'done'.",
        type=str,
        choices=["todo", "in-progress", "done"],
    )
    mark_subparser.add_argument("id", help="The id of the task", type=int)
    mark_subparser.set_defaults(func=mark_task_by_status)

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
