from ivi.marketplace import Marketplace, Product, CreationFlow
from ivi.ecosystem import IVIEcosystem


def test_add_and_get_product():
    market = Marketplace()
    product = Product(
        product_id="p1",
        creator="alice",
        name="Test Product",
        description="desc",
        required_tokens=1,
        belief_tag="growth",
    )
    market.add_product(product)
    assert market.get_product("p1") == product
    assert len(market.list_products()) == 1


def test_creation_flow_registers_product():
    eco = IVIEcosystem()
    market = Marketplace()
    flow = CreationFlow(marketplace=market, eco=eco)
    flow.create_product(
        product_id="p2",
        creator="bob",
        name="Flow Product",
        description="desc",
        required_tokens=0,
        belief_tag="success",
    )
    created = market.get_product("p2")
    assert created is not None
    # interaction should exist in the ecosystem's trace
    assert "p2" in eco.traces
