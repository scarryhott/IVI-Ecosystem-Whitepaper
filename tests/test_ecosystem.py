<<<<<<< HEAD
from ivi.ecosystem import IVIEcosystem
from ivi.belief_alignment import BeliefNode
=======

New
+32
-0

from ivi.ecosystem import IVIEcosystem
from ivi.belief_alignment import BeliefNode
from ivi.decentralized_scoring import Agent
>>>>>>> temp-branch


def test_overall_score_combines_modules():
    tree = BeliefNode(label="growth")
    tree.add_child(BeliefNode(label="success"))
    eco = IVIEcosystem(belief_tree=tree)
    eco.add_interaction("idea1", user="alice", tags=["success"], description="first")
    eco.add_interaction("idea1", user="bob", tags=["note"], description="second")
    score = eco.overall_score("idea1")
    # impact_score = 1/2 (one useful tag), trust_score = 2/2, alignment = 1/2 -> overall = 0.4*0.5 + 0.4*1 + 0.2*0.5 = 0.7
    assert abs(score - 0.7) < 1e-6
<<<<<<< HEAD
=======


def test_overall_score_with_content_weight():
    tree = BeliefNode(label="growth")
    tree.add_child(BeliefNode(label="success"))
    eco = IVIEcosystem(
        belief_tree=tree,
        impact_weight=0.3,
        trust_weight=0.3,
        alignment_weight=0.2,
        content_weight=0.2,
    )
    eco.add_interaction("idea2", user="alice", tags=["success"], description="x")
    eco.add_scoring_agent("idea2", Agent(name="len", evaluate=lambda t: len(t) / 10))
    eco.evaluate_content("idea2", "abcdef", user="alice")
    score = eco.overall_score("idea2")
    expected = 0.3 * 1 + 0.3 * 1 + 0.2 * 1 + 0.2 * 0.6
    assert abs(score - expected) < 1e-6
>>>>>>> temp-branch
