import sqlalchemy
from model import *

DSN = ""
engine = sqlalchemy.create_engine(DSN)

drop_tables(engine)
create_tables(engine)
