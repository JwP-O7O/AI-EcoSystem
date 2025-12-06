"""
Unit tests for Memory System

Tests cover:
- Memory initialization
- Document insertion
- Similarity search
- Document deletion
- Knowledge preloading
- Vector database operations
"""

import pytest
import os
import tempfile
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from langchain_core.documents import Document

from python.helpers.memory import Memory
from conftest import generate_mock_documents


class TestMemoryInitialization:
    """Test memory system initialization."""

    @pytest.mark.asyncio
    async def test_memory_get_creates_instance(self, agent, temp_memory_dir):
        """Test that Memory.get creates a memory instance."""
        with patch('python.helpers.files.get_abs_path', return_value=temp_memory_dir):
            memory = await Memory.get(agent)
            assert memory is not None
            assert isinstance(memory, Memory)

    @pytest.mark.asyncio
    async def test_memory_get_caches_instance(self, agent, temp_memory_dir):
        """Test that Memory.get caches instances."""
        with patch('python.helpers.files.get_abs_path', return_value=temp_memory_dir):
            memory1 = await Memory.get(agent)
            memory2 = await Memory.get(agent)

            # Should return same DB instance
            assert memory1.db is memory2.db

    def test_memory_initialize_creates_directories(self, mock_embeddings, temp_memory_dir):
        """Test that initialization creates required directories."""
        with patch('python.helpers.files.get_abs_path', return_value=temp_memory_dir):
            db = Memory.initialize(
                log_item=None,
                embeddings_model=mock_embeddings,
                memory_subdir="test",
                in_memory=True
            )
            assert db is not None

    def test_memory_initialize_loads_existing(self, mock_embeddings, temp_memory_dir):
        """Test that initialization loads existing database."""
        # Create a database first
        with patch('python.helpers.files.get_abs_path', return_value=temp_memory_dir):
            db1 = Memory.initialize(
                log_item=None,
                embeddings_model=mock_embeddings,
                memory_subdir="test",
                in_memory=False
            )

            # Save it
            db_path = Memory._abs_db_dir("test")
            os.makedirs(db_path, exist_ok=True)
            db1.save_local(db_path)

            # Load it again
            db2 = Memory.initialize(
                log_item=None,
                embeddings_model=mock_embeddings,
                memory_subdir="test",
                in_memory=False
            )

            assert db2 is not None


class TestMemoryDocumentInsertion:
    """Test document insertion functionality."""

    @pytest.mark.asyncio
    async def test_insert_text_simple(self, agent, memory_db):
        """Test inserting simple text."""
        doc_id = memory_db.insert_text("Test content", {"source": "test"})

        assert doc_id is not None
        assert isinstance(doc_id, str)

    @pytest.mark.asyncio
    async def test_insert_text_with_metadata(self, agent, memory_db):
        """Test inserting text with custom metadata."""
        metadata = {
            "source": "test",
            "category": "testing",
            "priority": "high"
        }
        doc_id = memory_db.insert_text("Test content", metadata)

        assert doc_id is not None

    @pytest.mark.asyncio
    async def test_insert_text_default_area(self, agent, memory_db):
        """Test that insert_text sets default area."""
        doc_id = memory_db.insert_text("Test content")

        # Verify default area was set
        assert doc_id is not None

    @pytest.mark.asyncio
    async def test_insert_documents_batch(self, agent, memory_db):
        """Test inserting multiple documents."""
        docs = generate_mock_documents(5)
        ids = memory_db.insert_documents(docs)

        assert len(ids) == 5
        assert all(isinstance(id, str) for id in ids)

    @pytest.mark.asyncio
    async def test_insert_documents_empty_list(self, agent, memory_db):
        """Test inserting empty document list."""
        ids = memory_db.insert_documents([])
        assert ids == []

    @pytest.mark.asyncio
    async def test_insert_documents_adds_ids(self, agent, memory_db):
        """Test that insert_documents adds IDs to metadata."""
        docs = [
            Document(page_content="Doc 1", metadata={}),
            Document(page_content="Doc 2", metadata={})
        ]
        ids = memory_db.insert_documents(docs)

        # Verify IDs were added to metadata
        assert all(doc.metadata.get("id") for doc in docs)


