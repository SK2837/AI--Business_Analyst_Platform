"""
ReportVersion model for report version history.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB, TIMESTAMP
from sqlalchemy.orm import relationship

from app.models.database import Base


class ReportVersion(Base):
    """
    ReportVersion model for tracking report changes over time.
    
    Enables versioning of reports to track modifications and
    allow users to view historical versions.
    
    Attributes:
        id: Unique version identifier
        report_id: Parent report
        version_number: Sequential version number
        content: Snapshot of report content at this version
        created_at: Version creation timestamp
        created_by: User who created this version
    """
    __tablename__ = "report_versions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    report_id = Column(UUID(as_uuid=True), ForeignKey("reports.id"), nullable=False, index=True)
    version_number = Column(Integer, nullable=False)
    content = Column(JSONB, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Relationships
    report = relationship("Report", back_populates="versions")
    creator = relationship("User")
    
    def __repr__(self):
        return f"<ReportVersion(id={self.id}, report_id={self.report_id}, version={self.version_number})>"
