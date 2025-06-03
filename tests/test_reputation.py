from ivi.social_verification import ReputationTrail


def test_trust_score_unique_actors():
    trail = ReputationTrail(item_id='x')
    trail.add_event(actor='alice', description='first')
    trail.add_event(actor='alice', description='second')
    trail.add_event(actor='bob', description='third')
    assert trail.trust_score() == 2/3
