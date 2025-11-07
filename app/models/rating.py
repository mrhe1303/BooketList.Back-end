from app import db
from datetime import datetime
from typing import Dict, Any
from sqlalchemy import Integer, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Rating(db.Model):
    __tablename__ = 'calificacion'
    
    id_calificacion: Mapped[int] = mapped_column(primary_key=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey('usuarios.id_usuario'), nullable=False)
    id_libro: Mapped[int] = mapped_column(ForeignKey('libros.id_libros'), nullable=False)
    calificacion: Mapped[int] = mapped_column(Integer, nullable=True)  # ✅ CHANGED: Now nullable
    resena: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    
    # Relaciones
    usuario: Mapped["User"] = relationship(back_populates="calificaciones")
    libro: Mapped["Book"] = relationship(back_populates="calificaciones")
    
    def serialize(self) -> Dict[str, Any]:
        return {
            "id_calificacion": self.id_calificacion,
            "id_usuario": self.id_usuario,
            "id_libro": self.id_libro,
            "calificacion": self.calificacion,
            "resena": self.resena,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }