from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime, timezone

from app.core.database import get_session
from app.models.activity import Activity, ActivityType, ActivityCreate, ActivityUpdate
from app.services.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=Activity, status_code=status.HTTP_201_CREATED)
def create_activity(
    activity_data: ActivityCreate,
    session: Session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    activity = Activity(
        **activity_data.dict(),
        user_id=current_user.id,
        updated_at=datetime.now(timezone.utc)
    )
    
    session.add(activity)
    session.commit()
    session.refresh(activity)
    return activity

@router.get("/", response_model=List[Activity])
def get_activities(
    skip: int = 0,
    limit: int = 100,
    activity_type: Optional[ActivityType] = None,
    session: Session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    query = select(Activity).where(Activity.user_id == current_user.id)
    
    if activity_type:
        query = query.where(Activity.activity_type == activity_type)
    
    query = query.offset(skip).limit(limit).order_by(Activity.date.desc())
    
    activities = session.exec(query).all()
    return activities

@router.get("/{activity_id}", response_model=Activity)
def get_activity(
    activity_id: int,
    session: Session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    activity = session.get(Activity, activity_id)
    
    if not activity or activity.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    return activity

@router.put("/{activity_id}", response_model=Activity)
def update_activity(
    activity_id: int,
    activity_update: ActivityUpdate,
    session: Session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    activity = session.get(Activity, activity_id)
    
    if not activity or activity.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    for key, value in activity_update.dict(exclude_unset=True).items():
        setattr(activity, key, value)
    
    activity.updated_at = datetime.now(timezone.utc)
    session.add(activity)
    session.commit()
    session.refresh(activity)
    
    return activity

@router.delete("/{activity_id}")
def delete_activity(
    activity_id: int,
    session: Session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    activity = session.get(Activity, activity_id)
    
    if not activity or activity.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    session.delete(activity)
    session.commit()
    
    return {"message": "Activity deleted successfully"}