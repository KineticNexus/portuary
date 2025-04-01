import logging
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

logger = logging.getLogger(__name__)


def init_db(db: Session) -> None:
    # Create initial admin user
    admin_user = db.query(User).filter(User.email == "admin@portuary.com").first()
    if not admin_user:
        user_in = UserCreate(
            email="admin@portuary.com",
            password="admin",
            full_name="Admin User",
            is_superuser=True,
        )
        user = User(
            email=user_in.email,
            hashed_password=get_password_hash(user_in.password),
            full_name=user_in.full_name,
            is_superuser=user_in.is_superuser,
        )
        db.add(user)
        db.commit()
        logger.info("Initial admin user created")


def create_initial_data() -> None:
    db = SessionLocal()
    try:
        init_db(db)
    except Exception as e:
        logger.error(f"Error creating initial data: {e}")
    finally:
        db.close()