from ivi.traceability import IdeaTrace


def test_add_event_timezone():
    trace = IdeaTrace(idea_id='x')
    trace.add_event(actor='alice', description='start')
    assert trace.events[0].timestamp.tzinfo is not None
