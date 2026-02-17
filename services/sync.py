import requests
import json 
from sqlalchemy.orm import Session
from models.model import CVE
from datetime import datetime

BASE_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"

# Track progress globally (simple version)
sync_progress = {
    "total": 0,
    "fetched": 0,
    "completed": False
}

def sync_cves_batch(db: Session, batch_size: int = 50):
    start_index = sync_progress.get("fetched", 0)

    response = requests.get(BASE_URL, params={
        "startIndex": start_index,
        "resultsPerPage": batch_size
    })
    data = response.json()

    vulnerabilities = data.get("vulnerabilities", [])
    total_results = data.get("totalResults", 0)
    sync_progress["total"] = total_results

    if not vulnerabilities:
        sync_progress["completed"] = True
        return

    for item in vulnerabilities:
        cve_data = item["cve"]

        cve_id = cve_data["id"]
        description = cve_data["descriptions"][0]["value"]
        published = datetime.fromisoformat(cve_data["published"].replace("Z", "+00:00"))
        last_modified = datetime.fromisoformat(cve_data["lastModified"].replace("Z", "+00:00"))

        metrics = cve_data.get("metrics", {})
        configurations = cve_data.get("configurations", {})

        base_score = None
        if "cvssMetricV31" in metrics:
            base_score = metrics["cvssMetricV31"][0]["cvssData"]["baseScore"]

        identifier = cve_data.get("sourceIdentifier")
        status = cve_data.get("vulnStatus")

        db_cve = CVE(
            cve_id=cve_id,
            description=description,
            published=published,
            last_modified=last_modified,
            base_score=base_score,
            identifier=identifier,
            status=status,
            metrics=json.dumps(metrics),  # Store as JSON string
            configurations=json.dumps(configurations)  # Store as JSON string
        )

        db.merge(db_cve)

    db.commit()
    sync_progress["fetched"] += len(vulnerabilities)

    if sync_progress["fetched"] >= total_results:
        sync_progress["completed"] = True
