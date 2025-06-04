import pytest

try:
    from ivi.firebase_utils import (
        init_firebase,
        verify_token,
        save_interaction,
        save_evaluation,
    )

    from ivi.firebase_utils import init_firebase, verify_token, save_interaction
except Exception:
    pytest.skip("firebase not available", allow_module_level=True)


def test_firebase_stubs():
    assert callable(init_firebase)
    assert callable(verify_token)
    assert callable(save_interaction)
    assert callable(save_evaluation)

