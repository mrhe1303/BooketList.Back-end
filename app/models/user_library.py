from app import db
from datetime import datetime
from sqlalchemy import String, DateTime, Integer, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

class UserLibrary(db.Model):
    __tablename__ = 'biblioteca_usuario'
    
    id_biblioteca: Mapped[int] = mapped_column(primary_key=True)
    id_usuario: Mapped[int] = mapped_column(Integer, ForeignKey('usuarios.id_usuario'), nullable=False)
    id_libro: Mapped[int] = mapped_column(Integer, ForeignKey('libros.id_libros'), nullable=False)
    
    # Campo para estado de lectura
    # ✅ CHANGED: Only two valid states now (leido is handled by Rating table)
    estado_lectura: Mapped[str] = mapped_column(
        String(20), 
        default='quiero_leer',
        nullable=False
    )
    # Valores posibles: 'quiero_leer', 'leyendo'
    # Nota: 'leido' ya NO es válido aquí - se maneja en la tabla Rating
    
    # Timestamps con timezone
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
    usuario: Mapped["User"] = relationship(back_populates="biblioteca")
    libro: Mapped["Book"] = relationship(back_populates="biblioteca")
    
    def serialize(self):
        return {
            'id_biblioteca': self.id_biblioteca,
            'id_usuario': self.id_usuario,
            'id_libro': self.id_libro,
            'estado_lectura': self.estado_lectura,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }