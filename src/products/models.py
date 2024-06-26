from database import metadata
from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, Boolean, ForeignKey

# from src.database import metadata

products_model = Table(
    "products",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("UnikalnyjKodProdukta", String, nullable=True),
    Column("NomerPartii", Integer, nullable=True),
    Column("DataPartii", TIMESTAMP, nullable=True),
    Column("is_aggregated", Boolean, nullable=True),
    Column("aggregated_at", TIMESTAMP, nullable=True),
    Column("assignment", ForeignKey("shift_assignment.NomerPartii"), nullable=True),
)
