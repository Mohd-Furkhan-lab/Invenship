import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from backend.app.main import get_app
from backend.models.user import User
from backend.models.revoked_token import TokenBlacklist
from backend.models.category import Category
from backend.models.products import Products
from backend.models.sales import Sales
from backend.models.suppliers import Supplier
from backend.models.purchases import Purchase
from backend.config.redis import r
from backend.config.cloudinary import cloudinary
from backend.config.database import Base,engine
from fastapi.middleware.cors import CORSMiddleware


app = get_app()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"

    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

