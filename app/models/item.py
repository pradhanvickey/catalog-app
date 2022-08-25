from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Float, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    price = Column(Float)
    image_url = Column(String, unique=True)
    is_active = Column(Boolean, default=True)
    menu_id = Column(Integer, ForeignKey("menus.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))

    menu = relationship("Menu", back_populates="items")
    owner = relationship("User", back_populates="items")

    __table_args__ = (UniqueConstraint('title', 'menu_id'),)
