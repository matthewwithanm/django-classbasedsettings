import socket


class BaseMeta:
    def is_active(self):
        return socket.gethostname() in getattr(self, 'hosts', [])


class ConfBase(type):
    def __new__(cls, name, bases, attrs):
        Meta = attrs.setdefault('Meta', type('Meta', (object,), {}))
        if BaseMeta not in Meta.__bases__:
            Meta.__bases__ += (BaseMeta,)
        return super(ConfBase, cls).__new__(cls, name, bases, attrs)

    def __init__(self, name, bases, attrs):
        super(ConfBase, self).__init__(name, bases, attrs)
        self._cbsettings_meta = self.Meta()


class Conf(object):
    __metaclass__ = ConfBase
