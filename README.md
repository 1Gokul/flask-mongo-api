# flask-mongo-api
Flask-MongoDB REST API

## [View API Documentation](https://documenter.getpostman.com/view/15393669/TzsZr8qn)

## Setup

- Clone the repo and navigate to the folder's root

- Open Terminal/CMD in the folder
- Run `pip install -r requirements.txt` to install all the packages

- [Get a MongoDB Atlas Connection String](https://docs.mongodb.com/guides/server/drivers/#obtain-your-mongodb-connection-string) and set it as the `MONGO_KEY` environment variable in [app.py](https://github.com/1Gokul/flask-mongo-api/blob/main/app.py#L14)

```python
os.environ["MONGO_KEY"] = "<paste_your_connection_string_here>""
```

- Create a JWT key and set it as the `JWT_SECRET` environment variable in [app.py](https://github.com/1Gokul/flask-mongo-api/blob/main/app.py#L16)
```python
os.environ["JWT_SECRET"] = "<paste_your_jwt_secret_here>""
```

- Run `python3 app.py` and you should be good to go! Check out the [Documentation](https://documenter.getpostman.com/view/15393669/TzsZr8qn) and send requests.
