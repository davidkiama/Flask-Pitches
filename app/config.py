

import os


class Config:
    pass


class DevConfig(Config):
    DEBUG = True


class ProdConfig(Config):
    DEBUG = True


    #  administrator list
config_options = {
    'development': DevConfig,
    'production': ProdConfig,
}
