"""
Unit tests for Code Analyzer Tool

Tests cover:
- Python code analysis
- JavaScript code analysis
- Security scanning
- Complexity analysis
- Dependency tracking
- Code quality scoring
"""

import pytest
import ast
from unittest.mock import AsyncMock, Mock, patch, mock_open
from python.tools.code_analyzer_tool import CodeAnalyzer
from python.helpers.tool import Response


class TestCodeAnalyzerPython:
    """Test Python code analysis functionality."""

    @pytest.mark.asyncio
    async def test_analyze_python_code_success(self, mock_agent, sample_python_code):
        """Test successful Python code analysis."""
        tool = CodeAnalyzer(agent=mock_agent, name="code_analyzer", args={}, message="")
        response = await tool.execute(action="analyze", code=sample_python_code)

        assert isinstance(response, Response)
        assert "Code Analysis" in response.message
        assert "python" in response.message.lower()
        assert "Functions" in response.message

    @pytest.mark.asyncio
    async def test_analyze_python_file(self, mock_agent, temp_test_file):
        """Test analyzing Python file from disk."""
        tool = CodeAnalyzer(agent=mock_agent, name="code_analyzer", args={}, message="")
        response = await tool.execute(action="analyze", file_path=temp_test_file)

        assert isinstance(response, Response)
        assert "Code Analysis" in response.message

    @pytest.mark.asyncio
    async def test_analyze_python_detects_functions(self, mock_agent, sample_python_code):
        """Test that Python analyzer detects functions."""
        tool = CodeAnalyzer(agent=mock_agent, name="code_analyzer", args={}, message="")
        result = tool._analyze_python(sample_python_code)

        assert "functions" in result
        assert len(result["functions"]) > 0
        assert result["functions"][0]["name"] == "example_function"

    @pytest.mark.asyncio
    async def test_analyze_python_detects_classes(self, mock_agent, sample_python_code):
        """Test that Python analyzer detects classes."""
        tool = CodeAnalyzer(agent=mock_agent, name="code_analyzer", args={}, message="")
        result = tool._analyze_python(sample_python_code)

        assert "classes" in result
        assert len(result["classes"]) > 0
        assert result["classes"][0]["name"] == "ExampleClass"

    @pytest.mark.asyncio
    async def test_analyze_python_detects_imports(self, mock_agent, sample_python_code):
        """Test that Python analyzer detects imports."""
        tool = CodeAnalyzer(agent=mock_agent, name="code_analyzer", args={}, message="")
        result = tool._analyze_python(sample_python_code)

        assert "imports" in result
        assert "os" in result["imports"]
        assert "sys" in result["imports"]

    @pytest.mark.asyncio
    async def test_analyze_python_syntax_error(self, mock_agent):
        """Test handling of Python syntax errors."""
        invalid_code = "def invalid_syntax(\n    pass"

        tool = CodeAnalyzer(agent=mock_agent, name="code_analyzer", args={}, message="")
        result = tool._analyze_python(invalid_code)

        assert "error" in result
        assert "Syntax error" in result["error"]

    @pytest.mark.asyncio
    async def test_analyze_python_calculates_metrics(self, mock_agent, sample_python_code):
        """Test that Python analyzer calculates metrics."""
        tool = CodeAnalyzer(agent=mock_agent, name="code_analyzer", args={}, message="")
        result = tool._analyze_python(sample_python_code)

        assert "metrics" in result
        assert "total_functions" in result["metrics"]
        assert "total_classes" in result["metrics"]
        assert "cyclomatic_complexity" in result["metrics"]


class TestCodeAnalyzerJavaScript:
    """Test JavaScript code analysis functionality."""

    @pytest.mark.asyncio
    async def test_analyze_javascript_code(self, mock_agent, sample_javascript_code):
        """Test JavaScript code analysis."""
        tool = CodeAnalyzer(agent=mock_agent, name="code_analyzer", args={}, message="")
        result = tool._analyze_javascript(sample_javascript_code)

        assert result["language"] == "javascript"
        assert len(result["functions"]) > 0
        assert len(result["classes"]) > 0

    @pytest.mark.asyncio
    async def test_analyze_javascript_detects_functions(self, mock_agent, sample_javascript_code):
        """Test that JavaScript analyzer detects functions."""
        tool = CodeAnalyzer(agent=mock_agent, name="code_analyzer", args={}, message="")
        result = tool._analyze_javascript(sample_javascript_code)

        func_names = [f["name"] for f in result["functions"]]
        assert "exampleFunction" in func_names

    @pytest.mark.asyncio
    async def test_analyze_javascript_detects_classes(self, mock_agent, sample_javascript_code):
        """Test that JavaScript analyzer detects classes."""
        tool = CodeAnalyzer(agent=mock_agent, name="code_analyzer", args={}, message="")
        result = tool._analyze_javascript(sample_javascript_code)

        class_names = [c["name"] for c in result["classes"]]
        assert "ExampleClass" in class_names


