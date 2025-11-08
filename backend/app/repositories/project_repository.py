"""
Project repository for project data operations
"""
from sqlalchemy.orm import Session
from typing import Optional, List

from app.models.models import Project, User
from app.repositories.base import BaseRepository


class ProjectRepository(BaseRepository):
    """Repository for project operations"""
    
    def __init__(self, db: Session):
        super().__init__(db, Project)
    
    def get_by_owner(self, owner_id: int, skip: int = 0, limit: int = 100) -> List[Project]:
        """Get projects owned by a user"""
        return self.db.query(Project).filter(
            Project.owner_id == owner_id
        ).offset(skip).limit(limit).all()
    
    def get_user_projects(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Project]:
        """Get projects where user is owner or member"""
        from sqlalchemy import or_
        return self.db.query(Project).filter(
            or_(
                Project.owner_id == user_id,
                Project.members.any(User.id == user_id)
            )
        ).offset(skip).limit(limit).all()
    
    def get_by_member(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Project]:
        """Get projects where user is a member"""
        return self.db.query(Project).join(
            Project.members
        ).filter(User.id == user_id).offset(skip).limit(limit).all()
    
    def add_member(self, project_id: int, user_id: int) -> bool:
        """Add user as member to project"""
        project = self.get_by_id(project_id)
        if not project:
            return False
        
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        
        if user not in project.members:
            project.members.append(user)
            self.db.commit()
        
        return True
    
    def remove_member(self, project_id: int, user_id: int) -> bool:
        """Remove user as member from project"""
        project = self.get_by_id(project_id)
        if not project:
            return False
        
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        
        if user in project.members:
            project.members.remove(user)
            self.db.commit()
        
        return True
    
    def is_member(self, project_id: int, user_id: int) -> bool:
        """Check if user is a member of the project (includes owner)"""
        project = self.get_by_id(project_id)
        if not project:
            return False
        
        # Owner is automatically a member
        if project.owner_id == user_id:
            return True
        
        return any(member.id == user_id for member in project.members)
    
    def is_owner(self, project_id: int, user_id: int) -> bool:
        """Check if user is the owner of the project"""
        project = self.get_by_id(project_id)
        if not project:
            return False
        
        return project.owner_id == user_id
