"""
Persistent Memory Tool - SQLite-based Long-term Memory
Advanced memory system for Agent Zero on Android

Features:
- Persistent storage across sessions
- Full-text search
- Tagging system
- Importance ranking
- Contextual retrieval
- Memory summarization
"""

import sqlite3
import json
import hashlib
from datetime import datetime
from typing import List, Dict, Optional
from python.helpers.tool import Tool, Response


class PersistentMemory(Tool):
    """Advanced persistent memory system using SQLite"""

    def __init__(self, agent, name: str, args: dict, message: str, **kwargs):
        super().__init__(agent, name, args, message, **kwargs)
        self.db_path = self._get_db_path()
        self._init_database()

    def _get_db_path(self) -> str:
        """Get database file path"""
        import os
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        db_dir = os.path.join(base_dir, "memory_db")
        os.makedirs(db_dir, exist_ok=True)
        return os.path.join(db_dir, "agent_memory.db")

    def _init_database(self):
        """Initialize SQLite database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Memories table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                content_hash TEXT UNIQUE,
                summary TEXT,
                importance INTEGER DEFAULT 5,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                accessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                access_count INTEGER DEFAULT 0,
                context TEXT,
                source TEXT
            )
        """)

        # Tags table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                memory_id INTEGER,
                tag TEXT NOT NULL,
                FOREIGN KEY (memory_id) REFERENCES memories (id) ON DELETE CASCADE
            )
        """)

        # Full-text search virtual table
        cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts USING fts5(
                content, summary, tags,
                content='memories',
                content_rowid='id'
            )
        """)

        # Triggers to keep FTS in sync
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS memories_ai AFTER INSERT ON memories BEGIN
                INSERT INTO memories_fts(rowid, content, summary)
                VALUES (new.id, new.content, new.summary);
            END
        """)

        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS memories_ad AFTER DELETE ON memories BEGIN
                DELETE FROM memories_fts WHERE rowid = old.id;
            END
        """)

        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS memories_au AFTER UPDATE ON memories BEGIN
                UPDATE memories_fts SET content = new.content, summary = new.summary
                WHERE rowid = new.id;
            END
        """)

        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_importance ON memories(importance DESC)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_accessed ON memories(accessed_at DESC)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tags_memory ON tags(memory_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tags_tag ON tags(tag)")

        conn.commit()
        conn.close()

    async def execute(self, **kwargs):
        """Execute memory operations"""
        operation = self.args.get("operation", "").lower()

        try:
            if operation == "store":
                return await self._store_memory()
            elif operation == "recall":
                return await self._recall_memories()
            elif operation == "search":
                return await self._search_memories()
            elif operation == "update":
                return await self._update_memory()
            elif operation == "delete":
                return await self._delete_memory()
            elif operation == "list":
                return await self._list_memories()
            elif operation == "stats":
                return await self._get_stats()
            elif operation == "summarize":
                return await self._summarize_memories()
            else:
                return Response(
                    message=f"Unknown operation: {operation}\n\n"
                           f"Available: store, recall, search, update, delete, list, stats, summarize",
                    break_loop=False
                )
        except Exception as e:
            return Response(
                message=f"Memory operation failed: {str(e)}",
                break_loop=False
            )

    async def _store_memory(self) -> Response:
        """Store new memory"""
        content = self.args.get("content", "")
        summary = self.args.get("summary", content[:200])
        importance = self.args.get("importance", 5)  # 1-10
        tags = self.args.get("tags", [])
        context = self.args.get("context", "")
        source = self.args.get("source", "user")

        if not content:
            return Response(message="Cannot store empty memory", break_loop=False)

        # Calculate content hash to avoid duplicates
        content_hash = hashlib.sha256(content.encode()).hexdigest()

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Store memory
            cursor.execute("""
                INSERT INTO memories (content, content_hash, summary, importance, context, source)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (content, content_hash, summary, importance, context, source))

            memory_id = cursor.lastrowid

            # Store tags
            if tags:
                for tag in tags:
                    cursor.execute("""
                        INSERT INTO tags (memory_id, tag)
                        VALUES (?, ?)
                    """, (memory_id, tag.lower()))

            conn.commit()

            return Response(
                message=f"✓ Memory stored (ID: {memory_id})\n"
                       f"Tags: {', '.join(tags) if tags else 'none'}\n"
                       f"Importance: {importance}/10",
                break_loop=False
            )

        except sqlite3.IntegrityError:
            # Duplicate content
            return Response(
                message="⚠️  Similar memory already exists (duplicate content)",
                break_loop=False
            )
        finally:
            conn.close()

    async def _recall_memories(self) -> Response:
        """Recall relevant memories based on context"""
        context = self.args.get("context", "")
        tags = self.args.get("tags", [])
        limit = self.args.get("limit", 5)
        min_importance = self.args.get("min_importance", 3)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Build query
        query = """
            SELECT DISTINCT m.id, m.content, m.summary, m.importance,
                   m.created_at, m.access_count, m.context
            FROM memories m
            LEFT JOIN tags t ON m.id = t.memory_id
            WHERE m.importance >= ?
        """
        params = [min_importance]

        # Filter by tags if provided
        if tags:
            placeholders = ','.join('?' * len(tags))
            query += f" AND t.tag IN ({placeholders})"
            params.extend([tag.lower() for tag in tags])

        # Order by importance and recency
        query += """
            ORDER BY m.importance DESC, m.accessed_at DESC
            LIMIT ?
        """
        params.append(limit)

        cursor.execute(query, params)
        results = cursor.fetchall()

        if not results:
            conn.close()
            return Response(
                message="No relevant memories found",
                break_loop=False
            )

        # Update access stats
        memory_ids = [r[0] for r in results]
        cursor.execute(f"""
            UPDATE memories
            SET accessed_at = CURRENT_TIMESTAMP,
                access_count = access_count + 1
            WHERE id IN ({','.join('?' * len(memory_ids))})
        """, memory_ids)
        conn.commit()

        # Format response
        memories_text = []
        for idx, (mem_id, content, summary, importance, created, access_count, ctx) in enumerate(results, 1):
            # Get tags for this memory
            cursor.execute("SELECT tag FROM tags WHERE memory_id = ?", (mem_id,))
            mem_tags = [t[0] for t in cursor.fetchall()]

            memories_text.append(
                f"[{idx}] Memory ID: {mem_id}\n"
                f"    Summary: {summary}\n"
                f"    Importance: {importance}/10 | Accessed: {access_count} times\n"
                f"    Tags: {', '.join(mem_tags) if mem_tags else 'none'}\n"
                f"    Content: {content[:200]}{'...' if len(content) > 200 else ''}\n"
            )

        conn.close()

        return Response(
            message=f"🧠 Recalled {len(results)} memories:\n\n" + "\n".join(memories_text),
            break_loop=False
        )

    async def _search_memories(self) -> Response:
        """Full-text search in memories"""
        query = self.args.get("query", "")
        limit = self.args.get("limit", 10)

        if not query:
            return Response(message="Search query required", break_loop=False)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Full-text search
        cursor.execute("""
            SELECT m.id, m.content, m.summary, m.importance, m.created_at
            FROM memories m
            JOIN memories_fts fts ON m.id = fts.rowid
            WHERE memories_fts MATCH ?
            ORDER BY rank, m.importance DESC
            LIMIT ?
        """, (query, limit))

        results = cursor.fetchall()
        conn.close()

        if not results:
            return Response(
                message=f"No memories found matching: {query}",
                break_loop=False
            )

        # Format results
        search_results = []
        for idx, (mem_id, content, summary, importance, created) in enumerate(results, 1):
            search_results.append(
                f"[{idx}] ID: {mem_id} | Importance: {importance}/10\n"
                f"    {summary}\n"
                f"    {content[:150]}...\n"
            )

        return Response(
            message=f"🔍 Found {len(results)} memories for '{query}':\n\n" + "\n".join(search_results),
            break_loop=False
        )

    async def _update_memory(self) -> Response:
        """Update existing memory"""
        memory_id = self.args.get("memory_id")
        updates = {}

        if "content" in self.args:
            updates["content"] = self.args["content"]
        if "summary" in self.args:
            updates["summary"] = self.args["summary"]
        if "importance" in self.args:
            updates["importance"] = self.args["importance"]

        if not memory_id or not updates:
            return Response(
                message="memory_id and at least one field to update required",
                break_loop=False
            )

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Build update query
        set_clause = ", ".join(f"{k} = ?" for k in updates.keys())
        values = list(updates.values()) + [memory_id]

        cursor.execute(f"""
            UPDATE memories SET {set_clause} WHERE id = ?
        """, values)

        conn.commit()
        updated = cursor.rowcount
        conn.close()

        if updated:
            return Response(
                message=f"✓ Memory {memory_id} updated",
                break_loop=False
            )
        else:
            return Response(
                message=f"✗ Memory {memory_id} not found",
                break_loop=False
            )

    async def _delete_memory(self) -> Response:
        """Delete memory"""
        memory_id = self.args.get("memory_id")

        if not memory_id:
            return Response(message="memory_id required", break_loop=False)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM memories WHERE id = ?", (memory_id,))
        conn.commit()
        deleted = cursor.rowcount
        conn.close()

        if deleted:
            return Response(
                message=f"✓ Memory {memory_id} deleted",
                break_loop=False
            )
        else:
            return Response(
                message=f"✗ Memory {memory_id} not found",
                break_loop=False
            )

    async def _list_memories(self) -> Response:
        """List recent memories"""
        limit = self.args.get("limit", 20)
        tag = self.args.get("tag")

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if tag:
            cursor.execute("""
                SELECT m.id, m.summary, m.importance, m.created_at, m.access_count
                FROM memories m
                JOIN tags t ON m.id = t.memory_id
                WHERE t.tag = ?
                ORDER BY m.created_at DESC
                LIMIT ?
            """, (tag.lower(), limit))
        else:
            cursor.execute("""
                SELECT id, summary, importance, created_at, access_count
                FROM memories
                ORDER BY created_at DESC
                LIMIT ?
            """, (limit,))

        results = cursor.fetchall()
        conn.close()

        if not results:
            return Response(message="No memories found", break_loop=False)

        # Format list
        memory_list = []
        for mem_id, summary, importance, created, access_count in results:
            memory_list.append(
                f"• ID {mem_id} [{importance}/10] - {summary[:80]}\n"
                f"  Created: {created} | Accessed: {access_count} times"
            )

        return Response(
            message=f"📝 {len(results)} memories:\n\n" + "\n\n".join(memory_list),
            break_loop=False
        )

    async def _get_stats(self) -> Response:
        """Get memory database statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Total memories
        cursor.execute("SELECT COUNT(*) FROM memories")
        total = cursor.fetchone()[0]

        # Total tags
        cursor.execute("SELECT COUNT(DISTINCT tag) FROM tags")
        total_tags = cursor.fetchone()[0]

        # Most used tags
        cursor.execute("""
            SELECT tag, COUNT(*) as count
            FROM tags
            GROUP BY tag
            ORDER BY count DESC
            LIMIT 10
        """)
        top_tags = cursor.fetchall()

        # Importance distribution
        cursor.execute("""
            SELECT importance, COUNT(*) as count
            FROM memories
            GROUP BY importance
            ORDER BY importance DESC
        """)
        importance_dist = cursor.fetchall()

        # Most accessed
        cursor.execute("""
            SELECT id, summary, access_count
            FROM memories
            ORDER BY access_count DESC
            LIMIT 5
        """)
        most_accessed = cursor.fetchall()

        conn.close()

        # Format stats
        stats_text = f"""
