from sqlalchemy import Column, String, Float, DateTime, Text
from core.database import Base

class CVE(Base):
    __tablename__ = "cves"

    cve_id = Column(String, primary_key=True, index=True)
    description = Column(String)
    published = Column(DateTime)
    last_modified = Column(DateTime)
    base_score = Column(Float)
    identifier = Column(String, nullable=True)  # email or owner identifier
    status = Column(String, nullable=True)      # e.g., 'Vulnerable', 'Rejected', etc.
    metrics = Column(Text, nullable=True)       # store JSON as string
    configurations = Column(Text, nullable=True)  # store CPE configs as JSON string



    # Add this helper to convert model instance to dictionary
    def to_dict(self):
        return {
        "cve_id": self.cve_id,
        "description": self.description,
        "published": self.published.isoformat(),
        "last_modified": self.last_modified.isoformat(),
        "status": self.status,
        "identifier": self.identifier,
        "metrics": self.metrics,             # Make sure you store CVSS metrics in DB or fetch dynamically
        "configurations": self.configurations  # Store as JSON in DB if needed
    }

