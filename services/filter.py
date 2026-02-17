from sqlalchemy.orm import Session
from models.model import CVE
from datetime import datetime, timedelta
from typing import Optional, List

def get_cves(
    db: Session,
    cve_id: Optional[str] = None,
    year: Optional[int] = None,
    min_score: Optional[float] = None,
    last_n_days: Optional[int] = None,
    skip: int = 0,
    limit: int = 10,
    sort_by: str = "published",
    order: str = "desc"
) -> List[CVE]:

    query = db.query(CVE)

    # Filters
    if cve_id:
        query = query.filter(CVE.cve_id == cve_id)
    if year:
        query = query.filter(CVE.published.like(f"{year}%"))
    if min_score:
        query = query.filter(CVE.base_score >= min_score)
    if last_n_days:
        cutoff = datetime.utcnow() - timedelta(days=last_n_days)
        query = query.filter(CVE.last_modified >= cutoff)

    # Sorting
    if sort_by == "published":
        query = query.order_by(CVE.published.desc() if order=="desc" else CVE.published.asc())
    elif sort_by == "last_modified":
        query = query.order_by(CVE.last_modified.desc() if order=="desc" else CVE.last_modified.asc())
    elif sort_by == "cve_id":
        query = query.order_by(CVE.cve_id.desc() if order=="desc" else CVE.cve_id.asc())
    elif sort_by == "base_score":
        query = query.order_by(CVE.base_score.desc() if order=="desc" else CVE.base_score.asc())

    total_count = query.count()  # total records matching filters

    # Pagination
    if limit:
        query = query.offset(skip).limit(limit)

    results = query.all()
    return results, total_count
