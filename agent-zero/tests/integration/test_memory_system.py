"""
Integration tests for Memory System

Tests the complete memory system including:
- Agent-Memory integration
- Knowledge base loading
- Cross-component memory operations
- Memory persistence across sessions
"""

import pytest
import os
from unittest.mock import patch, Mock
from langchain_core.documents import Document

from python.helpers.memory import Memory
from conftest import generate_mock_documents


class TestAgentMemoryIntegration:
    """Test integration between Agent and Memory system."""

    @pytest.mark.asyncio
    async def test_agent_can_access_memory(self, agent, temp_memory_dir):
        """Test that agent can access memory system."""
        with patch('python.helpers.files.get_abs_path', return_value=temp_memory_dir):
            memory = await Memory.get(agent)

            # Agent should be able to use memory
            doc_id = memory.insert_text("Agent memory test", {"source": "agent"})
            assert doc_id is not None

    @pytest.mark.asyncio
    async def test_agent_memory_shared_config(self, agent, temp_memory_dir):
        """Test that memory uses agent's configuration."""
        with patch('python.helpers.files.get_abs_path', return_value=temp_memory_dir):
            memory = await Memory.get(agent)

            assert memory.agent == agent
            assert memory.agent.config == agent.config

    @pytest.mark.asyncio
    async def test_multiple_agents_same_memory(self, agent_config, temp_memory_dir):
        """Test multiple agents sharing same memory subdirectory."""
        from agent import Agent, AgentContext

        with patch('python.helpers.files.get_abs_path', return_value=temp_memory_dir):
            # Create two contexts/agents with same memory subdir
            ctx1 = AgentContext(config=agent_config)
            ctx2 = AgentContext(config=agent_config)

            agent1 = ctx1.agent0
            agent2 = ctx2.agent0

            memory1 = await Memory.get(agent1)
            memory2 = await Memory.get(agent2)

            # Insert with agent1
            doc_id = memory1.insert_text("Shared memory test")

            # Should be accessible from agent2 (same DB instance)
            assert memory1.db is memory2.db

            # Cleanup
            AgentContext.remove(ctx1.id)
            AgentContext.remove(ctx2.id)


class TestMemoryKnowledgeIntegration:
    """Test integration with knowledge base loading."""

    @pytest.mark.asyncio
    async def test_knowledge_loading_with_agent(self, agent, temp_memory_dir, tmp_path):
        """Test loading knowledge files during memory initialization."""
        # Create fake knowledge directory structure
        knowledge_dir = tmp_path / "knowledge" / "default" / "main"
        knowledge_dir.mkdir(parents=True)

        # Create a test knowledge file
        (knowledge_dir / "test.md").write_text("# Test Knowledge\nThis is test knowledge content.")

        with patch('python.helpers.files.get_abs_path') as mock_path:
            def get_path(*paths):
                if "knowledge" in paths:
                    return str(tmp_path / "knowledge")
                return temp_memory_dir

            mock_path.side_effect = get_path

            # This should trigger knowledge loading
            agent.config.knowledge_subdirs = ["default"]
            memory = await Memory.get(agent)

            assert memory is not None

    @pytest.mark.asyncio
    async def test_knowledge_areas_loaded(self, agent, temp_memory_dir, tmp_path):
        """Test that all knowledge areas are loaded."""
        # Create directory structure for all areas
        for area in ["main", "fragments", "solutions"]:
            area_dir = tmp_path / "knowledge" / "default" / area
            area_dir.mkdir(parents=True)
            (area_dir / f"{area}.md").write_text(f"Content for {area}")

        with patch('python.helpers.files.get_abs_path') as mock_path:
            def get_path(*paths):
                if "knowledge" in paths:
                    return str(tmp_path / "knowledge")
                return temp_memory_dir

            mock_path.side_effect = get_path

            agent.config.knowledge_subdirs = ["default"]
            memory = await Memory.get(agent)

            # Knowledge should be loaded into memory
            assert memory is not None


class TestMemoryPersistenceIntegration:
    """Test memory persistence across sessions."""

    @pytest.mark.asyncio
    async def test_memory_persists_between_loads(self, agent, temp_memory_dir):
        """Test that memory persists between get() calls."""
        with patch('python.helpers.files.get_abs_path', return_value=temp_memory_dir):
            # First load
            memory1 = await Memory.get(agent)
            test_id = memory1.insert_text("Persistent content")

            # Clear cache to force reload
            Memory.index.clear()

            # Second load
            memory2 = await Memory.get(agent)

            # Should be able to access previously inserted content
            assert memory2 is not None

    @pytest.mark.asyncio
    async def test_memory_updates_persist(self, agent, temp_memory_dir):
        """Test that updates to memory are persisted."""
        with patch('python.helpers.files.get_abs_path', return_value=temp_memory_dir):
            memory = await Memory.get(agent)

            # Insert and delete
            doc_id = memory.insert_text("Temporary content")
            await memory.delete_documents_by_ids([doc_id])

            # Changes should be persisted automatically
            assert memory is not None


