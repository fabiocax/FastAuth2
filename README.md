# FastAPI Users

<p align="center">
  <img src="https://raw.githubusercontent.com/fabiocax/FastAuth2/master/imgs/logo.png?sanitize=true" alt="FastAPI Users">
</p>




**Documentation**: <a href="https://fastauth2.herokuapp.com/redoc" target="_blank"https://fastauth2.herokuapp.com/redoc</a>
<!-- ---
**Source Code**: <a href="https://github.com/fastapi-users/fastapi-users" target="_blank">https://github.com/fastapi-users/fastapi-users</a>

--- -->

Add quickly a registration and authentication system to your project. **FastAuth2** is designed to be as customizable and adaptable as possible.

## Features

* [X] Extensible base user model
* [X] Ready-to-use register, login, reset password and verify e-mail routes
* [X] Ready-to-use social OAuth2 login flow
* [X] Dependency callables to inject current user in route
* [X] Pluggable password validation
* [X] Customizable database backend
    * [X] [SQLAlchemy ORM async](https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html) included
    * [X] [MongoDB with Beanie ODM](https://github.com/roman-right/beanie/) included
* [X] Multiple customizable authentication backends
    * [X] Transports: Authorization header, Cookie
    * [X] Strategies: JWT, Database, Redis
* [X] Full OpenAPI schema support, even with several authentication backends


## Development

### Setup environment

You should create a virtual environment and activate it:

```bash
python -m venv venv/
```

```bash
source venv/bin/activate

```


Clone project:

```bash
https://github.com/fabiocax/FastAuth2.git

```

Install dependencies:

```bash
pip install -r requirements.txt

```

Configure variables:


```bash
SECRET_KEY="{openssl rand -hex 32}"
API_DATABASE_URL="database url"

```
## Docker Pull
```bash
docker pull shotofw/fastauth2

```
Create superuser

```bash
 docker run -p 5000:5000 -v /home/path/:/app/db -it shotofw/fastauth2  python cli.py createsuperuser admin senha

```
## Api Docs

http://127.0.0.1:5000/docs#/

## License

This project is licensed under the terms of the MIT license.
