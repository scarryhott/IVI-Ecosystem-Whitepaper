from ivi.belief_alignment import BeliefNode, score_alignment


def test_score_alignment_basic():
    root = BeliefNode(label='growth')
    root.add_child(BeliefNode(label='freedom'))
    score = score_alignment(['growth', 'freedom', 'other'], root)
    assert score == 2/3
