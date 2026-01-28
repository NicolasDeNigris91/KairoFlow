from sqlmodel import SQLModel, Field, Column, JSON, Index
from datetime import datetime, timezone
from typing import Optional, List
from enum import Enum

class ActivityType(str, Enum):
    WORK = "WORK"
    STUDY = "STUDY"
    EXERCISE = "EXERCISE"
    LEISURE = "LEISURE"
    OTHER = "OTHER"

class ActivityBase(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    activity_type: ActivityType = Field(default=ActivityType.OTHER)
    duration_minutes: int = Field(gt=0, le=1440)
    description: Optional[str] = Field(default=None, max_length=1000)
    tags: List[str] = Field(default=[], sa_column=Column(JSON))
    date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ActivityCreate(ActivityBase):
    pass

class ActivityUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    activity_type: Optional[ActivityType] = None
    duration_minutes: Optional[int] = Field(default=None, gt=0, le=1440)
    description: Optional[str] = Field(default=None, max_length=1000)
    tags: Optional[List[str]] = None
    date: Optional[datetime] = None

class Activity(ActivityBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    @property
    def duration_hours(self) -> float:
        return self.duration_minutes / 60
    
    @property
    def is_recent(self) -> bool:
        return (datetime.now(timezone.utc) - self.created_at).total_seconds() < 86400
    
    def get_formatted_date(self, format_str: str = "%d/%m/%Y %H:%M") -> str:
        return self.date.strftime(format_str)
    
    def add_tag(self, tag: str):
        if tag not in self.tags:
            self.tags.append(tag)
    
    def has_tag(self, tag: str) -> bool:
        return tag in self.tags
    
    __table_args__ = (
        Index('idx_user_date', 'user_id', 'date'),
        Index('idx_activity_type', 'activity_type'),
    )