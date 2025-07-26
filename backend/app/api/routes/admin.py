from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel, EmailStr

from app.core.database import get_db
from app.core.security import get_current_user, require_permission, log_security_event
from app.models.user import User, UserSession, SecurityLog, ROLE_PERMISSIONS

router = APIRouter()

# Pydantic models
class UserUpdate(BaseModel):
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    roles: Optional[List[str]] = None
    subscription_tier: Optional[str] = None
    subscription_duration_days: Optional[int] = 30

class RoleAssignment(BaseModel):
    user_id: int
    roles: List[str]

class SubscriptionUpdate(BaseModel):
    user_id: int
    tier: str  # basic, premium, pro
    duration_days: int = 30

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: str
    is_active: bool
    is_verified: bool
    is_admin: bool
    subscription_tier: str
    subscription_status: str
    is_subscriber: bool
    roles: List[str]
    permissions: List[str]
    created_at: Optional[str]
    last_login: Optional[str]
    subscription_expires: Optional[str]

    class Config:
        from_attributes = True

class SystemStats(BaseModel):
    total_users: int
    active_users: int
    verified_users: int
    admin_users: int
    subscriber_users: int
    free_users: int
    users_by_role: dict
    users_by_subscription: dict
    recent_registrations: int
    recent_logins: int

@router.get("/users", response_model=List[UserResponse])
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    role: Optional[str] = Query(None),
    subscription_tier: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    search: Optional[str] = Query(None),
    current_user: User = Depends(require_permission("read_users")),
    db: Session = Depends(get_db)
):
    """Get all users with filtering and pagination."""
    
    query = db.query(User)
    
    # Apply filters
    if role:
        query = query.filter(User.roles.contains([role]))
    
    if subscription_tier:
        query = query.filter(User.subscription_tier == subscription_tier)
    
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (User.email.ilike(search_term)) |
            (User.username.ilike(search_term))
        )
    
    # Apply pagination
    users = query.offset(skip).limit(limit).all()
    
    log_security_event("admin_users_viewed", current_user.id, {
        "filters": {
            "role": role,
            "subscription_tier": subscription_tier,
            "is_active": is_active,
            "search": search
        },
        "results_count": len(users)
    })
    
    return users

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user: User = Depends(require_permission("read_users")),
    db: Session = Depends(get_db)
):
    """Get specific user details."""
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    log_security_event("admin_user_viewed", current_user.id, {
        "target_user_id": user_id
    })
    
    return user

@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    current_user: User = Depends(require_permission("write_users")),
    db: Session = Depends(get_db)
):
    """Update user information."""
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Prevent admin from demoting themselves
    if user.id == current_user.id and user_update.is_active == False:
        raise HTTPException(status_code=400, detail="Cannot deactivate your own account")
    
    # Update fields
    if user_update.is_active is not None:
        user.is_active = user_update.is_active
    
    if user_update.is_verified is not None:
        user.is_verified = user_update.is_verified
    
    if user_update.roles is not None:
        user.set_roles(user_update.roles)
    
    if user_update.subscription_tier is not None:
        if user_update.subscription_tier == "admin":
            user.promote_to_admin()
        elif user_update.subscription_tier in ["basic", "premium", "pro"]:
            user.upgrade_subscription(
                user_update.subscription_tier,
                user_update.subscription_duration_days or 30
            )
        elif user_update.subscription_tier == "free":
            user.downgrade_subscription()
    
    db.commit()
    db.refresh(user)
    
    log_security_event("admin_user_updated", current_user.id, {
        "target_user_id": user_id,
        "changes": user_update.dict(exclude_unset=True)
    })
    
    return user

@router.post("/users/{user_id}/promote-admin")
async def promote_to_admin(
    user_id: int,
    current_user: User = Depends(require_permission("manage_roles")),
    db: Session = Depends(get_db)
):
    """Promote user to admin role."""
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.is_admin:
        raise HTTPException(status_code=400, detail="User is already an admin")
    
    user.promote_to_admin()
    db.commit()
    
    log_security_event("user_promoted_to_admin", current_user.id, {
        "target_user_id": user_id,
        "promoted_by": current_user.id
    })
    
    return {"message": f"User {user.username} promoted to admin"}

@router.post("/users/{user_id}/demote-admin")
async def demote_from_admin(
    user_id: int,
    current_user: User = Depends(require_permission("manage_roles")),
    db: Session = Depends(get_db)
):
    """Demote user from admin role."""
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not user.is_admin:
        raise HTTPException(status_code=400, detail="User is not an admin")
    
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot demote yourself")
    
    user.demote_from_admin()
    db.commit()
    
    log_security_event("user_demoted_from_admin", current_user.id, {
        "target_user_id": user_id,
        "demoted_by": current_user.id
    })
    
    return {"message": f"User {user.username} demoted from admin"}

@router.post("/users/{user_id}/upgrade-subscription")
async def upgrade_user_subscription(
    user_id: int,
    subscription: SubscriptionUpdate,
    current_user: User = Depends(require_permission("manage_subscriptions")),
    db: Session = Depends(get_db)
):
    """Upgrade user subscription."""
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    valid_tiers = ["basic", "premium", "pro"]
    if subscription.tier not in valid_tiers:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid subscription tier. Must be one of: {valid_tiers}"
        )
    
    user.upgrade_subscription(subscription.tier, subscription.duration_days)
    db.commit()
    
    log_security_event("user_subscription_upgraded", current_user.id, {
        "target_user_id": user_id,
        "tier": subscription.tier,
        "duration_days": subscription.duration_days
    })
    
    return {
        "message": f"User {user.username} upgraded to {subscription.tier} subscription",
        "expires": user.subscription_expires.isoformat() if user.subscription_expires else None
    }

