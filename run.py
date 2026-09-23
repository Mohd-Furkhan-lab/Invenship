from app.main import get_app
from models.user import User
from models.revoked_token import TokenBlacklist
from models.category import Category
from models.products import Products
from config.redis import r
from config.cloudinary import cloudinary
from config.database import Base,engine


app = get_app()

Base.metadata.create_all(bind=engine)

