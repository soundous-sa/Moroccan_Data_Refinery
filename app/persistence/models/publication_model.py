from datetime import datetime

from sqlalchemy import (
    String,
    DateTime,
    Integer,
    Text,
    Boolean
)

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column
)


class Base(DeclarativeBase):
    pass


class PublicationModel(Base):

    __tablename__ = "publications"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    title: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    publication_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    url: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        unique=True
    )

    source_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    sector: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    category: Mapped[str] = mapped_column(
        String(100),
        nullable=False
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

    def __repr__(self):

        return (
            f"<PublicationModel("
            f"id={self.id}, "
            f"title='{self.title}', "
            f"source='{self.source_id}', "
            f"status='{self.status}'"
            f")>"
        )