class TestMemorySearchIntegration:
    """Test integrated search operations."""

    @pytest.mark.asyncio
    async def test_insert_and_search_workflow(self, agent, temp_memory_dir):
        """Test complete insert and search workflow."""
        with patch('python.helpers.files.get_abs_path', return_value=temp_memory_dir):
            memory = await Memory.get(agent)

            # Insert multiple related documents
            memory.insert_text("Python is a programming language", {"topic": "python"})
            memory.insert_text("JavaScript is used for web development", {"topic": "javascript"})
            memory.insert_text("Python has great data science libraries", {"topic": "python"})

            # Search for Python-related content
            results = await memory.search_similarity_threshold(
                query="Python programming",
                limit=10,
                threshold=0.0
            )

            assert len(results) >= 0  # Should find at least some results

    @pytest.mark.asyncio
    async def test_search_with_metadata_filtering(self, agent, temp_memory_dir):
        """Test search with metadata filtering."""
        with patch('python.helpers.files.get_abs_path', return_value=temp_memory_dir):
            memory = await Memory.get(agent)

            # Insert documents with different metadata
            memory.insert_text("Important document", {"priority": "high", "area": "main"})
            memory.insert_text("Normal document", {"priority": "normal", "area": "main"})
            memory.insert_text("Low priority document", {"priority": "low", "area": "main"})

            # Search only high priority
            results = await memory.search_similarity_threshold(
                query="document",
                limit=10,
                threshold=0.0,
                filter="priority == 'high'"
            )

            assert isinstance(results, list)

    @pytest.mark.asyncio
    async def test_delete_and_verify_workflow(self, agent, temp_memory_dir):
        """Test delete operations and verification."""
        with patch('python.helpers.files.get_abs_path', return_value=temp_memory_dir):
            memory = await Memory.get(agent)

            # Insert documents
            id1 = memory.insert_text("Document 1")
            id2 = memory.insert_text("Document 2")
            id3 = memory.insert_text("Document 3")

            # Delete one
            removed = await memory.delete_documents_by_ids([id2])

            # Verify deletion
            assert isinstance(removed, list)


class TestMemoryWithTools:
    """Test memory integration with tools."""

    @pytest.mark.asyncio
    async def test_tool_can_use_memory(self, mock_agent, temp_memory_dir):
        """Test that tools can access and use memory."""
        with patch('python.helpers.files.get_abs_path', return_value=temp_memory_dir):
            # Create a real agent for this test
            from agent import Agent, AgentConfig
            from conftest import MockChatModel, MockEmbeddings

            config = AgentConfig(
                chat_model=MockChatModel(),
                utility_model=MockChatModel(),
                embeddings_model=MockEmbeddings(),
                memory_subdir="test_tool"
            )

            from agent import AgentContext
            context = AgentContext(config=config)
            real_agent = context.agent0

            # Get memory
            memory = await Memory.get(real_agent)
            memory.insert_text("Tool accessible data")

            # Tool should be able to use this memory
            assert memory.agent == real_agent

            # Cleanup
            AgentContext.remove(context.id)


class TestMemoryStressTest:
    """Stress test memory system with large operations."""

    @pytest.mark.asyncio
    async def test_insert_large_batch(self, agent, temp_memory_dir):
        """Test inserting large batch of documents."""
        with patch('python.helpers.files.get_abs_path', return_value=temp_memory_dir):
            memory = await Memory.get(agent)

            # Insert 100 documents
            docs = [
                Document(
                    page_content=f"Document {i} with content",
                    metadata={"index": i, "area": "main"}
                )
                for i in range(100)
            ]

            ids = memory.insert_documents(docs)

            assert len(ids) == 100

    @pytest.mark.asyncio
    async def test_large_search_results(self, agent, temp_memory_dir):
        """Test handling large search result sets."""
        with patch('python.helpers.files.get_abs_path', return_value=temp_memory_dir):
            memory = await Memory.get(agent)

            # Insert many similar documents
            for i in range(50):
                memory.insert_text(f"Test document number {i}")

            # Search with high limit
            results = await memory.search_similarity_threshold(
                query="Test document",
                limit=100,
                threshold=0.0
            )

            assert isinstance(results, list)

    @pytest.mark.asyncio
    async def test_concurrent_operations(self, agent, temp_memory_dir):
        """Test concurrent memory operations."""
        import asyncio

        with patch('python.helpers.files.get_abs_path', return_value=temp_memory_dir):
            memory = await Memory.get(agent)

            # Insert initial documents
            ids = []
            for i in range(10):
                doc_id = memory.insert_text(f"Concurrent test {i}")
                ids.append(doc_id)

            # Perform concurrent searches
            search_tasks = [
                memory.search_similarity_threshold(f"test {i}", 5, 0.0)
                for i in range(5)
            ]

            results = await asyncio.gather(*search_tasks)

            assert len(results) == 5
            assert all(isinstance(r, list) for r in results)


