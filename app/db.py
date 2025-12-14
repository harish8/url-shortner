from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime, timezone

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class Url(db.Model):
    id: Mapped[int] = mapped_column(primary_key = True)
    url: Mapped[str] = mapped_column(nullable=False)
    short_code: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    click_count: Mapped[int] = mapped_column(default=0)
