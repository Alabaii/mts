from datetime import datetime
import uuid
from sqlalchemy import JSON, UUID, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Faults(Base):
    __tablename__ = "faults"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ip: Mapped[str]
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    body_fault: Mapped[dict] = mapped_column(JSON, nullable=False)  # Используем dict для JSON
    code_fault: Mapped[int]
    comment: Mapped[str]