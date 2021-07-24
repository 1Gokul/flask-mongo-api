# flask-mongo-api
Flask-MongoDB REST API

## [View API Documentation](https://documenter.getpostman.com/view/15393669/TzsZr8qn)

## Setup

- Clone the repo and navigate to the folder's root

- Open Terminal/CMD in the folder
- Run `pip install -r requirements.txt` to install all the packages

- [Get a MongoDB Atlas Connection String](https://docs.mongodb.com/guides/server/drivers/#obtain-your-mongodb-connection-string) and set it as the `MONGO_KEY` environment variable

```python
os.environ["MONGO_KEY"] = "<your_connection_string>"
```

- Create a JWT key and set it as the `JWT_SECRET` environment variable
```python
os.environ["JWT_SECRET"] = "<your_jwt_secret>"
```

- Run `python3 app.py` and you should be good to go! Check out the [Documentation](https://documenter.getpostman.com/view/15393669/TzsZr8qn) and send requests.
