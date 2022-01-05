from app import create_app
from os import getenv
from dotenv import load_dotenv


load_dotenv()
app = create_app(getenv('FLASK_CONFIG'))


if __name__ == '__main__':
    app.run()    