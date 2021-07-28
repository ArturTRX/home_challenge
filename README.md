# home_challenge

I have analyzed project requirements and decided to choose the next technology stack to solve the problem:

FastAPI - modern high-performance web-framework with big community to write intuitive code that easy to debug and maintain. It gives an opportunity to write asynchronous code easier and use less server resources for more concurrent connections. 

Redis - inmemory NoSQL key-value storage. Oriented for the best performance with atomic operations that are used in current project.

### Endpoints

`GET /api/ad/ {'SDK Version': <version>, 'User name': <username>}`

`POST /api/impression/ {'SDK Version': <version>, 'User name': <username>}`

`GET /api/stats/ {'FilterType': <filter_type>}`

### Start project
`docker-compose build`

`docker-compose up`

### Tests

`pytest`
