from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime, timedelta
from typing import List, Dict, Any
import json

from app.core.database import Base

# Define role permissions
ROLE_PERMISSIONS = {
    "admin": [
        "read_predictions",
        "write_predictions", 
        "read_analytics",
        "write_analytics",
        "read_games",
        "write_games",
        "read_users",
        "write_users",
        "read_system",
        "write_system",
        "manage_scraping",
        "manage_ai",
        "view_security_logs",
        "manage_roles",
        "export_data",
        "manage_subscriptions"
    ],
    "subscriber": [
        "read_predictions",
        "read_analytics", 
        "read_games",
        "write_user_tips",
        "read_user_tips",
        "read_own_profile",
        "write_own_profile"
    ],
    "user": [
        "read_predictions",
        "read_analytics",
        "read_games",
        "read_own_profile",
        "write_own_profile"
    ],
    "moderator": [
        "read_predictions",
        "read_analytics",
        "read_games", 
        "read_users",
        "write_users",
        "moderate_user_tips",
        "view_security_logs"
    ]
}

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    
    # Authentication fields
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    # Profile information
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String)  # Encrypted in production
    
    # Account status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    
    # Subscription and roles
    subscription_tier = Column(String, default="free")  # free, basic, premium, pro
    subscription_expires = Column(DateTime)
    roles = Column(JSON, default=list)  # ["user", "subscriber", "admin", "moderator"]
    permissions = Column(JSON, default=list)
    
    # Security fields
    email_verification_token = Column(String, unique=True)
    password_reset_token = Column(String, unique=True)
    password_reset_expires = Column(DateTime)
    last_login = Column(DateTime)
    failed_login_attempts = Column(Integer, default=0)
    account_locked_until = Column(DateTime)
    
    # API access
    api_key_hash = Column(String, unique=True)
    api_key_created = Column(DateTime)
    api_key_last_used = Column(DateTime)
    
    # Privacy and preferences
    privacy_settings = Column(JSON, default=dict)
    notification_settings = Column(JSON, default=dict)
    
    # Audit fields
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_password_change = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user_tips = relationship("UserTip", back_populates="user")
    sessions = relationship("UserSession", back_populates="user")
    security_logs = relationship("SecurityLog", back_populates="user")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Set default roles and permissions
        if not self.roles:
            self.roles = ["subscriber"]
        if not self.permissions:
            self.permissions = ROLE_PERMISSIONS.get("subscriber", [])
        if not self.privacy_settings:
            self.privacy_settings = {
                "profile_visible": True,
                "tips_visible": True,
                "analytics_visible": True
            }
        if not self.notification_settings:
            self.notification_settings = {
                "email_notifications": True,
                "push_notifications": True,
                "weekly_summary": True,
                "new_predictions": True,
                "game_results": True
            }

    @property
    def full_name(self) -> str:
        """Get user's full name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

    @property
    def is_locked(self) -> bool:
        """Check if account is currently locked."""
        if not self.account_locked_until:
            return False
        return datetime.utcnow() < self.account_locked_until

    @property
    def is_subscriber(self) -> bool:
        """Check if user has an active subscription."""
        if not self.subscription_expires:
            return False
        return datetime.utcnow() < self.subscription_expires

    @property
    def subscription_status(self) -> str:
        """Get current subscription status."""
        if self.is_admin:
            return "admin"
        elif self.is_subscriber:
            return self.subscription_tier
        else:
            return "free"

    def set_password(self, password: str):
        """Set user password with validation."""
        from app.core.security import security_manager
        # Validate password strength
        validation = security_manager.validate_password_strength(password)
        if not validation["valid"]:
            raise ValueError(f"Password validation failed: {', '.join(validation['errors'])}")
        
        self.hashed_password = security_manager.hash_password(password)
        self.last_password_change = datetime.utcnow()
        self.failed_login_attempts = 0
        self.account_locked_until = None

    def verify_password(self, password: str) -> bool:
        """Verify user password."""
        from app.core.security import security_manager
        return security_manager.verify_password(password, self.hashed_password)

    def generate_api_key(self) -> str:
        """Generate a new API key for the user."""
        from app.core.security import security_manager
        api_key = security_manager.generate_api_key()
        self.api_key_hash = security_manager.hash_api_key(api_key)
        self.api_key_created = datetime.utcnow()
        return api_key

    def verify_api_key(self, api_key: str) -> bool:
        """Verify an API key."""
        from app.core.security import security_manager
        if not self.api_key_hash:
            return False
        
        api_key_hash = security_manager.hash_api_key(api_key)
        if api_key_hash == self.api_key_hash:
            self.api_key_last_used = datetime.utcnow()
            return True
        return False

    def has_role(self, role: str) -> bool:
        """Check if user has a specific role."""
        return role in self.roles

    def has_permission(self, permission: str) -> bool:
        """Check if user has a specific permission."""
        return permission in self.permissions

    def add_role(self, role: str):
        """Add a role to the user and update permissions."""
        from app.core.security import security_manager
        if role not in self.roles:
            self.roles.append(role)
            self._update_permissions()

    def remove_role(self, role: str):
        """Remove a role from the user and update permissions."""
        from app.core.security import security_manager
        if role in self.roles:
            self.roles.remove(role)
            self._update_permissions()

    def set_roles(self, roles: List[str]):
        """Set user roles and update permissions."""
        from app.core.security import security_manager
        self.roles = roles
        self._update_permissions()

    def _update_permissions(self):
        """Update user permissions based on their roles."""
        from app.core.security import security_manager
        permissions = set()
        
        # Add permissions for each role
        for role in self.roles:
            if role in ROLE_PERMISSIONS:
                permissions.update(ROLE_PERMISSIONS[role])
        
        # Admin gets all permissions
        if "admin" in self.roles:
            all_permissions = set()
            for role_perms in ROLE_PERMISSIONS.values():
                all_permissions.update(role_perms)
            permissions = all_permissions
        
        self.permissions = list(permissions)

    def add_permission(self, permission: str):
        """Add a permission to the user."""
        from app.core.security import security_manager
        if permission not in self.permissions:
            self.permissions.append(permission)

    def remove_permission(self, permission: str):
        """Remove a permission from the user."""
        from app.core.security import security_manager
        if permission in self.permissions:
            self.permissions.remove(permission)

    def promote_to_admin(self):
        """Promote user to admin role."""
        from app.core.security import security_manager
        self.is_admin = True
        self.add_role("admin")
        self.subscription_tier = "admin"
        self.subscription_expires = None  # Admin subscription never expires

    def demote_from_admin(self):
        """Demote user from admin role."""
        from app.core.security import security_manager
        self.is_admin = False
        self.remove_role("admin")
        self.subscription_tier = "free"
        self._update_permissions()

    def upgrade_subscription(self, tier: str, duration_days: int = 30):
        """Upgrade user subscription."""
        from app.core.security import security_manager
        valid_tiers = ["basic", "premium", "pro"]
        if tier not in valid_tiers:
            raise ValueError(f"Invalid subscription tier. Must be one of: {valid_tiers}")
        
        self.subscription_tier = tier
        self.subscription_expires = datetime.utcnow() + timedelta(days=duration_days)
        
        # Add subscriber role if not already present
        if "subscriber" not in self.roles:
            self.add_role("subscriber")

    def downgrade_subscription(self):
        """Downgrade user to free tier."""
        from app.core.security import security_manager
        self.subscription_tier = "free"
        self.subscription_expires = None
        self.remove_role("subscriber")

    def lock_account(self, minutes: int = 15):
        """Lock the account for a specified number of minutes."""
        from app.core.security import security_manager
        self.account_locked_until = datetime.utcnow() + timedelta(minutes=minutes)

    def unlock_account(self):
        """Unlock the account."""
        from app.core.security import security_manager
        self.account_locked_until = None
        self.failed_login_attempts = 0

    def record_failed_login(self):
        """Record a failed login attempt."""
        from app.core.security import security_manager
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= 5:
            self.lock_account()

    def record_successful_login(self):
        """Record a successful login."""
        from app.core.security import security_manager
        self.last_login = datetime.utcnow()
        self.failed_login_attempts = 0
        self.account_locked_until = None

    def generate_verification_token(self) -> str:
        """Generate email verification token."""
        from app.core.security import security_manager
        self.email_verification_token = security_manager.generate_secure_token()
        return self.email_verification_token

    def generate_password_reset_token(self) -> str:
        """Generate password reset token."""
        from app.core.security import security_manager
        self.password_reset_token = security_manager.generate_secure_token()
        self.password_reset_expires = datetime.utcnow() + timedelta(hours=24)
        return self.password_reset_token

    def verify_password_reset_token(self, token: str) -> bool:
        """Verify password reset token."""
        from app.core.security import security_manager
        if not self.password_reset_token or not self.password_reset_expires:
            return False
        
        if datetime.utcnow() > self.password_reset_expires:
            return False
        
        return token == self.password_reset_token

    def clear_password_reset_token(self):
        """Clear password reset token."""
        from app.core.security import security_manager
        self.password_reset_token = None
        self.password_reset_expires = None

    def to_dict(self, include_sensitive: bool = False) -> Dict[str, Any]:
        """Convert user to dictionary, optionally including sensitive data."""
        from app.core.security import security_manager
        data = {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "is_admin": self.is_admin,
            "subscription_tier": self.subscription_tier,
            "subscription_status": self.subscription_status,
            "is_subscriber": self.is_subscriber,
            "roles": self.roles,
            "permissions": self.permissions,
            "privacy_settings": self.privacy_settings,
            "notification_settings": self.notification_settings,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_login": self.last_login.isoformat() if self.last_login else None,
        }
        
        if include_sensitive:
            data.update({
                "phone_number": self.phone_number,
                "failed_login_attempts": self.failed_login_attempts,
                "account_locked_until": self.account_locked_until.isoformat() if self.account_locked_until else None,
                "api_key_created": self.api_key_created.isoformat() if self.api_key_created else None,
                "api_key_last_used": self.api_key_last_used.isoformat() if self.api_key_last_used else None,
                "subscription_expires": self.subscription_expires.isoformat() if self.subscription_expires else None,
            })
        
        return data

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}', roles={self.roles})>"


class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    session_token = Column(String, unique=True, nullable=False)
    ip_address = Column(String)
    user_agent = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_activity = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)

    # Relationships
    user = relationship("User", back_populates="sessions")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.expires_at:
            self.expires_at = datetime.utcnow() + timedelta(days=7)

    @property
    def is_expired(self) -> bool:
        """Check if session has expired."""
        return datetime.utcnow() > self.expires_at

    def refresh(self):
        """Refresh session activity."""
        self.last_activity = datetime.utcnow()

    def deactivate(self):
        """Deactivate the session."""
        self.is_active = False


class SecurityLog(Base):
    __tablename__ = "security_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    event_type = Column(String, nullable=False)  # login, logout, password_change, etc.
    ip_address = Column(String)
    user_agent = Column(Text)
    details = Column(JSON, default=dict)
    success = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="security_logs")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.details:
            self.details = {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert security log to dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "event_type": self.event_type,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "details": self.details,
            "success": self.success,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        } 