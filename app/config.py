class Config:
    HOST = "http://127.0.0.1:8188"  # ComfyUI host
    SECRET_KEY = "supersecret"

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
