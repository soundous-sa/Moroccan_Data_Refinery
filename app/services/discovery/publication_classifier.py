from app.services.discovery.classification_result import ClassificationResult

from app.services.discovery.classification_rules import *

from app.services.discovery.keywords import PUBLICATION_KEYWORDS


class PublicationClassifier:

    def classify(self, publication):

        score = 0

        reason = []

        url = publication.url.lower()

        title = publication.title.lower()

        # -------- Format --------

        for extension, value in FILE_SCORES.items():

            if url.endswith(extension):

                score += value

                reason.append(extension)

        # -------- Mots clés --------

        for keyword in PUBLICATION_KEYWORDS:

            if keyword in title:

                score += 10

                reason.append(keyword)

        accepted = score >= MINIMUM_SCORE

        return ClassificationResult(

            score=score,

            accepted=accepted,

            reason=", ".join(reason)

        )