import json
from python.helpers.tool import Tool, Response
from python.helpers.print_style import PrintStyle

class VectorMemory(Tool):
    """
    Enhanced memory tool using vector similarity search
    Allows semantic search through past conversations and learnings
    """

    async def execute(self, **kwargs):
        self.agent.set_data("timeout", 60)

        operation = kwargs.get("operation", "search")

        if operation == "store":
            return await self._store_memory(kwargs)
        elif operation == "search":
            return await self._search_memory(kwargs)
        elif operation == "stats":
            return await self._get_stats()
        else:
            return Response(
                message=f"Unknown operation: {operation}. Use 'store', 'search', or 'stats'.",
                break_loop=False
            )

    async def _store_memory(self, kwargs):
        """Store a new memory"""
        content = kwargs.get("content", "")
        memory_type = kwargs.get("memory_type", "general")

        if not content:
            return Response(
                message="Error: No content provided to store",
                break_loop=False
            )

        try:
            from python.helpers.vector_memory import get_memory
            memory = get_memory()

            metadata = {
                "context": kwargs.get("context", ""),
                "importance": kwargs.get("importance", "normal")
            }

            memory_id = memory.add_memory(
                content=content,
                memory_type=memory_type,
                agent_name=self.agent.agent_name,
                metadata=metadata
            )

            message = f"✅ Memory stored successfully (ID: {memory_id})\n"
            message += f"Type: {memory_type}\n"
            message += f"Content: {content[:100]}..."

            PrintStyle(font_color="green").print(message)
            self.agent.context.log.log(type="memory", heading="Memory Stored", content=message)

            return Response(message=message, break_loop=False)

        except ImportError:
            error_msg = "Vector memory not available. Install: pip install sentence-transformers"
            PrintStyle(font_color="red").print(error_msg)
            return Response(message=error_msg, break_loop=False)
        except Exception as e:
            error_msg = f"Error storing memory: {str(e)}"
            PrintStyle(font_color="red").print(error_msg)
            return Response(message=error_msg, break_loop=False)

    async def _search_memory(self, kwargs):
        """Search for relevant memories"""
        query = kwargs.get("query", "")
        top_k = int(kwargs.get("top_k", 5))
        memory_type = kwargs.get("memory_type", None)
        threshold = float(kwargs.get("threshold", 0.3))

        if not query:
            return Response(
                message="Error: No search query provided",
                break_loop=False
            )

        try:
            from python.helpers.vector_memory import get_memory
            memory = get_memory()

            results = memory.search(
                query=query,
                top_k=top_k,
                memory_type=memory_type,
                similarity_threshold=threshold
            )

            if not results:
                message = f"No relevant memories found for query: '{query}'"
                PrintStyle(font_color="yellow").print(message)
                return Response(message=message, break_loop=False)

            # Format results
            message = f"🔍 Found {len(results)} relevant memories:\n\n"
            for i, result in enumerate(results, 1):
                message += f"{i}. [{result['memory_type']}] (similarity: {result['similarity']:.2f})\n"
                message += f"   {result['content']}\n"
                message += f"   Stored by: {result['agent_name']} at {result['timestamp']}\n\n"

            PrintStyle(font_color="cyan").print(message)
            self.agent.context.log.log(type="memory", heading="Memory Search Results", content=message)

            return Response(message=message, break_loop=False)

        except ImportError:
            error_msg = "Vector memory not available. Install: pip install sentence-transformers"
            PrintStyle(font_color="red").print(error_msg)
            return Response(message=error_msg, break_loop=False)
        except Exception as e:
            error_msg = f"Error searching memory: {str(e)}"
            PrintStyle(font_color="red").print(error_msg)
            return Response(message=error_msg, break_loop=False)

    async def _get_stats(self):
        """Get memory statistics"""
        try:
            from python.helpers.vector_memory import get_memory
            memory = get_memory()

            stats = memory.get_memory_stats()

            message = "📊 Vector Memory Statistics:\n\n"
            message += f"Total memories: {stats['total_memories']}\n"
            message += f"Database size: {stats['database_size_mb']} MB\n\n"
            message += "Memories by type:\n"
            for mem_type, count in stats['by_type'].items():
                message += f"  - {mem_type}: {count}\n"

            PrintStyle(font_color="cyan").print(message)
            self.agent.context.log.log(type="memory", heading="Memory Stats", content=message)

            return Response(message=message, break_loop=False)

        except ImportError:
            error_msg = "Vector memory not available. Install: pip install sentence-transformers"
            PrintStyle(font_color="red").print(error_msg)
            return Response(message=error_msg, break_loop=False)
        except Exception as e:
            error_msg = f"Error getting stats: {str(e)}"
            PrintStyle(font_color="red").print(error_msg)
            return Response(message=error_msg, break_loop=False)
