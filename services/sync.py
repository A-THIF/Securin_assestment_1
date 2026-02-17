import requests
from sqlalchemy.orm import Session
from models.model import CVE
from datetime import datetime

BASE_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"

def sync_cves(db: Session):
    start_index = 0
    results_per_page = 2000

    while True:
        params = {
            "startIndex": start_index,
            "resultsPerPage": results_per_page
        }

        response = requests.get(BASE_URL, params=params)
        data = response.json()

        vulnerabilities = data.get("vulnerabilities", [])
        total_results = data.get("totalResults", 0)

        if not vulnerabilities:
            break

        for item in vulnerabilities:
            cve_data = item["cve"]

            cve_id = cve_data["id"]
            description = cve_data["descriptions"][0]["value"]
            published = datetime.fromisoformat(cve_data["published"].replace("Z", "+00:00"))
            last_modified = datetime.fromisoformat(cve_data["lastModified"].replace("Z", "+00:00"))

            metrics = cve_data.get("metrics", {})
            base_score = None

            if "cvssMetricV31" in metrics:
                base_score = metrics["cvssMetricV31"][0]["cvssData"]["baseScore"]

            db_cve = CVE(
                cve_id=cve_id,
                description=description,
                published=published,
                last_modified=last_modified,
                base_score=base_score
            )

            db.merge(db_cve)

        db.commit()

        start_index += results_per_page

        # Stop if we've reached the total number of CVEs
        if start_index >= total_results:
            break
