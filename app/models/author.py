from app import db
from datetime import datetime
from typing import List, Dict, Any
from sqlalchemy import String, DateTime, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Author(db.Model):
    __tablename__ = 'autores'
    
    id_autor: Mapped[int] = mapped_column(primary_key=True)
    nombre_autor: Mapped[str] = mapped_column(String(100), nullable=False)
    apellido_autor: Mapped[str] = mapped_column(String(100), nullable=False)
    biografia_autor: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    
    # Relación con libros
    libros: Mapped[List["Book"]] = relationship(back_populates="autor")
    
    def serialize(self) -> Dict[str, Any]:
        return {
            "id_autor": self.id_autor,
            "nombre_autor": self.nombre_autor,
            "apellido_autor": self.apellido_autor,
            "biografia_autor": self.biografia_autor,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }