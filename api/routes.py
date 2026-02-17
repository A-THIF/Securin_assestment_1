from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.model import CVE
from services.sync import sync_cves_batch, sync_progress  # import your batch function
from services.filter import get_cves
from typing import Optional

router = APIRouter()


# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Trigger background CVE sync
@router.post("/sync-cves")
def trigger_sync(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # Run sync_cves_batch repeatedly until completed in the background
    def sync_all_batches():
        while not sync_progress.get("completed", False):
            sync_cves_batch(db, batch_size=50)  # fetch 50 CVEs per batch

    background_tasks.add_task(sync_all_batches)
    return {"message": "CVE sync started in background."}


# Check progress
@router.get("/sync-progress")
def get_sync_progress_endpoint():
    return {
        "total": sync_progress.get("total", 0),
        "fetched": sync_progress.get("fetched", 0),
        "completed": sync_progress.get("completed", False)
    }

# CVE list route
@router.get("/cves")
def read_cves(
    skip: int = 0,
    limit: int = 10,
    sort_by: str = "published",
    order: str = "desc",
    cve_id: Optional[str] = None,
    year: Optional[int] = None,
    min_score: Optional[float] = None,
    last_n_days: Optional[int] = None,
    db: Session = Depends(get_db)
):
    results, total_count = get_cves(
        db,
        cve_id=cve_id,
        year=year,
        min_score=min_score,
        last_n_days=last_n_days,
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        order=order
    )

    # Only return the fields needed for the table
    data = [
        {
            "cve_id": c.cve_id,
            "identifier": c.identifier,
            "published": c.published,
            "last_modified": c.last_modified,
            "status": c.status
        }
        for c in results
    ]

    return {
        "data": [cve.to_dict() for cve in results],
        "skip": skip,
        "limit": limit,
        "count": total_count
    }

# Single CVE route
@router.get("/cves/{cve_id}")
def get_single_cve(cve_id: str, db: Session = Depends(get_db)):
    cve = db.query(CVE).filter(CVE.cve_id == cve_id).first()
    if cve:
        return cve.to_dict()
    return {"error": "CVE not found"}
