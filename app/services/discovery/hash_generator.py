import hashlib


class HashGenerator:

    def generate(self, value: str) -> str:

        return hashlib.sha256(

            value.encode()

        ).hexdigest()