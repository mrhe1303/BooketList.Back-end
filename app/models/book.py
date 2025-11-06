from app import db
from datetime import datetime
from typing import List, Dict, Any, Optional
from sqlalchemy import String, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Book(db.Model):
    __tablename__ = 'libros'

    id_libros: Mapped[int] = mapped_column(primary_key=True)
    titulo_libro: Mapped[str] = mapped_column(String(200), nullable=False)
    id_autor: Mapped[int] = mapped_column(ForeignKey('autores.id_autor'), nullable=False)
    genero_libro: Mapped[str] = mapped_column(String(50), nullable=False)
    descripcion_libros: Mapped[str] = mapped_column(Text, nullable=False)
    enlace_asin_libro: Mapped[str] = mapped_column(String(100), nullable=False)
    enlace_portada_libro: Mapped[str] = mapped_column(String(500), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    calificaciones: Mapped[List["Rating"]] = relationship(back_populates="libro")
    biblioteca: Mapped[List["UserLibrary"]] = relationship(back_populates="libro")
    autor: Mapped["Author"] = relationship(back_populates="libros")

    def serialize(self) -> Dict[str, Any]:
        return {
        "id_libros": self.id_libros,
            "titulo_libro": self.titulo_libro,
            "id_autor": self.id_autor,
            "autor": self.autor.serialize() if self.autor else None,
            "genero_libro": self.genero_libro,
            "descripcion_libros": self.descripcion_libros,
            "enlace_asin_libro": self.enlace_asin_libro,
            "enlace_portada_libro": self.enlace_portada_libro,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
