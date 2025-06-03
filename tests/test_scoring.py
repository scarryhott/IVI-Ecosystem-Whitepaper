import pytest
from ivi.decentralized_scoring import cyclic_revision, Agent, ScoringSystem


def test_cyclic_revision_initial_append():
    history = []
    score = cyclic_revision(history, 0.8)
    assert score == 0.8
    assert history == [0.8]


def test_scoring_system_runs_agent():
    agent = Agent(name="echo", evaluate=lambda text: len(text))
    system = ScoringSystem(item_id="x", agents=[agent])
    result = system.run_agents("abcd")
    assert result == system.score_history[-1]
    assert result == len("abcd")
