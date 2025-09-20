from sqlalchemy import create_engine
from database import Base
from models import Sweet

# URL-encode password (@ → %40)
DATABASE_URL = "mysql+pymysql://root:Sakshi%402004@localhost:3306/sweetshop"

engine = create_engine(DATABASE_URL, echo=True)

# Create tables
Base.metadata.create_all(engine)
print("Tables created successfully!")
