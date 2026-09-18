from sqlalchemy.orm import Session
from app.models import UserProfileModel
from datetime import datetime

def get_or_create_user(db: Session, user_id: str) -> UserProfileModel:
    user = db.query(UserProfileModel).filter(UserProfileModel.user_id == user_id).first()
    if not user:
        # Create user profile
        user = UserProfileModel(
            user_id=user_id,
            display_name=f"Reporter {user_id[-4:] if len(user_id) >= 4 else user_id}",
            total_points=0,
            reports_count=0,
            badge="Civic Scout"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

def award_points(db: Session, user_id: str, points: int = 10) -> tuple[int, str]:
    user = get_or_create_user(db, user_id)
    user.total_points += points
    user.reports_count += 1
    user.last_active = datetime.utcnow()
    
    # Update badge based on milestones
    if user.total_points >= 150:
        user.badge = "Trust Champion 🏆"
    elif user.total_points >= 75:
        user.badge = "Community Guardian 🛡️"
    elif user.total_points >= 25:
        user.badge = "Local Watchdog 🔍"
    else:
        user.badge = "Civic Scout 🌱"
        
    db.commit()
    db.refresh(user)
    return user.total_points, user.badge
