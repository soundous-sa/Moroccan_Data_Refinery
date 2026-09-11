from datetime import datetime
from time import sleep

from app.reports.discovery_report import DiscoveryReport
from app.reports.discovery_statistics import DiscoveryStatistics
from app.reports.report_builder import ReportBuilder

start = datetime.now()

sleep(2)

stats = DiscoveryStatistics(

    pages_visited=1,

    links_found=248,

    publications_found=43,

    duplicates_removed=12,

    pdf_count=21,

    excel_count=10,

    csv_count=4,

    html_count=8

)

report = DiscoveryReport(

    source="HCP",

    started_at=start,

    finished_at=datetime.now(),

    success=True,

    statistics=stats,

    message="Exploration terminée avec succès."

)

builder = ReportBuilder()

print(

    builder.build(report)

)