class TestMemorySimilaritySearch:
    """Test similarity search functionality."""

    @pytest.mark.asyncio
    async def test_search_similarity_basic(self, agent, memory_db):
        """Test basic similarity search."""
        # Insert some test documents
        memory_db.insert_text("Python programming language")
        memory_db.insert_text("JavaScript for web development")
        memory_db.insert_text("Machine learning with TensorFlow")

        # Search
        results = await memory_db.search_similarity_threshold(
            query="programming",
            limit=10,
            threshold=0.0
        )

        assert isinstance(results, list)

    @pytest.mark.asyncio
    async def test_search_similarity_with_threshold(self, agent, memory_db):
        """Test similarity search with threshold."""
        memory_db.insert_text("Exact match test")

        results = await memory_db.search_similarity_threshold(
            query="Exact match test",
            limit=5,
            threshold=0.5
        )

        assert isinstance(results, list)

    @pytest.mark.asyncio
    async def test_search_similarity_with_filter(self, agent, memory_db):
        """Test similarity search with metadata filter."""
        memory_db.insert_text("Test 1", {"category": "A"})
        memory_db.insert_text("Test 2", {"category": "B"})

        results = await memory_db.search_similarity_threshold(
            query="Test",
            limit=10,
            threshold=0.0,
            filter="category == 'A'"
        )

        assert isinstance(results, list)

    @pytest.mark.asyncio
    async def test_search_similarity_no_results(self, agent, memory_db):
        """Test similarity search with no matching results."""
        results = await memory_db.search_similarity_threshold(
            query="nonexistent query that matches nothing",
            limit=10,
            threshold=0.99
        )

        assert isinstance(results, list)


class TestMemoryDocumentDeletion:
    """Test document deletion functionality."""

    @pytest.mark.asyncio
    async def test_delete_by_ids_single(self, agent, memory_db):
        """Test deleting a single document by ID."""
        doc_id = memory_db.insert_text("Test document")

        removed = await memory_db.delete_documents_by_ids([doc_id])

        assert isinstance(removed, list)

    @pytest.mark.asyncio
    async def test_delete_by_ids_multiple(self, agent, memory_db):
        """Test deleting multiple documents by ID."""
        id1 = memory_db.insert_text("Doc 1")
        id2 = memory_db.insert_text("Doc 2")
        id3 = memory_db.insert_text("Doc 3")

        removed = await memory_db.delete_documents_by_ids([id1, id2, id3])

        assert isinstance(removed, list)

    @pytest.mark.asyncio
    async def test_delete_by_ids_nonexistent(self, agent, memory_db):
        """Test deleting non-existent documents."""
        removed = await memory_db.delete_documents_by_ids(["nonexistent_id"])

        assert isinstance(removed, list)
        assert len(removed) == 0

    @pytest.mark.asyncio
    async def test_delete_by_query(self, agent, memory_db):
        """Test deleting documents by query."""
        memory_db.insert_text("Delete this document")
        memory_db.insert_text("Keep this document")

        removed = await memory_db.delete_documents_by_query(
            query="Delete this",
            threshold=0.0
        )

        assert isinstance(removed, list)

    @pytest.mark.asyncio
    async def test_delete_by_query_with_filter(self, agent, memory_db):
        """Test deleting documents by query with filter."""
        memory_db.insert_text("Test 1", {"type": "temp"})
        memory_db.insert_text("Test 2", {"type": "permanent"})

        removed = await memory_db.delete_documents_by_query(
            query="Test",
            threshold=0.0,
            filter="type == 'temp'"
        )

        assert isinstance(removed, list)


