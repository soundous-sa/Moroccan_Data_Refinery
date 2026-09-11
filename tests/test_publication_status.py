from app.domain.publication_status import PublicationStatus
from app.services.persistence.publication_status_service import (
    PublicationStatusService
)


print()
print("=" * 60)
print("TEST TRANSITIONS")
print("=" * 60)


tests = [

    (
        PublicationStatus.DISCOVERED,
        PublicationStatus.DOWNLOADED
    ),

    (
        PublicationStatus.DOWNLOADED,
        PublicationStatus.PARSED
    ),

    (
        PublicationStatus.PARSED,
        PublicationStatus.PROCESSED
    ),

    (
        PublicationStatus.DOWNLOADED,
        PublicationStatus.FAILED
    ),

    (
        PublicationStatus.FAILED,
        PublicationStatus.DOWNLOADED
    )
]


for current, new in tests:

    result = PublicationStatusService.can_transition(
        current,
        new
    )

    print(
        f"{current.value} "
        f"-> "
        f"{new.value} "
        f": "
        f"{result}"
    )


print("=" * 60)
print()

try:

    PublicationStatusService.validate_transition(

        PublicationStatus.PROCESSED,

        PublicationStatus.DISCOVERED

    )

except ValueError as error:

    print(
        "Transition refusée :",
        error
    )