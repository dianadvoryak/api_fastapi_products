from sqlalchemy import Table, Column, Integer, String, Boolean, TIMESTAMP

from database import metadata
# from src.database import metadata

shift_assignment_model = Table(
    "shift_assignment",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("StatusZakrytiya", Boolean, nullable=True),
    Column("closed_at", TIMESTAMP, nullable=True),
    Column("PredstavlenieZadaniyaNaSmenu", String, nullable=True),
    Column("Liniya", String, nullable=True),
    Column("Smena", String, nullable=True),
    Column("Brigada", String, nullable=True),
    Column("NomerPartii", Integer, nullable=True,  unique=True),
    Column("DataPartii", TIMESTAMP, nullable=True, unique=True),
    Column("Nomenklatura", String, nullable=True),
    Column("KodEKN", String, nullable=True),
    Column("IdentifikatorRC", String, nullable=True),
    Column("DataVremyaNachalaSmeny", TIMESTAMP, nullable=False),
    Column("DataVremyaOkonchaniyaSmeny", TIMESTAMP, nullable=True),
)

