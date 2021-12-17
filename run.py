from app import create_app
from os import getenv
from dotenv import load_dotenv


if __name__ == '__main__':
    load_dotenv()
    app = create_app(getenv('FLASK_CONFIG'))
    app.run()