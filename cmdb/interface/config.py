class Config:
    """Parent configuration class."""
    TESTING = False
    DEBUG = False
    ENV = 'production'


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True
    ENV = 'development'


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    DEBUG = True
    ENV = 'testing'


class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False
    ENV = 'production'


class RestConfig(Config):
    DEBUG = False
    ENV = 'production'
    APPLICATION_ROOT = '/rest/'


class RestDevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'rest': RestConfig,
    'rest_development': RestDevelopmentConfig
}
