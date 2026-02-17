from sqlalchemy import Column, String, Float, DateTime
from core.database import Base

class CVE(Base):
    __tablename__ = "cves"

    cve_id = Column(String, primary_key=True, index=True)
    description = Column(String)
    published = Column(DateTime)
    last_modified = Column(DateTime)
    base_score = Column(Float)

    # Add this helper to convert model instance to dictionary
    def to_dict(self):
        return {
            "cve_id": self.cve_id,
            "published": self.published.isoformat() if self.published else None,
            "last_modified": self.last_modified.isoformat() if self.last_modified else None,
            "base_score": self.base_score,
            "description": self.description
        }