📊 Memory Database Statistics

Total Memories: {total}
Total Tags: {total_tags}

Top Tags:
{chr(10).join(f"  • {tag}: {count}" for tag, count in top_tags[:5])}

Importance Distribution:
{chr(10).join(f"  Level {imp}: {count} memories" for imp, count in importance_dist)}

Most Accessed:
{chr(10).join(f"  • ID {mid}: {summary[:50]} ({count} times)" for mid, summary, count in most_accessed)}
"""

        return Response(message=stats_text.strip(), break_loop=False)

    async def _summarize_memories(self) -> Response:
        """Create summary of all memories (for context)"""
        tag = self.args.get("tag")
        min_importance = self.args.get("min_importance", 7)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if tag:
            cursor.execute("""
                SELECT m.summary, m.importance
                FROM memories m
                JOIN tags t ON m.id = t.memory_id
                WHERE t.tag = ? AND m.importance >= ?
                ORDER BY m.importance DESC
            """, (tag.lower(), min_importance))
        else:
            cursor.execute("""
                SELECT summary, importance
                FROM memories
                WHERE importance >= ?
                ORDER BY importance DESC
                LIMIT 50
            """, (min_importance,))

        results = cursor.fetchall()
        conn.close()

        if not results:
            return Response(
                message="No high-importance memories to summarize",
                break_loop=False
            )

        # Create summary
        summaries = [f"[{imp}/10] {summary}" for summary, imp in results]

        return Response(
            message=f"📚 Memory Summary ({len(results)} items):\n\n" + "\n".join(summaries),
            break_loop=False
        )
