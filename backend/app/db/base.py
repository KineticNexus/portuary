# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base
from app.models.user import User
from app.models.vessel import Vessel
from app.models.cargo import Cargo
from app.models.dock import Dock
from app.models.schedule import Schedule