from ivi.ecosystem import IVIEcosystem
from ivi.belief_alignment import BeliefNode


def test_overall_score_combines_modules():
    tree = BeliefNode(label="growth")
    tree.add_child(BeliefNode(label="success"))
    eco = IVIEcosystem(belief_tree=tree)
    eco.add_interaction("idea1", user="alice", tags=["success"], description="first")
    eco.add_interaction("idea1", user="bob", tags=["note"], description="second")
    score = eco.overall_score("idea1")
    # impact_score = 1/2 (one useful tag), trust_score = 2/2, alignment = 1/2 -> overall = 0.4*0.5 + 0.4*1 + 0.2*0.5 = 0.7
    assert abs(score - 0.7) < 1e-6