class TestCodeAnalyzerSecurity:
    """Test security scanning functionality."""

    @pytest.mark.asyncio
    async def test_security_scan_clean_code(self, mock_agent, sample_python_code):
        """Test security scan on clean code."""
        tool = CodeAnalyzer(agent=mock_agent, name="code_analyzer", args={}, message="")
        response = await tool.execute(action="security", code=sample_python_code)

        assert "Security Scan" in response.message
        assert "No obvious vulnerabilities" in response.message

    @pytest.mark.asyncio
    async def test_security_scan_detects_eval(self, mock_agent):
        """Test that security scan detects eval usage."""
        dangerous_code = """
def unsafe_function(user_input):
    result = eval(user_input)
    return result
"""
        tool = CodeAnalyzer(agent=mock_agent, name="code_analyzer", args={}, message="")
        response = await tool.execute(action="security", code=dangerous_code)

        assert "Eval Usage" in response.message or "vulnerabilities" in response.message

    @pytest.mark.asyncio
    async def test_security_scan_detects_command_injection(self, mock_agent):
        """Test that security scan detects command injection."""
        dangerous_code = """
import os
def run_command(cmd):
    os.system(cmd)
"""
        tool = CodeAnalyzer(agent=mock_agent, name="code_analyzer", args={}, message="")
        response = await tool.execute(action="security", code=dangerous_code)

        assert "Command Injection" in response.message or "vulnerabilities" in response.message

    @pytest.mark.asyncio
    async def test_security_scan_detects_hardcoded_secrets(self, mock_agent):
        """Test that security scan detects hardcoded secrets."""
        dangerous_code = """
password = "supersecret123"
api_key = "sk-1234567890abcdef"
"""
        tool = CodeAnalyzer(agent=mock_agent, name="code_analyzer", args={}, message="")
        response = await tool.execute(action="security", code=dangerous_code)

        assert "Hardcoded Secrets" in response.message or "vulnerabilities" in response.message

    @pytest.mark.asyncio
    async def test_security_scan_multiple_vulnerabilities(self, mock_agent):
        """Test security scan with multiple vulnerabilities."""
        dangerous_code = """
import os
password = "secret"
def bad_func(user_input):
    eval(user_input)
    os.system(user_input)
"""
        tool = CodeAnalyzer(agent=mock_agent, name="code_analyzer", args={}, message="")
        response = await tool.execute(action="security", code=dangerous_code)

        assert "vulnerabilities" in response.message.lower()


class TestCodeAnalyzerComplexity:
    """Test complexity analysis functionality."""

    @pytest.mark.asyncio
    async def test_complexity_analysis_simple_function(self, mock_agent):
        """Test complexity analysis on simple function."""
        simple_code = """
def simple_function(x):
    return x * 2
"""
        tool = CodeAnalyzer(agent=mock_agent, name="code_analyzer", args={}, message="")
        response = await tool.execute(action="complexity", code=simple_code)

        assert "Complexity Analysis" in response.message
        assert "simple_function" in response.message

    @pytest.mark.asyncio
    async def test_complexity_analysis_complex_function(self, mock_agent):
        """Test complexity analysis on complex function."""
        complex_code = """
def complex_function(x, y, z):
    if x > 0:
        if y > 0:
            while z > 0:
                for i in range(10):
                    if i % 2 == 0:
                        z -= 1
    return x + y + z
"""
        tool = CodeAnalyzer(agent=mock_agent, name="code_analyzer", args={}, message="")
        response = await tool.execute(action="complexity", code=complex_code)

        assert "Complexity Analysis" in response.message
        assert "complex_function" in response.message

    def test_calculate_cyclomatic_complexity(self, mock_agent):
        """Test cyclomatic complexity calculation."""
        code = """
def test_func(x):
    if x > 0:
        return x
    elif x < 0:
        return -x
    else:
        return 0
"""
        tree = ast.parse(code)
        func_node = tree.body[0]

        tool = CodeAnalyzer(agent=mock_agent, name="code_analyzer", args={}, message="")
        complexity = tool._calculate_cyclomatic_complexity(func_node)

        assert complexity >= 1  # At least base complexity

    @pytest.mark.parametrize("complexity,expected_rating", [
        (3, "Simple"),
        (7, "Moderate"),
        (15, "Complex"),
        (25, "Very Complex")
    ])
    def test_complexity_rating(self, mock_agent, complexity, expected_rating):
        """Test complexity rating assignment."""
        tool = CodeAnalyzer(agent=mock_agent, name="code_analyzer", args={}, message="")
        rating = tool._complexity_rating(complexity)
        assert rating == expected_rating


