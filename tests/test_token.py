from ivi.token import TokenLedger
from ivi.ecosystem import IVIEcosystem
from ivi.belief_alignment import BeliefNode


def test_mint_and_transfer():
    ledger = TokenLedger()
    ledger.mint('alice', 1.5)
    assert ledger.balance_of('alice') == 1.5
    assert ledger.transfer('alice', 'bob', 1.0)
    assert ledger.balance_of('alice') == 0.5
    assert ledger.balance_of('bob') == 1.0


def test_interaction_mints_tokens():
    tree = BeliefNode(label='growth')
    tree.add_child(BeliefNode(label='success'))
    eco = IVIEcosystem(belief_tree=tree)
    eco.add_interaction('idea', user='alice', tags=['note'], description='x')
    # initial score -> tokens minted for alice
    balance = eco.ledger.balance_of('alice')
    assert balance > 0
    # second interaction by bob should increase score slightly
    eco.add_interaction('idea', user='bob', tags=['success'], description='y')
    assert eco.ledger.balance_of('bob') > 0