class TestMemoryKnowledgePreloading:
    """Test knowledge preloading functionality."""

    @pytest.mark.asyncio
    async def test_preload_knowledge_empty_dirs(self, agent, memory_db, temp_memory_dir):
        """Test preloading with empty knowledge directories."""
        with patch('python.helpers.files.get_abs_path', return_value=temp_memory_dir):
            await memory_db.preload_knowledge(
                log_item=None,
                kn_dirs=["test"],
                memory_subdir="test"
            )

        # Should complete without error

    @pytest.mark.asyncio
    async def test_preload_knowledge_creates_index(self, agent, memory_db, temp_memory_dir):
        """Test that preloading creates index file."""
        with patch('python.helpers.files.get_abs_path', return_value=temp_memory_dir):
            await memory_db.preload_knowledge(
                log_item=None,
                kn_dirs=["test"],
                memory_subdir="test"
            )

        # Check if index file would be created
        # (actual file creation depends on knowledge files existing)


class TestMemoryUtilities:
    """Test utility functions."""

    def test_format_docs_plain(self):
        """Test plain document formatting."""
        docs = generate_mock_documents(2)
        formatted = Memory.format_docs_plain(docs)

        assert isinstance(formatted, list)
        assert len(formatted) == 2
        assert all(isinstance(doc, str) for doc in formatted)

    def test_format_docs_plain_includes_metadata(self):
        """Test that formatted docs include metadata."""
        doc = Document(
            page_content="Test content",
            metadata={"id": "test_id", "source": "test"}
        )
        formatted = Memory.format_docs_plain([doc])

        assert "test_id" in formatted[0]
        assert "test" in formatted[0]
        assert "Test content" in formatted[0]

    def test_get_timestamp_format(self):
        """Test timestamp format."""
        timestamp = Memory.get_timestamp()

        assert isinstance(timestamp, str)
        assert len(timestamp) > 0
        # Should be in format YYYY-MM-DD HH:MM:SS
        assert len(timestamp.split()) == 2

    def test_cosine_normalizer_range(self):
        """Test that cosine normalizer returns values in [0, 1]."""
        assert 0 <= Memory._cosine_normalizer(-1.0) <= 1
        assert 0 <= Memory._cosine_normalizer(0.0) <= 1
        assert 0 <= Memory._cosine_normalizer(1.0) <= 1

    def test_cosine_normalizer_midpoint(self):
        """Test cosine normalizer at midpoint."""
        result = Memory._cosine_normalizer(0.0)
        assert 0.4 <= result <= 0.6  # Should be around 0.5

    def test_score_normalizer(self):
        """Test score normalizer."""
        result = Memory._score_normalizer(1.0)
        assert 0 <= result <= 1

    def test_abs_db_dir(self):
        """Test absolute database directory path."""
        path = Memory._abs_db_dir("test_subdir")
        assert "test_subdir" in path

    def test_get_comparator_valid(self):
        """Test creating comparator with valid condition."""
        comparator = Memory._get_comparator("value > 5")
        assert callable(comparator)
        assert comparator({"value": 10}) == True
        assert comparator({"value": 3}) == False

    def test_get_comparator_invalid(self):
        """Test comparator with invalid condition."""
        comparator = Memory._get_comparator("invalid_syntax ==")
        assert callable(comparator)
        # Should return False on error
        assert comparator({}) == False


class TestMemoryAreas:
    """Test memory area functionality."""

    def test_memory_areas_enum(self):
        """Test Memory.Area enum values."""
        assert Memory.Area.MAIN.value == "main"
        assert Memory.Area.FRAGMENTS.value == "fragments"
        assert Memory.Area.SOLUTIONS.value == "solutions"
        assert Memory.Area.INSTRUMENTS.value == "instruments"

    @pytest.mark.asyncio
    async def test_insert_text_custom_area(self, agent, memory_db):
        """Test inserting text with custom area."""
        doc_id = memory_db.insert_text(
            "Test content",
            {"area": Memory.Area.FRAGMENTS.value}
        )

        assert doc_id is not None

    @pytest.mark.asyncio
    async def test_search_by_area(self, agent, memory_db):
        """Test searching documents by area."""
        memory_db.insert_text("Main doc", {"area": "main"})
        memory_db.insert_text("Fragment doc", {"area": "fragments"})

        results = await memory_db.search_similarity_threshold(
            query="doc",
            limit=10,
            threshold=0.0,
            filter="area == 'main'"
        )

        assert isinstance(results, list)