@router.post("/users/{user_id}/downgrade-subscription")
async def downgrade_user_subscription(
    user_id: int,
    current_user: User = Depends(require_permission("manage_subscriptions")),
    db: Session = Depends(get_db)
):
    """Downgrade user to free subscription."""
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.downgrade_subscription()
    db.commit()
    
    log_security_event("user_subscription_downgraded", current_user.id, {
        "target_user_id": user_id
    })
    
    return {"message": f"User {user.username} downgraded to free subscription"}

@router.post("/users/{user_id}/unlock")
async def unlock_user_account(
    user_id: int,
    current_user: User = Depends(require_permission("write_users")),
    db: Session = Depends(get_db)
):
    """Unlock a locked user account."""
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not user.is_locked:
        raise HTTPException(status_code=400, detail="User account is not locked")
    
    user.unlock_account()
    db.commit()
    
    log_security_event("user_account_unlocked", current_user.id, {
        "target_user_id": user_id
    })
    
    return {"message": f"User {user.username} account unlocked"}

@router.get("/users/{user_id}/sessions")
async def get_user_sessions(
    user_id: int,
    current_user: User = Depends(require_permission("read_users")),
    db: Session = Depends(get_db)
):
    """Get user's active sessions."""
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    sessions = db.query(UserSession).filter(
        UserSession.user_id == user_id,
        UserSession.is_active == True
    ).all()
    
    return {
        "user_id": user_id,
        "username": user.username,
        "sessions": [
            {
                "id": session.id,
                "ip_address": session.ip_address,
                "user_agent": session.user_agent,
                "created_at": session.created_at.isoformat(),
                "last_activity": session.last_activity.isoformat(),
                "expires_at": session.expires_at.isoformat(),
                "is_expired": session.is_expired
            }
            for session in sessions
        ]
    }

@router.delete("/users/{user_id}/sessions/{session_id}")
async def terminate_user_session(
    user_id: int,
    session_id: int,
    current_user: User = Depends(require_permission("write_users")),
    db: Session = Depends(get_db)
):
    """Terminate a specific user session."""
    
    session = db.query(UserSession).filter(
        UserSession.id == session_id,
        UserSession.user_id == user_id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session.deactivate()
    db.commit()
    
    log_security_event("user_session_terminated", current_user.id, {
        "target_user_id": user_id,
        "session_id": session_id
    })
    
    return {"message": "Session terminated successfully"}

@router.get("/security-logs")
async def get_security_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    user_id: Optional[int] = Query(None),
    event_type: Optional[str] = Query(None),
    success: Optional[bool] = Query(None),
    current_user: User = Depends(require_permission("view_security_logs")),
    db: Session = Depends(get_db)
):
    """Get security logs with filtering."""
    
    query = db.query(SecurityLog)
    
    if user_id:
        query = query.filter(SecurityLog.user_id == user_id)
    
    if event_type:
        query = query.filter(SecurityLog.event_type == event_type)
    
    if success is not None:
        query = query.filter(SecurityLog.success == success)
    
    logs = query.order_by(SecurityLog.created_at.desc()).offset(skip).limit(limit).all()
    
    return {
        "logs": [log.to_dict() for log in logs],
        "total": query.count()
    }

@router.get("/system-stats", response_model=SystemStats)
async def get_system_stats(
    current_user: User = Depends(require_permission("read_system")),
    db: Session = Depends(get_db)
):
    """Get system statistics."""
    
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    verified_users = db.query(User).filter(User.is_verified == True).count()
    admin_users = db.query(User).filter(User.is_admin == True).count()
    subscriber_users = db.query(User).filter(User.is_subscriber == True).count()
    free_users = db.query(User).filter(User.subscription_tier == "free").count()
    
    # Users by role
    users_by_role = {}
    for role in ["user", "subscriber", "admin", "moderator"]:
        users_by_role[role] = db.query(User).filter(User.roles.contains([role])).count()
    
    # Users by subscription
    users_by_subscription = {}
    for tier in ["free", "basic", "premium", "pro", "admin"]:
        users_by_subscription[tier] = db.query(User).filter(User.subscription_tier == tier).count()
    
    # Recent activity
    recent_registrations = db.query(User).filter(
        User.created_at >= datetime.utcnow() - timedelta(days=7)
    ).count()
    
    recent_logins = db.query(User).filter(
        User.last_login >= datetime.utcnow() - timedelta(days=7)
    ).count()
    
    return SystemStats(
        total_users=total_users,
        active_users=active_users,
        verified_users=verified_users,
        admin_users=admin_users,
        subscriber_users=subscriber_users,
        free_users=free_users,
        users_by_role=users_by_role,
        users_by_subscription=users_by_subscription,
        recent_registrations=recent_registrations,
        recent_logins=recent_logins
    )

@router.get("/roles")
async def get_available_roles(
    current_user: User = Depends(require_permission("read_system")),
    db: Session = Depends(get_db)
):
    """Get available roles and their permissions."""
    
    return {
        "roles": ROLE_PERMISSIONS,
        "total_roles": len(ROLE_PERMISSIONS),
        "total_permissions": len(set().union(*ROLE_PERMISSIONS.values()))
    } 