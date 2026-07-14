# Task API

A simple in-memory CRUD API for managing a to-do list, built with FastAPI and Python.

## How to run
Make sure you have FastAPI and Uvicorn installed. Start the server locally using:
`uvicorn main:app --reload`

## Endpoints
| CRUD operation | HTTP method | Example endpoint | Meaning |
|---|---|---|---|
| Create | POST | `POST /tasks` | Add a new task |
| Read | GET | `GET /tasks` <br> `GET /tasks/3` | List all tasks / get task 3 |
| Update | PUT | `PUT /tasks/3` | Change task 3 |
| Delete | DELETE | `DELETE /tasks/3` | Remove task 3 |

## Example Request
```bash
curl -i http://localhost:8000/tasks/1

HTTP/1.1 200 OK
date: Tue, 14 Jul 2026 14:00:00 GMT
server: uvicorn
content-length: 44
content-type: application/json

![Swagger UI Screenshot](Swagger%20Screenshots/6.png)