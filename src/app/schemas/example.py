import uuid

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Example(Base):
    __tablename__ = "example"
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        comment="Primary key identifier for the record",
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
        index=True,
        comment="User ID from Supabase auth.users",
    )
