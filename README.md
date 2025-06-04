# IVI Ecosystem

A Framework for a Self-Governing, Self-Expanding, Meaning-Driven Intelligence & Community Ecosystem.

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

This repository contains a Python implementation of **Intangibly Verified Information (IVI)** concepts. The `src/ivi` package provides utility modules demonstrating:

- **Contextual Traceability**: Track the origin and evolution of ideas
- **Usefulness Verification**: Measure the impact and utility of information
- **Belief Alignment**: Align information with belief systems
- **Social Verification**: Establish trust through community validation
- **Structural Redundancy**: Ensure robustness through pattern repetition
- **Philosophical Heuristics**: Apply philosophical principles to information verification
- **Decentralized Scoring**: Enable distributed, AI-assisted scoring mechanisms

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/scarryhott/IVI-Ecosystem-Whitepaper.git
   cd IVI-Ecosystem-Whitepaper
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the package in development mode:
   ```bash
   pip install -e .[test]
   ```

## Quick Start

Run the demo script to see the modules in action:

```bash
python -m ivi.demo
```

## SlearnMap and LearningNode

`SlearnMap` organizes lessons as token-gated nodes. Each `LearningNode`
defines a lesson and the IVI tokens required to unlock it. The
`IVIEcosystem` automatically provisions a `SlearnMap` so you can attach
nodes and track completion.

Example usage:

```python
from ivi import IVIEcosystem, LearningNode

eco = IVIEcosystem()
eco.add_learning_node(LearningNode(node_id="intro", required_tokens=0))
eco.add_interaction("idea", user="bob", tags=["note"], description="start")
available = eco.learning_map.available_nodes("bob")  # ["intro"]
eco.complete_lesson("bob", "intro")
```

## Development

To run the test suite:

```bash
pytest
```

## Project Structure

```
.
├── src/
│   └── ivi/                    # Main package
│       ├── __init__.py         # Package exports
│       ├── traceability.py     # Idea tracing and provenance
│       ├── usefulness.py       # Usefulness verification
│       ├── belief_alignment.py # Belief system integration
│       ├── social_verification.py # Community validation
│       ├── redundancy.py       # Pattern integrity
│       ├── philosophical_heuristics.py # Philosophical metrics
│       └── decentralized_scoring.py # Distributed scoring
├── tests/                      # Test suite
├── pyproject.toml              # Project metadata and dependencies
└── README.md                   # This file
```
## Real-Time Dashboard

The optional `ivi.web` module exposes a FastAPI application that stores
interactions in an SQLite database and streams updates via WebSocket.
Launch the server with:

```bash
uvicorn ivi.web:app --reload
```

Then visit `/dashboard` to see a live feed of interactions.

If `firebase-admin` is installed and the environment variable `FIREBASE_CRED`
points to a service account JSON file, the dashboard will use Firebase for login
and store interactions in Firestore.

### Dashboard Features

- **User Profile:** Displays individual reputation scores, belief alignment
  metrics, and contribution history.
- **AI Interaction:** Provides personalized guidance and feedback based on user
  activity and ecosystem dynamics.
- **Token Management:** Lets users manage the tokens earned through their
  contributions and interactions.
- **Marketplace:** Facilitates trading and collaboration based on reputation and
  token holdings.
- **Marketplace Creation:** Launch products using the AI-assisted creation flow.



## Marketplace and Creation Flow

The `ivi.marketplace` module introduces a simple in-memory marketplace for
tokenized products. You can register new products and retrieve them later. The
`CreationFlow` helper connects the marketplace with the `IVIEcosystem` so newly
created products are automatically traced and scored.

Example usage:

```python
from ivi import IVIEcosystem, Marketplace, CreationFlow

eco = IVIEcosystem()
market = Marketplace()
flow = CreationFlow(marketplace=market, eco=eco)

flow.create_product(
    product_id="tool1",
    creator="alice",
    name="Flow State Toolkit",
    description="Unlock better focus",
    required_tokens=1,
    belief_tag="focus",
)

print(market.list_products())
```


Then visit `/dashboard` to log in with a Firebase ID token and submit
interactions. If `firebase-admin` is installed and the environment variable
`FIREBASE_CRED` points to a service account JSON file, the dashboard verifies
tokens and records interactions in Firestore. Interactions are processed through
the IVI ecosystem, so the resulting score and the user's token balance are
stored alongside the description. Evaluation requests are also saved to an
`evaluations` collection.

## Marketplace and Creation Flow

The `ivi.marketplace` module introduces a simple in-memory marketplace for
tokenized products. You can register new products and retrieve them later. The
`CreationFlow` helper connects the marketplace with the `IVIEcosystem` so newly
created products are automatically traced and scored.

Example usage:

```python
from ivi import IVIEcosystem, Marketplace, CreationFlow

eco = IVIEcosystem()
market = Marketplace()
flow = CreationFlow(marketplace=market, eco=eco)

flow.create_product(
    product_id="tool1",
    creator="alice",
    name="Flow State Toolkit",
    description="Unlock better focus",
    required_tokens=1,
    belief_tag="focus",
)

print(market.list_products())
```

## Real-Time Dashboard

The optional `ivi.web` module exposes a FastAPI application that stores
interactions in an SQLite database and streams updates via WebSocket.
Launch the server with:

```bash
uvicorn ivi.web:app --reload
```

Then visit `/dashboard` to log in with a Firebase ID token and submit
interactions. If `firebase-admin` is installed and the environment variable
`FIREBASE_CRED` points to a service account JSON file, the dashboard verifies
tokens and records interactions in Firestore. Interactions are processed through
the IVI ecosystem, so the resulting score and the user's token balance are
stored alongside the description. Evaluation requests are also saved to an
`evaluations` collection. The dashboard lists marketplace products via `/products`,
shows your token balance from `/profile`, and lets you add new listings through
an AI-assisted creation flow triggered by the **Create Product** button.

## Contributing

Contributions are welcome! Please see [CONTRIBUTIONS.md](CONTRIBUTIONS.md) for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
