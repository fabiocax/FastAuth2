# FastAPI Users

<p align="center">
  <img src="https://raw.githubusercontent.com/fabiocax/FastAuth2/master/imgs/logo.png?sanitize=true" alt="FastAPI Users">
</p>


---

**Documentation**: <a href="https://fastapi-users.github.io/fastapi-users/" target="_blank">https://fastapi-users.github.io/fastapi-users/</a>

**Source Code**: <a href="https://github.com/fastapi-users/fastapi-users" target="_blank">https://github.com/fastapi-users/fastapi-users</a>

---

Add quickly a registration and authentication system to your [FastAPI](https://fastapi.tiangolo.com/) project. **FastAPI Users** is designed to be as customizable and adaptable as possible.

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

## In a hurry? Discover Fief, the open-source authentication platform

<p align="center">
  <img src="https://raw.githubusercontent.com/fief-dev/.github/main/logos/logo-full-red.svg?sanitize=true" alt="Fief" width="256" style="width: 256px">
</p>

<img src="https://www.fief.dev/illustrations/guard-right.svg" alt="Fief" height="300" align="right" style="height: 300px">

**Implementing registration, login, social auth is hard and painful. We know it. With our highly secure and open-source users management platform, you can focus on your app while staying in control of your users data.**

* Based on **FastAPI Users**!
* **Open-source**: self-host it for free or use our hosted version
* **Bring your own database**: host your database anywhere, we'll take care of the rest
* **Pre-built login and registration pages**: clean and fast authentication so you don't have to do it yourself
* **Official Python client** with built-in **FastAPI integration**



## Development

### Setup environment

You should create a virtual environment and activate it:

```bash
python -m venv venv/
```

```bash
source venv/bin/activate
```

And then install the development dependencies:

```bash
make install
```

### Run unit tests

You can run all the tests with:

```bash
make test
```

Alternatively, you can run `pytest` yourself.

```bash
pytest
```

There are quite a few unit tests, so you might run into ulimit issues where there are too many open file descriptors. You may be able to set a new, higher limit temporarily with:

```bash
ulimit -n 2048
```

### Format the code

Execute the following command to apply `isort` and `black` formatting:

```bash
make format
```

## License

This project is licensed under the terms of the MIT license.