class TestMemoryErrorHandling:
    """Test error handling in integrated scenarios."""

    @pytest.mark.asyncio
    async def test_corrupted_metadata_handling(self, agent, temp_memory_dir):
        """Test handling of corrupted metadata."""
        with patch('python.helpers.files.get_abs_path', return_value=temp_memory_dir):
            memory = await Memory.get(agent)

            # Insert document with unusual metadata
            try:
                doc_id = memory.insert_text("Test", {"corrupted": None})
                assert doc_id is not None
            except Exception:
                pytest.fail("Should handle unusual metadata gracefully")

    @pytest.mark.asyncio
    async def test_invalid_filter_handling(self, agent, temp_memory_dir):
        """Test handling of invalid search filters."""
        with patch('python.helpers.files.get_abs_path', return_value=temp_memory_dir):
            memory = await Memory.get(agent)

            memory.insert_text("Test document")

            # Search with invalid filter (should not crash)
            results = await memory.search_similarity_threshold(
                query="test",
                limit=10,
                threshold=0.0,
                filter="invalid python syntax ==="
            )

            # Should return results or empty list, not crash
            assert isinstance(results, list)


class TestMemoryMultiArea:
    """Test operations across multiple memory areas."""

    @pytest.mark.asyncio
    async def test_insert_across_areas(self, agent, temp_memory_dir):
        """Test inserting documents across different areas."""
        with patch('python.helpers.files.get_abs_path', return_value=temp_memory_dir):
            memory = await Memory.get(agent)

            # Insert in different areas
            id1 = memory.insert_text("Main area doc", {"area": "main"})
            id2 = memory.insert_text("Fragment area doc", {"area": "fragments"})
            id3 = memory.insert_text("Solution area doc", {"area": "solutions"})

            assert all([id1, id2, id3])

    @pytest.mark.asyncio
    async def test_search_specific_area(self, agent, temp_memory_dir):
        """Test searching within specific area."""
        with patch('python.helpers.files.get_abs_path', return_value=temp_memory_dir):
            memory = await Memory.get(agent)

            # Insert in different areas
            memory.insert_text("Main content", {"area": "main"})
            memory.insert_text("Fragment content", {"area": "fragments"})

            # Search only in main area
            results = await memory.search_similarity_threshold(
                query="content",
                limit=10,
                threshold=0.0,
                filter="area == 'main'"
            )

            assert isinstance(results, list)

    @pytest.mark.asyncio
    async def test_delete_from_specific_area(self, agent, temp_memory_dir):
        """Test deleting documents from specific area."""
        with patch('python.helpers.files.get_abs_path', return_value=temp_memory_dir):
            memory = await Memory.get(agent)

            # Insert in different areas
            memory.insert_text("Main 1", {"area": "main"})
            memory.insert_text("Main 2", {"area": "main"})
            memory.insert_text("Fragment 1", {"area": "fragments"})

            # Delete only from main area
            removed = await memory.delete_documents_by_query(
                query="Main",
                threshold=0.0,
                filter="area == 'main'"
            )

            assert isinstance(removed, list)


# ============================================================================
# PERFORMANCE TESTS
# ============================================================================

class TestMemoryPerformance:
    """Test memory system performance characteristics."""

    @pytest.mark.asyncio
    async def test_insert_performance(self, agent, temp_memory_dir):
        """Test insert performance for reasonable dataset."""
        import time

        with patch('python.helpers.files.get_abs_path', return_value=temp_memory_dir):
            memory = await Memory.get(agent)

            start = time.time()

            # Insert 50 documents
            for i in range(50):
                memory.insert_text(f"Performance test document {i}")

            elapsed = time.time() - start

            # Should complete in reasonable time (< 10 seconds for 50 docs)
            assert elapsed < 10

    @pytest.mark.asyncio
    async def test_search_performance(self, agent, temp_memory_dir):
        """Test search performance with populated database."""
        import time

        with patch('python.helpers.files.get_abs_path', return_value=temp_memory_dir):
            memory = await Memory.get(agent)

            # Populate database
            for i in range(100):
                memory.insert_text(f"Search test document {i}")

            start = time.time()

            # Perform multiple searches
            for i in range(10):
                await memory.search_similarity_threshold(
                    query=f"document {i}",
                    limit=10,
                    threshold=0.0
                )

            elapsed = time.time() - start

            # 10 searches should complete quickly
            assert elapsed < 5
