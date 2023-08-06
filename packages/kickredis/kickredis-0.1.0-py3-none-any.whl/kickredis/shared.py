from dataclasses import dataclass

from lightbus.message import EventMessage


@dataclass
class QuestionHandle:
    id: str


class KStream:
    REDIS_STREAM_API_NAME = "KickerStream"

    def __init__(self, event_transport, stream_id):
        self.event_transport = event_transport
        self.stream_id = stream_id

    async def send_event(self, event_dict):
        await self.event_transport.send_event(
            EventMessage(
                api_name=KStream.REDIS_STREAM_API_NAME,
                event_name=f"{self.stream_id}",
                id=f"{self.stream_id}",
                kwargs=event_dict,
            ),
            options={},
        )

    def consume(self, consumer_name: str):
        return self.event_transport.consume(
            [(KStream.REDIS_STREAM_API_NAME, self.stream_id)],
            consumer_name,
            error_queue=None,
        )

    async def acknowledge(self, msg):
        await self.event_transport.acknowledge(msg)
