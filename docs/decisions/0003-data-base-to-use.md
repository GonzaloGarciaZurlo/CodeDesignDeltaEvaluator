---
# These are optional elements. Feel free to remove any of them.
status: {proposed}
date: {2024-09-16 when the decision was last updated}
deciders: {Daniel Gutson, Gonzalo García Zurlo}
consulted: {Daniel Gutson}
informed: {Daniel Gutson}
---
# Deciding which library to use for parsing

## Context and Problem Statement

What tool is most convenient for my project to save graphs in a database?

## Considered Options

* Neo4j
* Memgraph
* Amazon Neptune

## Decision Outcome

Memgraph:

Advantages: Very efficient for Cypher and good integration with Python, ideal for embedded or local solutions.
Disadvantages: Does not support Gremlin.

Neo4j:

Advantages: Excellent for Cypher, with the possibility of Gremlin via porting (not native).
Disadvantages: Embedded Neo4j is more complicated to configure compared to Memgraph and does not support Gremlin natively.

Amazon Neptune:

Advantages: Supports both Cypher and Gremlin, ideal if you need both query languages.
Disadvantages: It is a cloud solution, which can be a drawback if you are looking for something completely on-premise or embedded.

Choosing **Memgraph** offers high-performance graph processing with **Cypher** in real-time scenarios, but lacks **Gremlin** support. **Neo4j** is the best option for **Cypher** queries, with some experimental **Gremlin** support, but it prioritizes Cypher, making Gremlin less reliable. **Amazon Neptune** provides native **Gremlin** support and limited **Cypher** via openCypher, making it a versatile choice if you need both languages, but it might not offer the same performance and ease of use as Neo4j for Cypher-based projects.


---
Chosen option: "{title of option 1}", because
{justification. e.g., only option, which meets k.o. criterion decision driver | which resolves force {force} | … | comes out best (see below)}.

### Consequences


