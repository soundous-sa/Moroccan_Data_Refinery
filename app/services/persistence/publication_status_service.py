from app.domain.publication_status import PublicationStatus


class PublicationStatusService:

    # ==================================================
    # TRANSITIONS AUTORISÉES
    # ==================================================

    TRANSITIONS = {

        PublicationStatus.DISCOVERED: [

            PublicationStatus.DOWNLOADED,

            PublicationStatus.FAILED

        ],

        PublicationStatus.DOWNLOADED: [

            PublicationStatus.PARSED,

            PublicationStatus.FAILED

        ],

        PublicationStatus.PARSED: [

            PublicationStatus.PROCESSED,

            PublicationStatus.FAILED

        ],

        PublicationStatus.PROCESSED: [],

        PublicationStatus.FAILED: [

            PublicationStatus.DOWNLOADED

        ]
    }

    # ==================================================
    # VALIDATION
    # ==================================================

    @classmethod
    def can_transition(
        cls,
        current_status,
        new_status
    ):

        allowed = cls.TRANSITIONS.get(
            current_status,
            []
        )

        return new_status in allowed

    # ==================================================
    # VALIDATION AVEC EXCEPTION
    # ==================================================

    @classmethod
    def validate_transition(
        cls,
        current_status,
        new_status
    ):

        if not cls.can_transition(
            current_status,
            new_status
        ):

            raise ValueError(

                f"Transition interdite : "
                f"{current_status.value} "
                f"-> "
                f"{new_status.value}"

            )

        return True