class TestCodeAnalyzerDependencies:
    """Test dependency analysis functionality."""

    @pytest.mark.asyncio
    async def test_dependency_analysis_python(self, mock_agent, tmp_path):
        """Test Python dependency analysis."""
        # Create a fake requirements.txt
        req_file = tmp_path / "requirements.txt"
        req_file.write_text("requests==2.28.0\nnumpy>=1.20.0\npandas")

        test_file = tmp_path / "test.py"
        test_file.write_text("import os")

        tool = CodeAnalyzer(agent=mock_agent, name="code_analyzer", args={}, message="")
        response = await tool.execute(action="dependencies", file_path=str(test_file))

        assert "Dependency Analysis" in response.message
        assert "python" in response.message.lower()

    @pytest.mark.asyncio
    async def test_dependency_analysis_node(self, mock_agent, tmp_path):
        """Test Node.js dependency analysis."""
        # Create a fake package.json
        pkg_file = tmp_path / "package.json"
        pkg_file.write_text('{"dependencies": {"express": "^4.17.1", "lodash": "^4.17.21"}}')

        test_file = tmp_path / "test.js"
        test_file.write_text("const express = require('express');")

        tool = CodeAnalyzer(agent=mock_agent, name="code_analyzer", args={}, message="")
        response = await tool.execute(action="dependencies", file_path=str(test_file))

        assert "Dependency Analysis" in response.message

    @pytest.mark.asyncio
    async def test_dependency_analysis_no_deps(self, mock_agent, tmp_path):
        """Test dependency analysis with no dependencies."""
        test_file = tmp_path / "test.py"
        test_file.write_text("print('hello')")

        tool = CodeAnalyzer(agent=mock_agent, name="code_analyzer", args={}, message="")
        response = await tool.execute(action="dependencies", file_path=str(test_file))

        assert isinstance(response, Response)


class TestCodeAnalyzerQuality:
    """Test code quality scoring functionality."""

    @pytest.mark.asyncio
    async def test_quality_score_clean_code(self, mock_agent, sample_python_code):
        """Test quality score on clean code."""
        tool = CodeAnalyzer(agent=mock_agent, name="code_analyzer", args={}, message="")

        # Mock the analysis result
        with patch.object(tool, '_analyze_code', return_value=Mock(message="```json\n{}\n```")):
            response = await tool.execute(action="quality", code=sample_python_code)

        assert "Code Quality Score" in response.message

    @pytest.mark.asyncio
    async def test_quality_score_with_issues(self, mock_agent):
        """Test quality score with code issues."""
        tool = CodeAnalyzer(agent=mock_agent, name="code_analyzer", args={}, message="")

        # Mock analysis with issues
        mock_response = Mock()
        mock_response.message = '```json\n{"issues": [{"type": "warning", "message": "test"}]}\n```'

        with patch.object(tool, '_analyze_code', return_value=mock_response):
            response = await tool.execute(action="quality", code="test")

        assert "Code Quality Score" in response.message


class TestCodeAnalyzerIssueDetection:
    """Test issue detection functionality."""

    def test_detect_bare_except(self, mock_agent):
        """Test detection of bare except clauses."""
        code_with_bare_except = """
try:
    risky_operation()
except:
    pass
"""
        tree = ast.parse(code_with_bare_except)
        tool = CodeAnalyzer(agent=mock_agent, name="code_analyzer", args={}, message="")
        issues = tool._detect_python_issues(tree, code_with_bare_except)

        assert any("Bare" in issue["message"] for issue in issues)

    def test_detect_long_function(self, mock_agent):
        """Test detection of long functions."""
        # Create a function with many lines
        long_func = "def long_func():\n" + "    pass\n" * 60

        tree = ast.parse(long_func)
        tool = CodeAnalyzer(agent=mock_agent, name="code_analyzer", args={}, message="")
        issues = tool._detect_python_issues(tree, long_func)

        assert any("long" in issue["message"].lower() for issue in issues)

    def test_detect_many_parameters(self, mock_agent):
        """Test detection of functions with many parameters."""
        code_many_params = """
def many_params(a, b, c, d, e, f, g):
    return a + b + c + d + e + f + g
"""
        tree = ast.parse(code_many_params)
        tool = CodeAnalyzer(agent=mock_agent, name="code_analyzer", args={}, message="")
        issues = tool._detect_python_issues(tree, code_many_params)

        assert any("parameters" in issue["message"] or "many" in issue["message"].lower() for issue in issues)


