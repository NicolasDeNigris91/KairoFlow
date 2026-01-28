from fastapi import APIRouter, Depends
from sqlmodel import Session, select, func, and_
from datetime import datetime, timedelta, date, timezone
from typing import Dict, List

from app.core.database import get_session
from app.models.activity import Activity, ActivityType
from app.services.auth import get_current_user

router = APIRouter()

@router.get("/")
def get_user_stats(
    session: Session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    today = datetime.now(timezone.utc).date()
    week_ago = today - timedelta(days=7)
    
    total_activities_query = select(func.count(Activity.id)).where(
        Activity.user_id == current_user.id
    )
    total_activities = session.exec(total_activities_query).first() or 0
    
    total_minutes_query = select(func.sum(Activity.duration_minutes)).where(
        Activity.user_id == current_user.id
    )
    total_minutes = session.exec(total_minutes_query).first() or 0
    
    week_minutes_query = select(func.sum(Activity.duration_minutes)).where(
        and_(
            Activity.user_id == current_user.id,
            func.date(Activity.date) >= week_ago
        )
    )
    week_minutes = session.exec(week_minutes_query).first() or 0
    
    activities_by_type = {}
    for activity_type in ActivityType:
        type_query = select(func.count(Activity.id)).where(
            and_(
                Activity.user_id == current_user.id,
                Activity.activity_type == activity_type
            )
        )
        count = session.exec(type_query).first() or 0
        if count > 0:
            activities_by_type[activity_type.value] = count
    
    most_frequent_type = max(activities_by_type.items(), key=lambda x: x[1]) if activities_by_type else None
    
    recent_activities_query = select(Activity).where(
        Activity.user_id == current_user.id
    ).order_by(Activity.date.desc()).limit(5)
    recent_activities = session.exec(recent_activities_query).all()
    
    consecutive_days = 0
    current_day = today
    while True:
        day_query = select(func.count(Activity.id)).where(
            and_(
                Activity.user_id == current_user.id,
                func.date(Activity.date) == current_day
            )
        )
        day_count = session.exec(day_query).first() or 0
        
        if day_count > 0:
            consecutive_days += 1
            current_day = current_day - timedelta(days=1)
        else:
            break
    
    daily_goal = 480
    daily_minutes_query = select(func.sum(Activity.duration_minutes)).where(
        and_(
            Activity.user_id == current_user.id,
            func.date(Activity.date) == today
        )
    )
    today_minutes = session.exec(daily_minutes_query).first() or 0
    daily_goal_percentage = min(100, int((today_minutes / daily_goal) * 100)) if daily_goal > 0 else 0
    
    return {
        "total_activities": total_activities,
        "total_minutes": total_minutes,
        "total_hours": round(total_minutes / 60, 1),
        "week_minutes": week_minutes,
        "week_hours": round(week_minutes / 60, 1),
        "activities_by_type": activities_by_type,
        "most_frequent_type": most_frequent_type[0] if most_frequent_type else None,
        "consecutive_days": consecutive_days,
        "daily_goal_percentage": daily_goal_percentage,
        "today_minutes": today_minutes,
        "recent_activities": recent_activities
    }