from ivi.usefulness import UsefulnessRecord


def test_impact_score_basic():
    record = UsefulnessRecord(item_id='x')
    record.add_feedback(user='alice', tag='success', notes='good')
    record.add_feedback(user='bob', tag='aha', notes='useful')
    record.add_feedback(user='carol', tag='solution', notes='fixed')
    record.add_feedback(user='dave', tag='other', notes='meh')
    assert record.impact_score() == 3/4
