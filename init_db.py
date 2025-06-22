import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.database import Base, engine
from app.db import models

Base.metadata.create_all(bind=engine)
print("✅ Database initialized.")
