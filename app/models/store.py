import uuid

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.database import Base


def generate_uuid():
    return str(uuid.uuid4())


class Store(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    contact_no = Column(String)
    address = Column(String)
    logo_url = Column(String, unique=True)
    qr_code_url = Column(String, unique=True)
    is_active = Column(Boolean, default=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    unique_store_key = Column(String, nullable=False, default=generate_uuid)

    owner = relationship("User", back_populates="stores")
    menus = relationship("Menu", back_populates="store")

    __table_args__ = (UniqueConstraint('name', 'owner_id'),)
