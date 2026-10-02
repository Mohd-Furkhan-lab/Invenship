import cloudinary
from env_loader import load_env
import os

load_env()

cloudinary.config(
    cloud_name = os.getenv("cloud_name"),
    api_key = os.getenv("api_key"),
    api_secret = os.getenv("api_secret")
)
