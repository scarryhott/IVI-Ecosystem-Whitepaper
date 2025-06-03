from ivi.philosophical_heuristics import fractal_integrity, predictive_coherence


def test_fractal_integrity_constant_values():
    assert fractal_integrity([1, 1, 1]) == 1.0


def test_predictive_coherence_perfect_match():
    assert predictive_coherence([0.5, 0.7], [0.5, 0.7]) == 1.0
