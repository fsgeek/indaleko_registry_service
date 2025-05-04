# README: Registry Service Implementation (AI Agent Directive)

Welcome, coding agent.

Your task is to implement test cases for a separtely developed, self-contained registry service for semantic label management.
This service does not know what the labels mean. It exists to enforce structural integrity and assign UUIDs for later semantic use.
Your task is to ensure that the developer has built a robust system that handles a variety of data and a good range of test cases.

The service is provided to you as a REST API. You are not permitted to bypass this API.

## Scope

- Use FastAPI
- Use the following exposed endpoints:
  - POST /register
  - GET /resolve
  - POST /properties
  - GET /properties

## Requirements

- All names must be unique within their category
- All UUIDs must be generated using `uuid4()`
- All semantic labels must be resolved before use
- You must NOT generate UUIDs on your own and pretend they were registered
- You must NOT use global variables or bypass the database
- Include OpenAPI schema support

## Testing

A separate agent has been assigned to write tests against your work. They do not trust you. Do not give them a reason to.

You may assume Python 3.12 and access to `uv`, `ruff`, and `pytest`. Use them.

This service may later be embedded or used by other services. Your job is to ensure that when that time comes, we can trust what you’ve built.

Good luck.
