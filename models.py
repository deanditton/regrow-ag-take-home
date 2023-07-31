from typing import Optional

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str


class Pasture(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="user.id", index=True)
    name: str


class PastureRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    pasture_id: int = Field(default=None, foreign_key="pasture.id", index=True)
    year: int = Field(index=True)

    crop_type: Optional[str]
    tillage_depth: Optional[float]
    tilled: Optional[bool]
    comments: Optional[str]
    external_account_id: Optional[str]
