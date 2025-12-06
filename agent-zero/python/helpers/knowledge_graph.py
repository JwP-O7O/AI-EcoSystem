"""
Knowledge Graph - Dynamic knowledge management with graph relationships
"""

import json
from typing import List, Dict, Set, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class Entity:
    """Represents an entity in the knowledge graph"""
    id: str
    type: str  # person, project, concept, file, tool, etc.
    name: str
    attributes: Dict[str, any]

    def to_dict(self):
        return asdict(self)


@dataclass
class Relationship:
    """Represents a relationship between entities"""
    source_id: str
    target_id: str
    type: str  # uses, creates, depends_on, related_to, etc.
    weight: float = 1.0
    attributes: Dict[str, any] = None

    def to_dict(self):
        return asdict(self)


class KnowledgeGraph:
    """
    Dynamic knowledge graph for Agent Zero

    Features:
    - Entity and relationship management
    - Graph traversal and path finding
    - Semantic queries
    - Integration with vector memory
    - Export to various formats
    """

    def __init__(self, storage_path: str = None):
        self.entities: Dict[str, Entity] = {}
        self.relationships: List[Relationship] = []
        self.storage_path = storage_path or "work_dir/knowledge_graph.json"

        # Load existing graph if available
        self.load()

    def add_entity(self, entity: Entity) -> Entity:
        """Add or update an entity"""
        self.entities[entity.id] = entity
        return entity

    def get_entity(self, entity_id: str) -> Optional[Entity]:
        """Get entity by ID"""
        return self.entities.get(entity_id)

    def find_entities(self, entity_type: str = None, **attributes) -> List[Entity]:
        """Find entities by type and/or attributes"""
        results = []

        for entity in self.entities.values():
            # Check type
            if entity_type and entity.type != entity_type:
                continue

            # Check attributes
            match = True
            for key, value in attributes.items():
                if entity.attributes.get(key) != value:
                    match = False
                    break

            if match:
                results.append(entity)

        return results

    def add_relationship(self, source_id: str, target_id: str,
                        rel_type: str, weight: float = 1.0,
                        **attributes) -> Relationship:
        """Add a relationship between entities"""

        # Verify entities exist
        if source_id not in self.entities or target_id not in self.entities:
            raise ValueError(f"Both entities must exist: {source_id}, {target_id}")

        rel = Relationship(
            source_id=source_id,
            target_id=target_id,
            type=rel_type,
            weight=weight,
            attributes=attributes or {}
        )

        self.relationships.append(rel)
        return rel

    def get_relationships(self, entity_id: str,
                         direction: str = "both",
                         rel_type: str = None) -> List[Relationship]:
        """
        Get relationships for an entity

        Args:
            entity_id: Entity to get relationships for
            direction: 'incoming', 'outgoing', or 'both'
            rel_type: Filter by relationship type
        """
        results = []

        for rel in self.relationships:
            include = False

            if direction in ["outgoing", "both"] and rel.source_id == entity_id:
                include = True
            if direction in ["incoming", "both"] and rel.target_id == entity_id:
                include = True

            if include and (rel_type is None or rel.type == rel_type):
                results.append(rel)

        return results

    def get_neighbors(self, entity_id: str, rel_type: str = None) -> List[Entity]:
        """Get all neighboring entities"""
        neighbors = []
        rels = self.get_relationships(entity_id, "both", rel_type)

        for rel in rels:
            neighbor_id = rel.target_id if rel.source_id == entity_id else rel.source_id
            neighbor = self.get_entity(neighbor_id)
            if neighbor:
                neighbors.append(neighbor)

        return neighbors

    def find_path(self, start_id: str, end_id: str,
                  max_depth: int = 5) -> Optional[List[str]]:
        """Find shortest path between two entities (BFS)"""

        if start_id not in self.entities or end_id not in self.entities:
            return None

        if start_id == end_id:
            return [start_id]

        visited = set()
        queue = [(start_id, [start_id])]

        while queue:
            current_id, path = queue.pop(0)

            if len(path) > max_depth:
                continue

            if current_id in visited:
                continue

            visited.add(current_id)

            # Get neighbors
            neighbors = self.get_neighbors(current_id)

            for neighbor in neighbors:
                if neighbor.id == end_id:
                    return path + [neighbor.id]

                if neighbor.id not in visited:
                    queue.append((neighbor.id, path + [neighbor.id]))

        return None  # No path found

    def find_related(self, entity_id: str, max_distance: int = 2) -> Dict[str, int]:
        """
        Find all entities within max_distance hops
        Returns dict of entity_id -> distance
        """
        if entity_id not in self.entities:
            return {}

        distances = {entity_id: 0}
        visited = set([entity_id])
        current_level = [entity_id]

        for distance in range(1, max_distance + 1):
            next_level = []

            for current_id in current_level:
                neighbors = self.get_neighbors(current_id)

                for neighbor in neighbors:
                    if neighbor.id not in visited:
                        visited.add(neighbor.id)
                        distances[neighbor.id] = distance
                        next_level.append(neighbor.id)

            current_level = next_level
            if not current_level:
                break

        return distances

    def get_central_entities(self, top_n: int = 10) -> List[Tuple[Entity, int]]:
        """Get most connected entities (degree centrality)"""

        degree_map = {}

        for entity_id in self.entities:
            degree = len(self.get_relationships(entity_id, "both"))
            degree_map[entity_id] = degree

        # Sort by degree
        sorted_entities = sorted(degree_map.items(), key=lambda x: x[1], reverse=True)

        results = []
        for entity_id, degree in sorted_entities[:top_n]:
            entity = self.get_entity(entity_id)
            if entity:
                results.append((entity, degree))

        return results

    def query(self, query_type: str, **params) -> any:
        """
        Execute graph queries

        Query types:
        - "path": Find path between entities
        - "neighbors": Get neighbors of entity
        - "related": Find related entities within distance
        - "central": Get central entities
        - "subgraph": Extract subgraph around entity
        """

        if query_type == "path":
            return self.find_path(params["start"], params["end"],
                                 params.get("max_depth", 5))

        elif query_type == "neighbors":
            return self.get_neighbors(params["entity_id"],
                                     params.get("rel_type"))

        elif query_type == "related":
            return self.find_related(params["entity_id"],
                                    params.get("max_distance", 2))

        elif query_type == "central":
            return self.get_central_entities(params.get("top_n", 10))

        elif query_type == "subgraph":
            return self._extract_subgraph(params["entity_id"],
                                         params.get("depth", 2))

        else:
            raise ValueError(f"Unknown query type: {query_type}")

    def _extract_subgraph(self, entity_id: str, depth: int = 2) -> Dict:
        """Extract subgraph around an entity"""

        related = self.find_related(entity_id, depth)
        entity_ids = list(related.keys())

        subgraph_entities = {eid: self.entities[eid] for eid in entity_ids}
        subgraph_rels = [rel for rel in self.relationships
                        if rel.source_id in entity_ids and rel.target_id in entity_ids]

        return {
            "entities": subgraph_entities,
            "relationships": subgraph_rels,
            "center": entity_id
        }

    def save(self):
        """Save graph to disk"""
        data = {
            "entities": {eid: e.to_dict() for eid, e in self.entities.items()},
            "relationships": [r.to_dict() for r in self.relationships]
        }

        Path(self.storage_path).parent.mkdir(parents=True, exist_ok=True)

        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2)

    def load(self):
        """Load graph from disk"""
        if not Path(self.storage_path).exists():
            return

        try:
            with open(self.storage_path, 'r') as f:
                data = json.load(f)

            # Load entities
            self.entities = {}
            for eid, e_data in data.get("entities", {}).items():
                self.entities[eid] = Entity(**e_data)

            # Load relationships
            self.relationships = []
            for r_data in data.get("relationships", []):
                self.relationships.append(Relationship(**r_data))

        except Exception as e:
            print(f"Error loading knowledge graph: {e}")

    def to_json(self) -> str:
        """Export graph as JSON"""
        data = {
            "entities": [e.to_dict() for e in self.entities.values()],
            "relationships": [r.to_dict() for r in self.relationships]
        }
        return json.dumps(data, indent=2)

    def to_graphviz(self) -> str:
        """Export graph as Graphviz DOT format"""
        lines = ["digraph KnowledgeGraph {"]
        lines.append("  rankdir=LR;")
        lines.append("  node [shape=box];")

        # Add entities
        for entity in self.entities.values():
            label = f"{entity.name}\\n({entity.type})"
            lines.append(f'  "{entity.id}" [label="{label}"];')

        # Add relationships
        for rel in self.relationships:
            label = rel.type
            lines.append(f'  "{rel.source_id}" -> "{rel.target_id}" [label="{label}"];')

        lines.append("}")
        return "\n".join(lines)

    def stats(self) -> Dict:
        """Get graph statistics"""
        return {
            "total_entities": len(self.entities),
            "total_relationships": len(self.relationships),
            "entity_types": self._count_entity_types(),
            "relationship_types": self._count_relationship_types(),
            "avg_degree": self._average_degree(),
            "max_degree": self._max_degree()
        }

    def _count_entity_types(self) -> Dict[str, int]:
        counts = {}
        for entity in self.entities.values():
            counts[entity.type] = counts.get(entity.type, 0) + 1
        return counts

    def _count_relationship_types(self) -> Dict[str, int]:
        counts = {}
        for rel in self.relationships:
            counts[rel.type] = counts.get(rel.type, 0) + 1
        return counts

    def _average_degree(self) -> float:
        if not self.entities:
            return 0.0
        total = sum(len(self.get_relationships(eid, "both"))
                   for eid in self.entities)
        return total / len(self.entities)

    def _max_degree(self) -> int:
        if not self.entities:
            return 0
        return max(len(self.get_relationships(eid, "both"))
                  for eid in self.entities)


