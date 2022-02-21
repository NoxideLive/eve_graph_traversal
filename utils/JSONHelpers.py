import io

from rest_framework.parsers import JSONParser


class JSONHelpers:
    @staticmethod
    def parse(s: bytes):
        stream = io.BytesIO(s)
        data = JSONParser().parse(stream)
        return data
