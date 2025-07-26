from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel

from app.core.database import get_db
from app.core.security import get_current_user, require_permission
from app.models.user import User
from app.models.content import Content, ContentTemplate
from app.services.content_service import ContentService

router = APIRouter()
content_service = ContentService()

# Pydantic models
class ContentCreate(BaseModel):
    title: str
    content_type: str
    template_name: str
    context: Dict[str, Any]
    is_premium: bool = False
    is_featured: bool = False
    tags: List[str] = []
    categories: List[str] = []

class ContentUpdate(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None
    content_body: Optional[str] = None
    excerpt: Optional[str] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    keywords: Optional[str] = None
    is_premium: Optional[bool] = None
    is_featured: Optional[bool] = None
    tags: Optional[List[str]] = None
    categories: Optional[List[str]] = None
    change_reason: Optional[str] = None

class ContentResponse(BaseModel):
    id: int
    title: str
    slug: str
    content_type: str
    summary: Optional[str] = None
    excerpt: Optional[str] = None
    content_body: Optional[str] = None
    status: str
    is_featured: bool
    is_premium: bool
    view_count: int
    engagement_score: float
    tags: List[str]
    categories: List[str]
    published_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ContentListResponse(BaseModel):
    content: List[ContentResponse]
    total: int
    page: int
    per_page: int
    total_pages: int

# Content generation endpoints
@router.post("/generate", response_model=ContentResponse)
async def generate_content(
    content_data: ContentCreate,
    current_user: User = Depends(require_permission("write_predictions")),
    db: Session = Depends(get_db)
):
    """Generate new content using AI templates."""
    try:
        content = content_service.generate_content(
            db=db,
            template_name=content_data.template_name,
            context=content_data.context,
            user_id=current_user.id
        )
        
        if not content:
            raise HTTPException(status_code=500, detail="Failed to generate content")
        
        # Update additional fields
        if content_data.is_premium:
            content.is_premium = content_data.is_premium
        if content_data.is_featured:
            content.is_featured = content_data.is_featured
        if content_data.tags:
            content.tags = content_data.tags
        if content_data.categories:
            content.categories = content_data.categories
        
        db.commit()
        db.refresh(content)
        
        return content
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating content: {str(e)}")

@router.post("/generate/game-analysis/{game_id}", response_model=ContentResponse)
async def generate_game_analysis(
    game_id: int,
    current_user: User = Depends(require_permission("write_predictions")),
    db: Session = Depends(get_db)
):
    """Generate analysis for a specific game."""
    try:
        content = content_service.generate_game_analysis(
            db=db,
            game_id=game_id,
            user_id=current_user.id
        )
        
        if not content:
            raise HTTPException(status_code=404, detail="Game not found or failed to generate analysis")
        
        return content
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating game analysis: {str(e)}")

@router.post("/generate/team-preview/{team_id}", response_model=ContentResponse)
async def generate_team_preview(
    team_id: int,
    season: int = Query(2024, description="Season for preview"),
    current_user: User = Depends(require_permission("write_predictions")),
    db: Session = Depends(get_db)
):
    """Generate team preview for a specific season."""
    try:
        content = content_service.generate_team_preview(
            db=db,
            team_id=team_id,
            season=season,
            user_id=current_user.id
        )
        
        if not content:
            raise HTTPException(status_code=404, detail="Team not found or failed to generate preview")
        
        return content
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating team preview: {str(e)}")

# Content management endpoints
@router.get("/", response_model=ContentListResponse)
async def get_content(
    content_type: Optional[str] = Query(None, description="Filter by content type"),
    status: Optional[str] = Query("published", description="Filter by status"),
    is_featured: Optional[bool] = Query(None, description="Filter featured content"),
    is_premium: Optional[bool] = Query(None, description="Filter premium content"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=100, description="Items per page"),
    current_user: User = Depends(require_permission("read_predictions")),
    db: Session = Depends(get_db)
):
    """Get content with filtering and pagination."""
    try:
        # Build query
        query = db.query(Content)
        
        # Apply filters
        if content_type:
            query = query.filter(Content.content_type == content_type)
        if status:
            query = query.filter(Content.status == status)
        if is_featured is not None:
            query = query.filter(Content.is_featured == is_featured)
        if is_premium is not None:
            query = query.filter(Content.is_premium == is_premium)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        offset = (page - 1) * per_page
        content_list = query.order_by(Content.created_at.desc()).offset(offset).limit(per_page).all()
        
        # Calculate pagination info
        total_pages = (total + per_page - 1) // per_page
        
        return ContentListResponse(
            content=content_list,
            total=total,
            page=page,
            per_page=per_page,
            total_pages=total_pages
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving content: {str(e)}")

@router.get("/featured", response_model=List[ContentResponse])
async def get_featured_content(
    limit: int = Query(5, ge=1, le=20, description="Number of featured items"),
    current_user: User = Depends(require_permission("read_predictions")),
    db: Session = Depends(get_db)
):
    """Get featured content."""
    try:
        content = content_service.get_featured_content(db=db, limit=limit)
        return content
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving featured content: {str(e)}")

@router.get("/{content_id}", response_model=ContentResponse)
async def get_content_by_id(
    content_id: int,
    current_user: User = Depends(require_permission("read_predictions")),
    db: Session = Depends(get_db)
):
    """Get specific content by ID."""
    try:
        content = db.query(Content).filter(Content.id == content_id).first()
        if not content:
            raise HTTPException(status_code=404, detail="Content not found")
        
        # Track view
        content_service.track_content_view(db=db, content_id=content_id)
        
        return content
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving content: {str(e)}")

@router.get("/slug/{slug}", response_model=ContentResponse)
async def get_content_by_slug(
    slug: str,
    current_user: User = Depends(require_permission("read_predictions")),
    db: Session = Depends(get_db)
):
    """Get content by slug."""
    try:
        content = db.query(Content).filter(Content.slug == slug).first()
        if not content:
            raise HTTPException(status_code=404, detail="Content not found")
        
        # Track view
        content_service.track_content_view(db=db, content_id=content.id)
        
        return content
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving content: {str(e)}")

@router.put("/{content_id}", response_model=ContentResponse)
async def update_content(
    content_id: int,
    content_update: ContentUpdate,
    current_user: User = Depends(require_permission("write_predictions")),
    db: Session = Depends(get_db)
):
    """Update content."""
    try:
        updates = content_update.dict(exclude_unset=True)
        content = content_service.update_content(
            db=db,
            content_id=content_id,
            updates=updates,
            user_id=current_user.id
        )
        
        if not content:
            raise HTTPException(status_code=404, detail="Content not found")
        
        return content
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating content: {str(e)}")

@router.post("/{content_id}/publish")
async def publish_content(
    content_id: int,
    current_user: User = Depends(require_permission("write_predictions")),
    db: Session = Depends(get_db)
):
    """Publish content."""
    try:
        success = content_service.publish_content(
            db=db,
            content_id=content_id,
            user_id=current_user.id
        )
        
        if not success:
            raise HTTPException(status_code=404, detail="Content not found")
        
        return {"message": "Content published successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error publishing content: {str(e)}")

@router.post("/{content_id}/archive")
async def archive_content(
    content_id: int,
    current_user: User = Depends(require_permission("write_predictions")),
    db: Session = Depends(get_db)
):
    """Archive content."""
    try:
        content = db.query(Content).filter(Content.id == content_id).first()
        if not content:
            raise HTTPException(status_code=404, detail="Content not found")
        
        content.archive()
        content.updated_by = current_user.id
        content.updated_at = datetime.utcnow()
        
        db.commit()
        
        return {"message": "Content archived successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error archiving content: {str(e)}")

@router.delete("/{content_id}")
async def delete_content(
    content_id: int,
    current_user: User = Depends(require_permission("write_predictions")),
    db: Session = Depends(get_db)
):
    """Delete content (soft delete by archiving)."""
    try:
        content = db.query(Content).filter(Content.id == content_id).first()
        if not content:
            raise HTTPException(status_code=404, detail="Content not found")
        
        # Soft delete by archiving
        content.archive()
        content.updated_by = current_user.id
        content.updated_at = datetime.utcnow()
        
        db.commit()
        
        return {"message": "Content deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting content: {str(e)}")

# Template management endpoints
@router.get("/templates/", response_model=List[Dict[str, Any]])
async def get_content_templates(
    current_user: User = Depends(require_permission("read_predictions")),
    db: Session = Depends(get_db)
):
    """Get available content templates."""
    try:
        templates = db.query(ContentTemplate).filter(ContentTemplate.is_active == True).all()
        return [
            {
                "id": template.id,
                "name": template.name,
                "description": template.description,
                "content_type": template.content_type,
                "usage_count": template.usage_count,
                "success_rate": template.success_rate
            }
            for template in templates
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving templates: {str(e)}")

@router.get("/templates/{template_id}", response_model=Dict[str, Any])
async def get_content_template(
    template_id: int,
    current_user: User = Depends(require_permission("read_predictions")),
    db: Session = Depends(get_db)
):
    """Get specific content template."""
    try:
        template = db.query(ContentTemplate).filter(ContentTemplate.id == template_id).first()
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")
        
        return {
            "id": template.id,
            "name": template.name,
            "description": template.description,
            "content_type": template.content_type,
            "prompt_template": template.prompt_template,
            "content_structure": template.content_structure,
            "seo_template": template.seo_template,
            "usage_count": template.usage_count,
            "success_rate": template.success_rate
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving template: {str(e)}")

# Analytics endpoints
@router.get("/{content_id}/analytics", response_model=Dict[str, Any])
async def get_content_analytics(
    content_id: int,
    period: str = Query("daily", description="Analytics period"),
    current_user: User = Depends(require_permission("read_analytics")),
    db: Session = Depends(get_db)
):
    """Get content analytics."""
    try:
        content = db.query(Content).filter(Content.id == content_id).first()
        if not content:
            raise HTTPException(status_code=404, detail="Content not found")
        
        # Get analytics data
        from app.models.content import ContentAnalytics
        
        analytics = db.query(ContentAnalytics).filter(
            ContentAnalytics.content_id == content_id
        ).order_by(ContentAnalytics.date.desc()).limit(30).all()
        
        return {
            "content_id": content_id,
            "view_count": content.view_count,
            "engagement_score": content.engagement_score,
            "analytics": [
                {
                    "date": a.date.isoformat(),
                    "views": a.views,
                    "unique_views": a.unique_views,
                    "shares": a.shares,
                    "engagement_time": a.engagement_time
                }
                for a in analytics
            ]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving analytics: {str(e)}") 