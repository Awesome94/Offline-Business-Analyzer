import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    TOKEN_EXPIRATION = os.environ['TOKEN_EXPIRATION']
    SSL_REDIRECT = False
    
    @staticmethod
    def init_app(app):
        pass

class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True

class HerokuConfig(ProductionConfig): 
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)
        # log to stderr
        import logging
        from logging import StreamHandler 
        file_handler = StreamHandler() 
        file_handler.setLevel(logging.INFO) 
        app.logger.addHandler(file_handler)
        SSL_REDIRECT = True if os.environ.get('DYNO') else False
        # handle reverse proxy
        from werkzeug.contrib.fixers import ProxyFix 
        app.wsgi_app = ProxyFix(app.wsgi_app)


class DockerConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        import logging
        from logging import StreamHandler
        file_handler = StreamHandler
        file_handler.setLevel(logging.INFO)
        app.logger.addhandler(file_handler)

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'docker': DockerConfig,
    'heroku': HerokuConfig,
    'default': DevelopmentConfig

}