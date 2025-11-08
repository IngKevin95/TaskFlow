"""
Base repository class for all repositories
"""
from sqlalchemy.orm import Session
from typing import TypeVar, Generic, List, Optional

T = TypeVar('T')


class BaseRepository(Generic[T]):
    """Base repository for common CRUD operations"""
    
    def __init__(self, db: Session, model: type):
        self.db = db
        self.model = model
    
    def create(self, **kwargs) -> T:
        """Create a new entity"""
        entity = self.model(**kwargs)
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity
    
    def create_from_obj(self, obj: T) -> T:
        """Create a new entity from an object"""
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj
    
    def get_by_id(self, entity_id: int) -> Optional[T]:
        """Get entity by ID"""
        return self.db.query(self.model).filter(self.model.id == entity_id).first()
    
    def get(self, entity_id: int) -> Optional[T]:
        """Get entity by ID (alias for get_by_id)"""
        return self.get_by_id(entity_id)
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Get all entities with pagination"""
        return self.db.query(self.model).offset(skip).limit(limit).all()
    
    def update(self, entity_id: int, **kwargs) -> Optional[T]:
        """Update an entity"""
        entity = self.get_by_id(entity_id)
        if not entity:
            return None
        
        for key, value in kwargs.items():
            if hasattr(entity, key):
                setattr(entity, key, value)
        
        self.db.commit()
        self.db.refresh(entity)
        return entity
    
    def delete(self, entity_id: int) -> bool:
        """Delete an entity"""
        entity = self.get_by_id(entity_id)
        if not entity:
            return False
        
        self.db.delete(entity)
        self.db.commit()
        return True
