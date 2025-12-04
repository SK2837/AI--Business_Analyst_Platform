"""
Alert model for proactive monitoring.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB, TIMESTAMP
from sqlalchemy.orm import relationship
import enum

from app.models.database import Base


class AlertType(str, enum.Enum):
    """Alert type enumeration."""
    THRESHOLD = "threshold"
    TREND = "trend"
    ANOMALY = "anomaly"
    COMPARATIVE = "comparative"


class Alert(Base):
    """
    Alert model for proactive data monitoring.
    
    Defines alert rules that monitor data sources for specific conditions
    and trigger notifications when conditions are met.
    
    Attributes:
        id: Unique alert identifier
        user_id: User who created the alert
        name: Alert name
        description: Optional description
        alert_type: Type of alert (threshold, trend, anomaly, comparative)
        condition_config: Alert condition details (metric, operator, threshold, etc.)
        data_source_id: Data source to monitor
        check_frequency: Cron expression for check schedule
        notification_channels: Array of notification targets (email, slack, etc.)
        is_active: Whether this alert is currently active
        last_checked_at: Last time alert was evaluated
        last_triggered_at: Last time alert condition was met
        created_at: Alert creation timestamp
        updated_at: Last modification timestamp
    """
    __tablename__ = "alerts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    alert_type = Column(SQLEnum(AlertType), nullable=False)
    condition_config = Column(JSONB, nullable=False)
    data_source_id = Column(UUID(as_uuid=True), ForeignKey("data_sources.id"), nullable=False)
    check_frequency = Column(String(100), nullable=False, index=True)
    notification_channels = Column(JSONB, nullable=False, default=list)
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    last_checked_at = Column(TIMESTAMP, nullable=True)
    last_triggered_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="alerts")
    data_source = relationship("DataSource", back_populates="alerts")
    executions = relationship("AlertExecution", back_populates="alert", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Alert(id={self.id}, name={self.name}, type={self.alert_type})>"