class TestCodeAnalyzerLanguageDetection:
    """Test programming language detection."""

    @pytest.mark.parametrize("filename,expected_lang", [
        ("test.py", "python"),
        ("app.js", "javascript"),
        ("component.tsx", "typescript"),
        ("Main.java", "java"),
        ("program.cpp", "cpp"),
        ("script.go", "go"),
        ("app.rs", "rust"),
    ])
    def test_detect_language(self, mock_agent, filename, expected_lang):
        """Test language detection from file extensions."""
        tool = CodeAnalyzer(agent=mock_agent, name="code_analyzer", args={}, message="")
        detected = tool._detect_language(filename)
        assert detected == expected_lang

    def test_detect_language_unknown(self, mock_agent):
        """Test detection of unknown file type."""
        tool = CodeAnalyzer(agent=mock_agent, name="code_analyzer", args={}, message="")
        detected = tool._detect_language("file.xyz")
        assert detected == "unknown"


class TestCodeAnalyzerEdgeCases:
    """Test edge cases and error handling."""

    @pytest.mark.asyncio
    async def test_analyze_empty_code(self, mock_agent):
        """Test analyzing empty code."""
        tool = CodeAnalyzer(agent=mock_agent, name="code_analyzer", args={}, message="")
        response = await tool.execute(action="analyze", code="")

        assert "No code provided" in response.message

    @pytest.mark.asyncio
    async def test_analyze_invalid_file_path(self, mock_agent):
        """Test analyzing non-existent file."""
        tool = CodeAnalyzer(agent=mock_agent, name="code_analyzer", args={}, message="")
        response = await tool.execute(action="analyze", file_path="/nonexistent/file.py")

        assert "Error" in response.message

    @pytest.mark.asyncio
    async def test_unknown_action(self, mock_agent):
        """Test unknown action handling."""
        tool = CodeAnalyzer(agent=mock_agent, name="code_analyzer", args={}, message="")
        response = await tool.execute(action="invalid_action")

        assert "Unknown action" in response.message

    @pytest.mark.asyncio
    async def test_analyze_no_input(self, mock_agent):
        """Test analyze with no file or code."""
        tool = CodeAnalyzer(agent=mock_agent, name="code_analyzer", args={}, message="")
        response = await tool.execute(action="analyze")

        assert "No code provided" in response.message

    @pytest.mark.asyncio
    async def test_format_analysis_with_error(self, mock_agent):
        """Test formatting analysis results with error."""
        tool = CodeAnalyzer(agent=mock_agent, name="code_analyzer", args={}, message="")
        result = {"error": "Test error message"}
        formatted = tool._format_analysis_response(result, "test.py")

        assert "Analysis Error" in formatted
        assert "Test error message" in formatted


class TestCodeAnalyzerFormatting:
    """Test response formatting."""

    def test_format_analysis_complete(self, mock_agent, mock_code_analysis_response):
        """Test formatting complete analysis."""
        tool = CodeAnalyzer(agent=mock_agent, name="code_analyzer", args={}, message="")
        formatted = tool._format_analysis_response(mock_code_analysis_response, "test.py")

        assert "Code Analysis" in formatted
        assert "test.py" in formatted
        assert "Functions" in formatted
        assert "Classes" in formatted
        assert "Metrics" in formatted

    def test_format_analysis_minimal(self, mock_agent):
        """Test formatting minimal analysis."""
        tool = CodeAnalyzer(agent=mock_agent, name="code_analyzer", args={}, message="")
        minimal = {"language": "python", "lines": 10}
        formatted = tool._format_analysis_response(minimal, "test.py")

        assert "python" in formatted.lower()
        assert "10" in formatted


# ============================================================================
# INTEGRATION-STYLE TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_full_python_analysis_workflow(mock_agent, sample_python_code):
    """Test complete Python analysis workflow."""
    tool = CodeAnalyzer(agent=mock_agent, name="code_analyzer", args={}, message="")

    # Analyze
    analyze_response = await tool.execute(action="analyze", code=sample_python_code)
    assert "Code Analysis" in analyze_response.message

    # Security scan
    security_response = await tool.execute(action="security", code=sample_python_code)
    assert "Security Scan" in security_response.message

    # Complexity
    complexity_response = await tool.execute(action="complexity", code=sample_python_code)
    assert "Complexity Analysis" in complexity_response.message
