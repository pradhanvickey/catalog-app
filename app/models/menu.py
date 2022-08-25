from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.database import Base


class Menu(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True)
    is_active = Column(Boolean, default=True)
    image_url = Column(String, unique=True)
    store_id = Column(Integer, ForeignKey("stores.id"))

    store = relationship("Store", back_populates="menus")
    items = relationship("Item", back_populates="menu")

    __table_args__ = (UniqueConstraint('title', 'store_id'),)
