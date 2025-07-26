from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Dict, Any, Optional
import json
from app.core.database import Base

class Content(Base):
    __tablename__ = "content"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Content identification
    title = Column(String, index=True)
    slug = Column(String, unique=True, index=True)
    content_type = Column(String, index=True)  # "article", "analysis", "prediction", "brownlow", "news"
    
    # Content details
    summary = Column(Text)
    content_body = Column(Text)  # Main content
    excerpt = Column(Text)  # Short preview
    
    # SEO and metadata
    meta_title = Column(String)
    meta_description = Column(Text)
    keywords = Column(Text)  # Comma-separated keywords
    canonical_url = Column(String)
    
    # AI generation details
    ai_model = Column(String, default="gemini-1.5-flash")
    ai_prompt = Column(Text)  # The prompt used to generate content
    ai_context = Column(Text)  # Context data provided to AI
    generation_parameters = Column(JSON)  # Temperature, max tokens, etc.
    
    # Content relationships
    related_game_id = Column(Integer, ForeignKey("games.id"), index=True)
    related_team_id = Column(Integer, ForeignKey("teams.id"), index=True)
    related_prediction_id = Column(Integer, ForeignKey("predictions.id"), index=True)
    author_id = Column(Integer, ForeignKey("users.id"), index=True)
    
    # Content status and publishing
    status = Column(String, default="draft")  # "draft", "published", "archived", "scheduled"
    is_featured = Column(Boolean, default=False)
    is_premium = Column(Boolean, default=False)  # Premium content for subscribers
    
    # Publishing details
    published_at = Column(DateTime, index=True)
    scheduled_at = Column(DateTime, index=True)
    expires_at = Column(DateTime, index=True)
    
    # Performance metrics
    view_count = Column(Integer, default=0)
    share_count = Column(Integer, default=0)
    engagement_score = Column(Float, default=0.0)
    
    # Content structure
    tags = Column(JSON, default=list)  # ["AFL", "betting", "predictions", "analysis"]
    categories = Column(JSON, default=list)  # ["game-analysis", "team-preview", "betting-tips"]
    
    # Version control
    version = Column(Integer, default=1)
    parent_content_id = Column(Integer, ForeignKey("content.id"), index=True)
    
    # Audit fields
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(Integer, ForeignKey("users.id"), index=True)
    updated_by = Column(Integer, ForeignKey("users.id"), index=True)
    
    # Relationships
    related_game = relationship("Game")
    related_team = relationship("Team")
    related_prediction = relationship("Prediction")
    author = relationship("User", foreign_keys=[author_id])
    creator = relationship("User", foreign_keys=[created_by])
    updater = relationship("User", foreign_keys=[updated_by])
    parent_content = relationship("Content", remote_side=[id])
    content_versions = relationship("Content", back_populates="parent_content")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.tags:
            self.tags = []
        if not self.categories:
            self.categories = []
        if not self.generation_parameters:
            self.generation_parameters = {
                "temperature": 0.7,
                "max_tokens": 1000,
                "top_p": 0.9
            }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert content to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "slug": self.slug,
            "content_type": self.content_type,
            "summary": self.summary,
            "excerpt": self.excerpt,
            "status": self.status,
            "is_featured": self.is_featured,
            "is_premium": self.is_premium,
            "published_at": self.published_at.isoformat() if self.published_at else None,
            "view_count": self.view_count,
            "engagement_score": self.engagement_score,
            "tags": self.tags,
            "categories": self.categories,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
    def increment_view(self):
        """Increment view count."""
        self.view_count += 1
    
    def update_engagement_score(self, score: float):
        """Update engagement score."""
        self.engagement_score = score
    
    def publish(self):
        """Publish the content."""
        self.status = "published"
        self.published_at = datetime.utcnow()
    
    def archive(self):
        """Archive the content."""
        self.status = "archived"
    
    def schedule(self, publish_date: datetime):
        """Schedule content for publishing."""
        self.status = "scheduled"
        self.scheduled_at = publish_date


class ContentVersion(Base):
    __tablename__ = "content_versions"
    
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("content.id"), index=True)
    version_number = Column(Integer, index=True)
    
    # Version content
    title = Column(String)
    content_body = Column(Text)
    summary = Column(Text)
    excerpt = Column(Text)
    
    # Version metadata
    change_reason = Column(String)  # "AI regeneration", "manual edit", "correction"
    ai_model = Column(String)
    ai_prompt = Column(Text)
    generation_parameters = Column(JSON)
    
    # Version control
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(Integer, ForeignKey("users.id"), index=True)
    
    # Relationships
    content = relationship("Content")
    creator = relationship("User")


class ContentAnalytics(Base):
    __tablename__ = "content_analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("content.id"), index=True)
    
    # Analytics period
    date = Column(DateTime, index=True)
    period_type = Column(String)  # "daily", "weekly", "monthly"
    
    # Performance metrics
    views = Column(Integer, default=0)
    unique_views = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    engagement_time = Column(Float, default=0.0)  # Average time spent in seconds
    
    # User behavior
    bounce_rate = Column(Float, default=0.0)
    scroll_depth = Column(Float, default=0.0)  # Average scroll depth percentage
    
    # Conversion metrics
    click_through_rate = Column(Float, default=0.0)
    conversion_rate = Column(Float, default=0.0)
    
    # SEO metrics
    search_impressions = Column(Integer, default=0)
    search_clicks = Column(Integer, default=0)
    search_position = Column(Float, default=0.0)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    content = relationship("Content")


class ContentTemplate(Base):
    __tablename__ = "content_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Template details
    name = Column(String, unique=True, index=True)
    description = Column(Text)
    content_type = Column(String, index=True)
    
    # Template structure
    prompt_template = Column(Text)  # AI prompt template
    content_structure = Column(JSON)  # Expected content structure
    seo_template = Column(JSON)  # SEO metadata template
    
    # Template settings
    is_active = Column(Boolean, default=True)
    priority = Column(Integer, default=0)  # Higher priority templates used first
    
    # Usage tracking
    usage_count = Column(Integer, default=0)
    success_rate = Column(Float, default=0.0)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(Integer, ForeignKey("users.id"), index=True)
    
    # Relationships
    creator = relationship("User")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.content_structure:
            self.content_structure = {
                "sections": ["introduction", "analysis", "conclusion"],
                "required_fields": ["title", "summary", "content_body"],
                "optional_fields": ["excerpt", "meta_description"]
            }
        if not self.seo_template:
            self.seo_template = {
                "meta_title_template": "{title} - FootyBets.ai",
                "meta_description_template": "{summary}",
                "keyword_suggestions": ["AFL", "betting", "predictions"]
            }
    
    def get_prompt_with_context(self, context: Dict[str, Any]) -> str:
        """Get the prompt template filled with context data."""
        prompt = self.prompt_template
        for key, value in context.items():
            prompt = prompt.replace(f"{{{key}}}", str(value))
        return prompt
    
    def increment_usage(self):
        """Increment usage count."""
        self.usage_count += 1
    
    def update_success_rate(self, success_rate: float):
        """Update success rate."""
        self.success_rate = success_rate 