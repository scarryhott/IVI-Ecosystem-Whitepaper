from __future__ import annotations

"""Marketplace for tokenized, meaning-based products."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Product:
    """Representation of a marketplace product."""

    product_id: str
    creator: str
    name: str
    description: str
    required_tokens: int = 0
    belief_tag: str | None = None


@dataclass
class Marketplace:
    """Simple in-memory marketplace."""

    products: Dict[str, Product] = field(default_factory=dict)

    def add_product(self, product: Product) -> None:
        self.products[product.product_id] = product

    def get_product(self, product_id: str) -> Optional[Product]:
        return self.products.get(product_id)

    def list_products(self) -> List[Product]:
        return list(self.products.values())


@dataclass
class CreationFlow:
    """AI-assisted product creation flow (simplified)."""

    marketplace: Marketplace
    eco: "IVIEcosystem"

    def create_product(
        self,
        product_id: str,
        creator: str,
        name: str,
        description: str,
        required_tokens: int = 0,
        belief_tag: str | None = None,
    ) -> Product:
        # Register the idea within the ecosystem for traceability
        if belief_tag:
            self.eco.add_interaction(product_id, user=creator, tags=[belief_tag], description=name)
        else:
            self.eco.add_interaction(product_id, user=creator, tags=["product"], description=name)
        product = Product(
            product_id=product_id,
            creator=creator,
            name=name,
            description=description,
            required_tokens=required_tokens,
            belief_tag=belief_tag,
        )
        self.marketplace.add_product(product)
        return product
