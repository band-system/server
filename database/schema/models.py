from sqlalchemy.orm import mapped_column, Mapped
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
from dataclasses import dataclass

db = SQLAlchemy()

@dataclass
class User(db.Model):
    id: Mapped[str] = mapped_column(primary_key=True, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(db.String, nullable=False)
    name: Mapped[str] = mapped_column(db.VARCHAR, nullable=False)
    prefered_time: Mapped[str] = mapped_column(db.String, nullable=True)
    bio: Mapped[str] = mapped_column(db.VARCHAR, nullable=True)
    photo: Mapped[str] = mapped_column(db.String, nullable=True)
    ig: Mapped[str] = mapped_column(db.String, nullable=True)
    fb: Mapped[str] = mapped_column(db.String, nullable=True)
    email: Mapped[str] = mapped_column(db.String, nullable=True)

@dataclass
class Band(db.Model):
    id: Mapped[str] = mapped_column(primary_key=True, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(db.String, nullable=False)
    name: Mapped[str] = mapped_column(db.VARCHAR, nullable=False)
    practice_time: Mapped[str] = mapped_column(db.String, nullable=True)
    bio: Mapped[str] = mapped_column(db.VARCHAR, nullable=True)
    photo: Mapped[str] = mapped_column(db.String, nullable=True)
    ig: Mapped[str] = mapped_column(db.String, nullable=True)
    fb: Mapped[str] = mapped_column(db.String, nullable=True)
    contact_window: Mapped[str] = mapped_column(db.String, nullable=True)

@dataclass
class Instrument(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.VARCHAR, nullable=False)

@dataclass   
class Region(db.Model):
    id: Mapped[str] = mapped_column(db.String, primary_key=True)
    name: Mapped[str] = mapped_column(db.VARCHAR, nullable=False)

@dataclass
class Style(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.VARCHAR, nullable=False)


User_Instrument = db.Table(
    'User_Instrument',
    db.Column("user_id", sa.ForeignKey(User.id), primary_key=True),
    db.Column("instrument_id", sa.ForeignKey(Instrument.id), primary_key=True),
    db.Column("experience", sa.Integer)
)

User_Region = db.Table(
    'User_Region',
    db.Column("user_id", sa.ForeignKey(User.id), primary_key=True),
    db.Column("region_id", sa.ForeignKey(Region.id), primary_key=True)
)

User_Style = db.Table(
    'User_Style',
    db.Column("user_id", sa.ForeignKey(User.id), primary_key=True),
    db.Column("style_id", sa.ForeignKey(Style.id), primary_key=True)
)

User_Band = db.Table(
    'User_Band',
    db.Column("user_id", sa.ForeignKey(User.id), primary_key=True),
    db.Column("band_id", sa.ForeignKey(Band.id), primary_key=True),
    db.Column("status", sa.Integer)
)

Band_Style = db.Table(
    'Band_Style',
    db.Column("band_id",sa.ForeignKey(Band.id), primary_key=True ),
    db.Column("style_id", sa.ForeignKey(Style.id), primary_key=True)
)

Band_Region = db.Table(
    'Band_Region',
    db.Column("band_id",sa.ForeignKey(Band.id), primary_key=True ),
    db.Column("region_id", sa.ForeignKey(Region.id), primary_key=True)
)


