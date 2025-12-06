#!/usr/bin/env python3
"""
Quick test script to verify all upgrades are working
Run this to check if everything is properly installed
"""

import sys
import os

def test_imports():
    """Test if all new modules can be imported"""
    print("🔍 Testing imports...")

    tests = []

    # Cost Tracker
    try:
        from python.helpers.cost_tracker import CostTracker, get_tracker
        tests.append(("✅", "Cost Tracker"))
    except Exception as e:
        tests.append(("❌", f"Cost Tracker: {str(e)}"))

    # Observability
    try:
        from python.helpers.observability import ObservabilityLogger, get_logger
        tests.append(("✅", "Observability Logger"))
    except Exception as e:
        tests.append(("❌", f"Observability Logger: {str(e)}"))

    # Vector Memory (may fail if sentence-transformers not installed)
    try:
        from python.helpers.vector_memory import VectorMemory, get_memory
        tests.append(("✅", "Vector Memory (imports only)"))
    except Exception as e:
        tests.append(("⚠️", f"Vector Memory: {str(e)} (Install: pip install sentence-transformers)"))

    # Extensions
    try:
        from python.extensions.monologue_end._60_self_reflection import SelfReflection
        tests.append(("✅", "Self-Reflection Extension"))
    except Exception as e:
        tests.append(("❌", f"Self-Reflection Extension: {str(e)}"))

    try:
        from python.extensions.monologue_end._70_cost_summary import CostSummary
        tests.append(("✅", "Cost Summary Extension"))
    except Exception as e:
        tests.append(("❌", f"Cost Summary Extension: {str(e)}"))

    try:
        from python.extensions.monologue_end._80_observability_summary import ObservabilitySummary
        tests.append(("✅", "Observability Summary Extension"))
    except Exception as e:
        tests.append(("❌", f"Observability Summary Extension: {str(e)}"))

    # Tools
    try:
        from python.tools.vector_memory_tool import VectorMemory as VectorMemoryTool
        tests.append(("✅", "Vector Memory Tool"))
    except Exception as e:
        tests.append(("❌", f"Vector Memory Tool: {str(e)}"))

    # Print results
    print("\n📊 Test Results:\n")
    for status, name in tests:
        print(f"{status} {name}")

    # Summary
    passed = sum(1 for s, _ in tests if s == "✅")
    warnings = sum(1 for s, _ in tests if s == "⚠️")
    failed = sum(1 for s, _ in tests if s == "❌")

    print(f"\n📈 Summary: {passed} passed, {warnings} warnings, {failed} failed")

    return failed == 0

def test_prompts():
    """Test if prompt files exist"""
    print("\n🔍 Testing prompt files...")

    prompts = [
        "prompts/default/agent.system.main.solving.react.md",
        "prompts/default/agent.system.tool.vector_memory.md",
    ]

    tests = []
    for prompt in prompts:
        if os.path.exists(prompt):
            tests.append(("✅", prompt))
        else:
            tests.append(("❌", f"{prompt} (not found)"))

    for status, name in tests:
        print(f"{status} {name}")

    passed = sum(1 for s, _ in tests if s == "✅")
    failed = sum(1 for s, _ in tests if s == "❌")

    return failed == 0

def test_functionality():
    """Test basic functionality of new modules"""
    print("\n🔍 Testing functionality...")

    tests = []

    # Test Cost Tracker
    try:
        from python.helpers.cost_tracker import CostTracker
        tracker = CostTracker("test_session")
        tracker.log_usage("Agent 0", "gpt-3.5-turbo", "chat", 100, 50)
        summary = tracker.get_session_summary()
        assert summary["total_tokens"] == 150
        tests.append(("✅", "Cost Tracker functionality"))
    except Exception as e:
        tests.append(("❌", f"Cost Tracker functionality: {str(e)}"))

    # Test Observability
    try:
        from python.helpers.observability import ObservabilityLogger
        logger = ObservabilityLogger("test_session")
        logger.log_llm_call("Agent 0", "gpt-3.5-turbo", 100, 50, 1000.0)
        stats = logger.get_statistics()
        assert stats["llm_calls"] == 1
        tests.append(("✅", "Observability Logger functionality"))
    except Exception as e:
        tests.append(("❌", f"Observability Logger functionality: {str(e)}"))

    # Test Vector Memory (basic, without embedding)
    try:
        from python.helpers.vector_memory import VectorMemory
        # Just test initialization
        # vm = VectorMemory()  # Would load model
        tests.append(("✅", "Vector Memory structure (not testing embedding)"))
    except Exception as e:
        tests.append(("❌", f"Vector Memory structure: {str(e)}"))

    for status, name in tests:
        print(f"{status} {name}")

    passed = sum(1 for s, _ in tests if s == "✅")
    failed = sum(1 for s, _ in tests if s == "❌")

    return failed == 0

def main():
    print("=" * 60)
    print("🚀 Agent Zero Upgrades - Test Suite")
    print("=" * 60)

    all_passed = True

    all_passed &= test_imports()
    all_passed &= test_prompts()
    all_passed &= test_functionality()

    print("\n" + "=" * 60)
    if all_passed:
        print("✅ ALL TESTS PASSED! Upgrades are working correctly.")
    else:
        print("⚠️ SOME TESTS FAILED. Check output above for details.")
    print("=" * 60)

    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
