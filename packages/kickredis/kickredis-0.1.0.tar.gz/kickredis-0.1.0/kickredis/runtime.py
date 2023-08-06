from lightbus.transports.redis.event import RedisEventTransport, StreamUse

from kickredis.registry import ObjectRegistry
from kickredis.config import kicker_config
from kickredis.shared import KStream


class KickerRuntime:
    def __init__(self):
        self._event_transport = RedisEventTransport(
            service_name="", consumer_name="", stream_use=StreamUse.PER_EVENT
        )
        self._object_registry = ObjectRegistry(kicker_config.redis)

    @property
    def object_registry(self):
        return self._object_registry

    @property
    def event_transport(self):
        return self._event_transport

    def get_kstream(self, stream_id):
        return KStream(self.event_transport, stream_id)


kicker_runtime = KickerRuntime()
