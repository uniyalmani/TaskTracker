# TaskTracker
Task Tracker is a personal project designed to help individuals efficiently manage and track their tasks and activities

---
# API

---

## ***Create a new Task***
```
POST /v1/tasks
```
***Input for creating single task***
```
{title: "Test Task 2"}

```
***output***
```
{title: "Test Task 2"}
```
---
## ***Create multiple Task***
```
POST /v1/tasks
```
***Input for creating Bulk task***
```
{
   tasks: [
      {title: "Test Task 1", is_completed: true},
      {title: "Test Task 2", is_completed: false},
      {title: "Test Task 3", is_completed: true}
   ]
}

```
***output***
```
(return a 201 code)
{
   tasks: [
      {id: 1},
      {id: 2},
      {id: 3}
   ]
}
```
---

## ***Bulk add tasks***
```
GET /v1/tasks
```
***Input***
```
None
```
***Output***
```
(return a 200 code)
{
   tasks: [
     {id: 1, title: "Test Task 1", is_completed: true},
     {id: 2, title: "Test Task 2", is_completed: false}
   ]
}
```
---

## ***Get a specific task***
```
GET /v1/tasks/{id}
```
***input**
```
id (passed through the URL)
```
***Output***
```
(return a 200 code)
{id: 3, title: "Test Task 2", is_completed: false}
```
***Note***
```
This endpoint returns a specific task or returns a 404 not found response

```
---

## ***Delete a specific task***
```
DELETE /v1/tasks/{id}
```
***Input***
```
id (passed through the URL)
```
***Output***
```
None (return a 204 code)
```
***Note***
```
This endpoint deletes a specific task. If the task doesn’t exist still send the same response
```
---

## ***Bulk delete tasks***
```
DELETE /v1/tasks
```
***Input***
```
{
   tasks: [
     {id: 1},
     {id: 2},
     {id: 3}
  ]
}
```
***Output***
```
None (return a 204 code)
```
***Note***
```
This endpoint bulk deletes more than one task.
```

---

## ***Edit the title or completion of a specific task***

```
PUT /v1/tasks/{id}
```
***Input***
```
{title: "Test Task 2", is_completed: false}
```
***Output***
```
None (return a 204 code)
```
***Note***
```
This endpoint deletes a specific task or returns a 404 not found response
```



