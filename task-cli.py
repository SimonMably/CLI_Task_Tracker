import argparse
import datetime
import json
from pathlib import Path

TASK_FILE = "tasks.json"


def create_json_file(file):
    """Creates file, if it doen't exsist. Uses json.dump() to enter an empty list in file.

    Arguments:
        file -- Takes file path/filename as a string.
    """
    filename = Path(file)

    if not filename.exists():
        filename.touch()

        with open(file, mode="w", encoding="utf-8") as fp:
            json.dump([], fp)


def read_json(file):
    """Opens and reads a json file.

    Arguments:
        file -- file path / name as a string. Intended file is a json file.

    Returns:
        json list, either empty or contains json objects.
    """
    with open(file, "r", encoding="utf-8") as fp:
        return json.load(fp)


def add_task(args):
    """Adds a new task to a json file.

    Example:
        task-cli.py add "Finish task by today."

    Arguments:
        args -- arguments taken at the command line.
    """
    task_list = read_json(TASK_FILE)

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
    """Updates a tasks description and updated_at keys. Task is specified via tasks id.

    Examply:
        task-cli.py update "Finish task by Thursday" 1

    Arguments:
        args -- arguments taken at the command line.
    """
    task_list = read_json(TASK_FILE)

    for task in task_list:
        if str(task["id"]) == args.id:
            task["description"] = args.new_description
            task["updated_at"] = datetime.datetime.now().strftime(
                "%d/%m/%Y %I:%M %p %Z"
            )
            break
    else:
        print(f"Task with id {args.id} not found")

    with open(TASK_FILE, "w", encoding="utf-8") as fp:
        json.dump(task_list, fp, indent=4)

    print(f"Successfully updated task {args.id}")


def delete_task(args):
    """Delete a task, specified by the tasks id.

    Example:
        task-cli.py delete 1

    Arguments:
        args -- arguments taken at the command line.
    """

    task_list = read_json(TASK_FILE)

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


def mark_task_by_status(args):
    """Update the status of an existing task. Available options:
        - todo
        - in-progress
        - done

    Example:
        task-cli.py mark in-progress 1

    Arguments:
        args -- arguments taken at the command line.
    """
    task_list = read_json(TASK_FILE)

    for task in task_list:
        if task["id"] == args.id:
            if task["status"] == args.mark_status:
                print(f"This task has already been marked as {args.mark_status}")
                return

            if args.mark_status == "todo":
                task["status"] = "todo"
            elif args.mark_status == "in-progress":
                task["status"] = "in-progress"
            elif args.mark_status == "done":
                task["status"] = "done"
            break
    else:
        print(f"Task with id {args.id} not found.")
        return

    with open(TASK_FILE, "w", encoding="utf-8") as fp:
        json.dump(task_list, fp, indent=4)

    print(f"Successfully status of task {args.id} to {args.mark_status}")


def list_tasks_by_status(args):
    """Lists all tasks or lists tasks by specific status. Available status': todo, in-progress, done.

    Examples:
        List all tasks: task-cli.py list
        List tasks by status: task-cli.py list in-progress

    Arguments:
        args -- arguments to pass in on command line.
    """
    task_list = read_json(TASK_FILE)

    if not task_list:
        print("There are no tasks to list.")
        return

    if len([task for task in task_list if task["status"] == args.list_status]) == 0:
        if args.list_status == "all":
            pass
        else:
            print(f"There are no tasks with the status of {args.list_status}")
            return

    for task in task_list:
        if args.list_status == "all":
            print(f"Task ID {task['id']}: {task['description']} - {task['status']}")
        elif args.list_status == task["status"]:
            print(f"Task ID {task['id']}: {task['description']} - {task['status']}")


def main():
    parser = argparse.ArgumentParser(
        prog="tasl-cli",
        description="CLI Task Tracker",
        epilog="Thanks for using %(prog)s!",
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
    update_subparser.set_defaults(func=update_task)

    # Delete task command
    delete_subparser = subparsers.add_parser(
        "delete", help="delete a task by specifying a task id."
    )
    delete_subparser.add_argument("id", help="the id of the task to delete", type=int)
    delete_subparser.set_defaults(func=delete_task)

    mark_subparser = subparsers.add_parser(
        "mark",
        help="Mark a task as 'todo', 'done' or 'in-progress'. All tasks are marked as 'todo' by default when created.",
    )
    mark_subparser.add_argument(
        "mark_status",
        help="Mark a task as 'todo' or 'in-progress' or 'done'.",
        type=str,
        choices=["todo", "in-progress", "done"],
    )
    mark_subparser.add_argument("id", help="The id of the task", type=int)
    mark_subparser.set_defaults(func=mark_task_by_status)

    # List task command
    list_subparser = subparsers.add_parser(
        "list",
        help="list: list all tasks. Or use optional args; done: list all tasks marked as done, in-progress: list all tasks marked as in-progress, todo: list all taskes marked as todo.",
    )
    list_subparser.add_argument(
        "list_status",
        help="The status by which to list tasks. Options include all, todo, in-progress, and done. If you want to list all tasks, you have the option to use the all argument or leave blank as the all argument is set as the default.",
        nargs="?",
        choices=["all", "todo", "in-progress", "done"],
        default="all",
    )
    list_subparser.set_defaults(func=list_tasks_by_status)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    create_json_file("tasks.json")
    main()
