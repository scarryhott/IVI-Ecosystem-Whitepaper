from ivi.events import EventBus
import asyncio

def test_event_bus_publish():
    bus = EventBus()
    received = []
    bus.subscribe(lambda t, p: received.append((t, p)))
    asyncio.run(bus.publish("ping", {"ok": True}))
    assert received == [("ping", {"ok": True})]
