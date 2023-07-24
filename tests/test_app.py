import requests

def test_create_task():
    # Store the current number of tasks in the database
    initial_tasks_count = len(requests.get('http://localhost:8000/v1/tasks').json()["tasks"])

    # Create a new task
    r = requests.post('http://localhost:8000/v1/tasks', json={"title": "My First Task"})
    assert r.status_code == 201
    assert isinstance(r.json()["id"], int)

    # Verify that the number of tasks in the database has increased by 1
    updated_tasks_count = len(requests.get('http://localhost:8000/v1/tasks').json()["tasks"])
    assert updated_tasks_count == initial_tasks_count + 1


def test_get_task():
    # Create a new task to ensure there is a task in the database
    create_response = requests.post('http://localhost:8000/v1/tasks', json={"title": "Test Task"})
    task_id = create_response.json()["id"]

    # Get the created task by ID
    r = requests.get(f'http://localhost:8000/v1/tasks/{task_id}')
    assert r.status_code == 200

    # Verify that the retrieved task matches the created task
    assert r.json()["id"] == task_id
    assert r.json()["title"] == "Test Task"
    assert r.json()["is_completed"] is False

def test_update_task():
    # Create a new task to ensure there is a task in the database
    create_response = requests.post('http://localhost:8000/v1/tasks', json={"title": "Test Task"})
    task_id = create_response.json()["id"]

    # Update the task
    update_response = requests.put(f'http://localhost:8000/v1/tasks/{task_id}', json={"title": "Updated Task", "is_completed": True})
    assert update_response.status_code == 204

    # Verify that the task was updated in the database
    get_response = requests.get(f'http://localhost:8000/v1/tasks/{task_id}')
    assert get_response.status_code == 200

    # Verify that the task's title and is_completed attributes have been updated
    assert get_response.json()["id"] == task_id
    assert get_response.json()["title"] == "Updated Task"
    assert get_response.json()["is_completed"] is True

import requests

def test_delete_task():
    # Create a new task to ensure there is a task in the database
    create_response = requests.post('http://localhost:8000/v1/tasks', json={"title": "Test Task"})
    task_id = create_response.json()["id"]

    # Delete the task
    delete_response = requests.delete(f'http://localhost:8000/v1/tasks/{task_id}')
    assert delete_response.status_code == 204

    # Verify that the task has been deleted from the database
    get_response = requests.get(f'http://localhost:8000/v1/tasks/{task_id}')
    assert get_response.status_code == 404
    assert get_response.json()["detail"]["error"] == "There is no task at that id"


def test_create_bulk_task():
    # Bulk create tasks
    tasks = [
        {"title": "Task 1", "is_completed": False},
        {"title": "Task 2", "is_completed": True},
        {"title": "Task 3", "is_completed": False}
    ]
    create_response = requests.post('http://localhost:8000/v1/tasks', json={"tasks": tasks})
    assert create_response.status_code == 201

    # Verify that the tasks have been assigned unique IDs
    task_ids = create_response.json()["tasks"]

    # Verify that the tasks exist in the database and have the correct title and is_completed values
    for task_id in task_ids:
        get_response = requests.get(f'http://localhost:8000/v1/tasks/{task_id["id"]}')
        assert get_response.status_code == 200
        task = get_response.json()
        matching_task_data = next((task_data for task_data in tasks if task_data["title"] == task["title"] and task_data["is_completed"] == task["is_completed"]), None)
        assert matching_task_data is not None

    # Clean up by deleting the created tasks
    for task_id in task_ids:
        delete_response = requests.delete(f'http://localhost:8000/v1/tasks/{task_id["id"]}')
        assert delete_response.status_code == 204



def test_delete_bulk_tasks():
    # Bulk create tasks
    tasks = [
        {"title": "Task 1", "is_completed": False},
        {"title": "Task 2", "is_completed": True},
        {"title": "Task 3", "is_completed": False}
    ]
    create_response = requests.post('http://localhost:8000/v1/tasks', json={"tasks": tasks})
    assert create_response.status_code == 201

    # Get the IDs of the created tasks
    created_tasks = create_response.json()["tasks"]
    task_ids = [{"id": task["id"]} for task in created_tasks]

    # Bulk delete tasks
    delete_response = requests.delete('http://localhost:8000/v1/tasks', json={"tasks": task_ids})
    assert delete_response.status_code == 204

    # Verify that the tasks have been deleted from the database
    for task_id in task_ids:
        get_response = requests.get(f'http://localhost:8000/v1/tasks/{task_id["id"]}')
        assert get_response.status_code == 404
        assert get_response.json()["detail"]["error"] == "There is no task at that id"
