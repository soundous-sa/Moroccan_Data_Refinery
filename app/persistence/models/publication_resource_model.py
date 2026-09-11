from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column

from app.persistence.models.publication_model import Base


class PublicationResourceModel(Base):

    __tablename__ = "publication_resources"

    __table_args__ = (
        UniqueConstraint(
            "publication_id",
            "url",
            name="uq_publication_resources_publication_url"
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    publication_id: Mapped[int] = mapped_column(
        ForeignKey("publications.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    title: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    url: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    filename: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True
    )

    file_type: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    content_type: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    file_path: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    file_size: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        default=0
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="DISCOVERED"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.now
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now
    )
