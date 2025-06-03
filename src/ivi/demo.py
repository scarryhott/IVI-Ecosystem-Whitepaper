"""Simple demonstration of IVI modules."""

from datetime import datetime, timezone

from . import (
    Agent,
    BeliefNode,
    IdeaTrace,
    ReputationTrail,
    ScoringSystem,
    UsefulnessRecord,
    score_alignment,
    semantic_provenance,
    temporal_layering,
)


def main() -> None:
    # Traceability example
    trace = IdeaTrace(idea_id="idea1")
    trace.add_event(actor="alice", description="shared initial concept")
    trace.add_event(actor="bob", description="expanded on concept")
    print("Origin Map:", trace.origin_map())

    # Usefulness example
    use = UsefulnessRecord(item_id="idea1")
    use.add_feedback(user="alice", tag="aha", notes="helped me solve a problem")
    use.add_feedback(user="carol", tag="note", notes="interesting")
    print("Impact Score:", use.impact_score())

    # Belief alignment example
    root = BeliefNode(label="growth")
    root.add_child(BeliefNode(label="freedom"))
    alignment = score_alignment(["growth", "justice"], root)
    print("Alignment Score:", alignment)

    # Social verification example
    rep = ReputationTrail(item_id="idea1")
    rep.add_event(actor="alice", description="used in project")
    rep.add_event(actor="bob", description="discussed in community")
    print("Trust Score:", rep.trust_score())

    # Decentralized scoring example
    agent = Agent(name="length_checker", evaluate=lambda text: len(text) / 100)
    scoring = ScoringSystem(item_id="idea1", agents=[agent])
    print("Initial Score:", scoring.run_agents("sample content"))

    # Contextual metrics
    sem_score = semantic_provenance("hello world", ["hello", "world news"])
    now = datetime.now(timezone.utc)
    temp_weight = temporal_layering(now, now)
    print("Semantic Provenance:", sem_score)
    print("Temporal Weight:", temp_weight)


if __name__ == "__main__":
    main()
