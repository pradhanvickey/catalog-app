from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.database import Base


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

    owner = relationship("User", back_populates="stores")
    menus = relationship("Menu", back_populates="store")

    __table_args__ = (UniqueConstraint('name', 'owner_id'),)
