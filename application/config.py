import os
import sys


basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

WIN = sys.platform.startswith("win")
if WIN:
    prefix = "sqlite:///"
else:
    prefix = "sqlite:////"


class BaseConfig:
    TODOLIST_ITEM_PER_PAGE = 20
    # SERVER_NAME = 'todoism.dev:5000'  # enable subdomain support
    SECRET_KEY = os.getenv("SECRET_KEY", "a secret string")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL",prefix+os.path.join(basedir, "data.db"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TODOLIST_LOCALES = ['en_US', 'zh_Hans_CN']
    BABEL_DEFAULT_LOCALE = TODOLIST_LOCALES[0]


class DevelopmentConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///"
    WTF_CSRF_ENABLED = False


class HerokuConfig(ProductionConfig):
    pass

config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "heroku": HerokuConfig
}