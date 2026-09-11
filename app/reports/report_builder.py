class ReportBuilder:

    def build(self, report):

        duration = (

            report.finished_at -

            report.started_at

        ).total_seconds()

        stats = report.statistics

        return f"""
============================================================
DISCOVERY REPORT
============================================================

Source               : {report.source}

Début                : {report.started_at}

Fin                  : {report.finished_at}

Durée                : {duration:.2f} sec

------------------------------------------------------------

Pages analysées      : {stats.pages_visited}

Liens trouvés        : {stats.links_found}

Publications valides : {stats.publications_found}

Doublons supprimés   : {stats.duplicates_removed}

------------------------------------------------------------

PDF                  : {stats.pdf_count}

EXCEL                : {stats.excel_count}

CSV                  : {stats.csv_count}

HTML                 : {stats.html_count}

------------------------------------------------------------

Succès               : {report.success}

Message              : {report.message}

============================================================
"""