from uuid import uuid4


def create_id(prefix=''):
    return prefix + uuid4().hex
