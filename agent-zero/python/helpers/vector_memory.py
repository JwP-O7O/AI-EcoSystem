"""
Lightweight Vector Memory System for Termux/Android
Uses sentence-transformers with a small model and SQLite for storage
No heavy dependencies like ChromaDB
"""

import sqlite3
import json
import numpy as np
from typing import List, Dict, Tuple, Optional
from datetime import datetime
import os
from python.helpers import files

class VectorMemory:
    """
    Lightweight vector-based memory using sentence transformers and SQLite
    Optimized for Termux/Android with minimal dependencies
    """

    def __init__(self, db_path: str = None, embedding_model: str = "all-MiniLM-L6-v2"):
        """
        Initialize vector memory

        Args:
            db_path: Path to SQLite database
            embedding_model: Sentence transformer model name (default: small 80MB model)
        """
        self.db_path = db_path or files.get_abs_path("memory", "vector_memory.db")
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        # Initialize database
        self._init_database()

        # Lazy load embedding model (only when needed)
        self._embedding_model = None
        self._embedding_model_name = embedding_model
        self._embedding_dim = None

    def _init_database(self):
        """Create database tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Main memory table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                embedding BLOB NOT NULL,
                memory_type TEXT,
                agent_name TEXT,
                timestamp TEXT,
                metadata TEXT
            )
        """)

        # Index for faster lookups
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_memory_type
            ON memories(memory_type)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_timestamp
            ON memories(timestamp)
        """)

        conn.commit()
        conn.close()

    def _get_embedding_model(self):
        """Lazy load embedding model"""
        if self._embedding_model is None:
            try:
                from sentence_transformers import SentenceTransformer
                print(f"Loading embedding model: {self._embedding_model_name}...")
                self._embedding_model = SentenceTransformer(self._embedding_model_name)
                self._embedding_dim = self._embedding_model.get_sentence_embedding_dimension()
                print(f"Model loaded (dimension: {self._embedding_dim})")
            except ImportError:
                raise ImportError(
                    "sentence-transformers not installed. "
                    "Install with: pip install sentence-transformers"
                )
        return self._embedding_model

    def _text_to_embedding(self, text: str) -> np.ndarray:
        """Convert text to embedding vector"""
        model = self._get_embedding_model()
        embedding = model.encode(text, convert_to_numpy=True)
        return embedding

    def _embedding_to_bytes(self, embedding: np.ndarray) -> bytes:
        """Convert numpy array to bytes for storage"""
        return embedding.tobytes()

    def _bytes_to_embedding(self, blob: bytes) -> np.ndarray:
        """Convert bytes back to numpy array"""
        if self._embedding_dim is None:
            # Need to initialize model to get dimension
            self._get_embedding_model()
        return np.frombuffer(blob, dtype=np.float32).reshape(self._embedding_dim)

    def add_memory(
        self,
        content: str,
        memory_type: str = "general",
        agent_name: str = "Agent 0",
        metadata: Dict = None
    ) -> int:
        """
        Add a memory to the vector database

        Args:
            content: The text content to remember
            memory_type: Type of memory (general, solution, fact, instruction, etc.)
            agent_name: Name of the agent storing this memory
            metadata: Additional metadata as dict

        Returns:
            Memory ID
        """
        # Generate embedding
        embedding = self._text_to_embedding(content)
        embedding_bytes = self._embedding_to_bytes(embedding)

        # Store in database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO memories (content, embedding, memory_type, agent_name, timestamp, metadata)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            content,
            embedding_bytes,
            memory_type,
            agent_name,
            datetime.now().isoformat(),
            json.dumps(metadata or {})
        ))

        memory_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return memory_id

    def search(
        self,
        query: str,
        top_k: int = 5,
        memory_type: str = None,
        similarity_threshold: float = 0.3
    ) -> List[Dict]:
        """
        Search for similar memories using cosine similarity

        Args:
            query: Search query text
            top_k: Number of results to return
            memory_type: Filter by memory type (optional)
            similarity_threshold: Minimum similarity score (0-1)

        Returns:
            List of memory dicts with similarity scores
        """
        # Generate query embedding
        query_embedding = self._text_to_embedding(query)

        # Fetch memories from database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if memory_type:
            cursor.execute("""
                SELECT id, content, embedding, memory_type, agent_name, timestamp, metadata
                FROM memories
                WHERE memory_type = ?
            """, (memory_type,))
        else:
            cursor.execute("""
                SELECT id, content, embedding, memory_type, agent_name, timestamp, metadata
                FROM memories
            """)

        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return []

        # Calculate similarities
        results = []
        for row in rows:
            memory_id, content, embedding_bytes, mem_type, agent, timestamp, metadata_str = row

            # Convert embedding
            memory_embedding = self._bytes_to_embedding(embedding_bytes)

            # Cosine similarity
            similarity = self._cosine_similarity(query_embedding, memory_embedding)

            if similarity >= similarity_threshold:
                results.append({
                    "id": memory_id,
                    "content": content,
                    "similarity": float(similarity),
                    "memory_type": mem_type,
                    "agent_name": agent,
                    "timestamp": timestamp,
                    "metadata": json.loads(metadata_str)
                })

        # Sort by similarity and return top_k
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]

    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors"""
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)

    def delete_memory(self, memory_id: int):
        """Delete a specific memory"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM memories WHERE id = ?", (memory_id,))
        conn.commit()
        conn.close()

    def clear_all(self, memory_type: str = None):
        """Clear all memories or specific type"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if memory_type:
            cursor.execute("DELETE FROM memories WHERE memory_type = ?", (memory_type,))
        else:
            cursor.execute("DELETE FROM memories")

        conn.commit()
        conn.close()

    def get_memory_stats(self) -> Dict:
        """Get statistics about stored memories"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Total count
        cursor.execute("SELECT COUNT(*) FROM memories")
        total = cursor.fetchone()[0]

        # Count by type
        cursor.execute("""
            SELECT memory_type, COUNT(*) as count
            FROM memories
            GROUP BY memory_type
        """)
        by_type = {row[0]: row[1] for row in cursor.fetchall()}

        # Database size
        cursor.execute("SELECT page_count * page_size as size FROM pragma_page_count(), pragma_page_size()")
        db_size = cursor.fetchone()[0]

        conn.close()

        return {
            "total_memories": total,
            "by_type": by_type,
            "database_size_bytes": db_size,
            "database_size_mb": round(db_size / (1024 * 1024), 2)
        }


# Global instance for easy access
_global_memory: Optional[VectorMemory] = None

def get_memory() -> VectorMemory:
    """Get or create global vector memory instance"""
    global _global_memory
    if _global_memory is None:
        _global_memory = VectorMemory()
    return _global_memory
