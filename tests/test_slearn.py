from ivi.ecosystem import IVIEcosystem
from ivi.belief_alignment import BeliefNode
from ivi.slearn import LearningNode


def test_slearn_unlocks_with_tokens():
    tree = BeliefNode(label="growth")
    tree.add_child(BeliefNode(label="success"))
    eco = IVIEcosystem(belief_tree=tree)
    eco.add_learning_node(LearningNode(node_id="lesson1", required_tokens=0.1))
    eco.add_interaction("idea", user="alice", tags=["note"], description="x")
    available = eco.learning_map.available_nodes("alice")
    assert "lesson1" in available
    assert eco.complete_lesson("alice", "lesson1")