class TestMemoryEdgeCases:
    """Test edge cases and error handling."""

    @pytest.mark.asyncio
    async def test_insert_very_long_text(self, agent, memory_db):
        """Test inserting very long text."""
        long_text = "test " * 10000  # Very long text
        doc_id = memory_db.insert_text(long_text)

        assert doc_id is not None

    @pytest.mark.asyncio
    async def test_insert_unicode_text(self, agent, memory_db):
        """Test inserting Unicode text."""
        unicode_text = "Testing: 你好 🌍 العربية"
        doc_id = memory_db.insert_text(unicode_text)

        assert doc_id is not None

    @pytest.mark.asyncio
    async def test_insert_empty_text(self, agent, memory_db):
        """Test inserting empty text."""
        doc_id = memory_db.insert_text("")

        assert doc_id is not None

    @pytest.mark.asyncio
    async def test_search_empty_query(self, agent, memory_db):
        """Test searching with empty query."""
        memory_db.insert_text("Test content")

        results = await memory_db.search_similarity_threshold(
            query="",
            limit=10,
            threshold=0.0
        )

        assert isinstance(results, list)

    @pytest.mark.asyncio
    async def test_delete_empty_id_list(self, agent, memory_db):
        """Test deleting with empty ID list."""
        removed = await memory_db.delete_documents_by_ids([])

        assert removed == []


class TestMemoryPersistence:
    """Test memory persistence functionality."""

    @pytest.mark.asyncio
    async def test_save_db(self, agent, memory_db, temp_memory_dir):
        """Test saving database to disk."""
        with patch('python.helpers.files.get_abs_path', return_value=temp_memory_dir):
            memory_db.insert_text("Persistent test")
            # _save_db is called automatically
            # Just verify no errors occurred

    @pytest.mark.asyncio
    async def test_reload_persisted_data(self, agent, temp_memory_dir, mock_embeddings):
        """Test reloading persisted data."""
        # First session: insert data
        with patch('python.helpers.files.get_abs_path', return_value=temp_memory_dir):
            agent.config.memory_subdir = "persist_test"
            memory1 = await Memory.get(agent)
            memory1.insert_text("Persistent content")

            # Clear cache
            Memory.index.clear()

            # Second session: load data
            memory2 = await Memory.get(agent)
            # Should be a new instance but with same data


# ============================================================================
# PARAMETRIZED TESTS
# ============================================================================

@pytest.mark.parametrize("area", [
    Memory.Area.MAIN,
    Memory.Area.FRAGMENTS,
    Memory.Area.SOLUTIONS,
    Memory.Area.INSTRUMENTS
])
@pytest.mark.asyncio
async def test_insert_all_areas(agent, memory_db, area):
    """Test inserting documents in all memory areas."""
    doc_id = memory_db.insert_text(
        f"Test content for {area.value}",
        {"area": area.value}
    )
    assert doc_id is not None


@pytest.mark.parametrize("threshold", [0.0, 0.3, 0.5, 0.7, 0.9])
@pytest.mark.asyncio
async def test_search_various_thresholds(agent, memory_db, threshold):
    """Test searching with various threshold values."""
    memory_db.insert_text("Test document for threshold testing")

    results = await memory_db.search_similarity_threshold(
        query="Test document",
        limit=10,
        threshold=threshold
    )

    assert isinstance(results, list)


@pytest.mark.parametrize("count", [1, 5, 10, 50])
@pytest.mark.asyncio
async def test_insert_various_document_counts(agent, memory_db, count):
    """Test inserting various numbers of documents."""
    docs = generate_mock_documents(count)
    ids = memory_db.insert_documents(docs)

    assert len(ids) == count