class KnowledgeGraphBuilder:
    """Helper class to build knowledge graphs from conversations and code"""

    def __init__(self, graph: KnowledgeGraph):
        self.graph = graph

    def extract_from_conversation(self, messages: List[Dict]) -> None:
        """Extract entities and relationships from conversation history"""
        # This would use NLP to extract entities
        # For now, simplified implementation
        pass

    def extract_from_code(self, file_path: str) -> None:
        """Extract entities and relationships from code"""
        import ast

        with open(file_path, 'r') as f:
            code = f.read()

        try:
            tree = ast.parse(code)

            # Create entity for the file
            file_entity = Entity(
                id=f"file:{file_path}",
                type="file",
                name=file_path,
                attributes={"language": "python"}
            )
            self.graph.add_entity(file_entity)

            # Extract functions and classes
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_entity = Entity(
                        id=f"func:{file_path}:{node.name}",
                        type="function",
                        name=node.name,
                        attributes={"line": node.lineno, "args": len(node.args.args)}
                    )
                    self.graph.add_entity(func_entity)

                    # Create relationship
                    self.graph.add_relationship(
                        file_entity.id,
                        func_entity.id,
                        "contains"
                    )

                elif isinstance(node, ast.ClassDef):
                    class_entity = Entity(
                        id=f"class:{file_path}:{node.name}",
                        type="class",
                        name=node.name,
                        attributes={"line": node.lineno}
                    )
                    self.graph.add_entity(class_entity)

                    self.graph.add_relationship(
                        file_entity.id,
                        class_entity.id,
                        "contains"
                    )

        except SyntaxError:
            pass
