from nanome._internal._util._serializers import _TypeSerializer

class _GetControllerTransforms(_TypeSerializer):
    def __init__(self):
        pass

    def version(self):
        return 0

    def name(self):
        return "GetControllerTransforms"

    def serialize(self, version, value, data):
        pass

    def deserialize(self, version, data):
        return None