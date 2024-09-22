import uuid
from sqlalchemy import Column, Enum, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class Car(Base):
    __tablename__ = 'cars'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    color = Column(Enum('yellow', 'blue', 'gray', name='car_color'), nullable=False)
    model = Column(Enum('hatch', 'sedan', 'convertible', name='car_model'), nullable=False)
    owner_id = Column(UUID(as_uuid=True), ForeignKey('owners.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime, server_default=func.current_timestamp())
    updated_at = Column(DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    deleted_at = Column(DateTime, nullable=True)

    def to_dict(self):
        return {
            'id': str(self.id),
            'color': self.color,
            'model': self.model,
            'owner_id': str(self.owner_id),
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at
        }
