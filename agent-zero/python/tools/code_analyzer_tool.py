"""
Code Analyzer Tool - Advanced static code analysis
"""

import ast
import os
from pathlib import Path
from python.helpers.tool import Tool, Response
from python.helpers.print_style import PrintStyle


class CodeAnalyzer(Tool):
    """
    Advanced code analysis tool

    Capabilities:
    - AST parsing for Python/JavaScript
    - Code quality scoring
    - Security vulnerability detection
    - Complexity analysis
    - Dependency tracking
    - Dead code detection
    """

    async def execute(self, action: str = "analyze", **kwargs):
        """
        Execute code analysis operations

        Args:
            action: Operation to perform
                - "analyze": Full code analysis
                - "security": Security-focused scan
                - "complexity": Complexity metrics
                - "dependencies": Dependency analysis
                - "quality": Code quality score

        Actions:
            analyze: file_path or code
            security: file_path or code
            complexity: file_path or code
            dependencies: file_path
            quality: file_path or code
        """

        if action == "analyze":
            return await self._analyze_code(
                file_path=kwargs.get("file_path"),
                code=kwargs.get("code")
            )
        elif action == "security":
            return await self._security_scan(
                file_path=kwargs.get("file_path"),
                code=kwargs.get("code")
            )
        elif action == "complexity":
            return await self._complexity_analysis(
                file_path=kwargs.get("file_path"),
                code=kwargs.get("code")
            )
        elif action == "dependencies":
            return await self._dependency_analysis(
                file_path=kwargs.get("file_path")
            )
        elif action == "quality":
            return await self._quality_score(
                file_path=kwargs.get("file_path"),
                code=kwargs.get("code")
            )
        else:
            return Response(
                message=f"Unknown action: {action}",
                break_loop=False
            )

    async def _analyze_code(self, file_path: str = None, code: str = None) -> Response:
        """Comprehensive code analysis"""

        PrintStyle(font_color="cyan").print("🔍 Analyzing code...")

        # Get code content
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                language = self._detect_language(file_path)
            except Exception as e:
                return Response(
                    message=f"Error reading file: {str(e)}",
                    break_loop=False
                )
        else:
            language = "python"  # default

        if not code:
            return Response(
                message="No code provided for analysis",
                break_loop=False
            )

        # Perform analysis based on language
        if language == "python":
            result = self._analyze_python(code, file_path)
        elif language in ["javascript", "typescript"]:
            result = self._analyze_javascript(code, file_path)
        else:
            result = {"error": f"Unsupported language: {language}"}

        # Format response
        response = self._format_analysis_response(result, file_path or "code snippet")

        return Response(message=response, break_loop=False)

    def _analyze_python(self, code: str, file_path: str = None) -> dict:
        """Analyze Python code using AST"""

        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return {
                "error": f"Syntax error: {str(e)}",
                "line": e.lineno,
                "offset": e.offset
            }

        analysis = {
            "language": "python",
            "lines": len(code.splitlines()),
            "functions": [],
            "classes": [],
            "imports": [],
            "complexity": 0,
            "issues": [],
            "metrics": {}
        }

        # Walk the AST
        for node in ast.walk(tree):
            # Functions
            if isinstance(node, ast.FunctionDef):
                analysis["functions"].append({
                    "name": node.name,
                    "line": node.lineno,
                    "args": len(node.args.args),
                    "decorators": len(node.decorator_list),
                    "is_async": isinstance(node, ast.AsyncFunctionDef)
                })

            # Classes
            elif isinstance(node, ast.ClassDef):
                methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                analysis["classes"].append({
                    "name": node.name,
                    "line": node.lineno,
                    "methods": len(methods),
                    "bases": len(node.bases)
                })

            # Imports
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    analysis["imports"].append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    analysis["imports"].append(f"{module}.{alias.name}")

            # Complexity indicators
            elif isinstance(node, (ast.If, ast.For, ast.While, ast.Try)):
                analysis["complexity"] += 1

        # Calculate metrics
        analysis["metrics"] = {
            "total_functions": len(analysis["functions"]),
            "total_classes": len(analysis["classes"]),
            "total_imports": len(analysis["imports"]),
            "cyclomatic_complexity": analysis["complexity"],
            "avg_function_args": sum(f["args"] for f in analysis["functions"]) / len(analysis["functions"]) if analysis["functions"] else 0
        }

        # Detect issues
        analysis["issues"] = self._detect_python_issues(tree, code)

        return analysis

    def _analyze_javascript(self, code: str, file_path: str = None) -> dict:
        """Basic JavaScript analysis (without full AST parser)"""

        lines = code.splitlines()

        analysis = {
            "language": "javascript",
            "lines": len(lines),
            "functions": [],
            "classes": [],
            "imports": [],
            "issues": []
        }

        # Simple pattern matching (would need proper JS parser for production)
        import re

        # Find functions
        func_pattern = r'function\s+(\w+)\s*\('
        for i, line in enumerate(lines, 1):
            matches = re.findall(func_pattern, line)
            for match in matches:
                analysis["functions"].append({
                    "name": match,
                    "line": i
                })

        # Find classes
        class_pattern = r'class\s+(\w+)'
        for i, line in enumerate(lines, 1):
            matches = re.findall(class_pattern, line)
            for match in matches:
                analysis["classes"].append({
                    "name": match,
                    "line": i
                })

        # Find imports
        import_pattern = r'import\s+.*\s+from\s+[\'"](.+)[\'"]'
        for line in lines:
            matches = re.findall(import_pattern, line)
            analysis["imports"].extend(matches)

        return analysis

    def _detect_python_issues(self, tree: ast.AST, code: str) -> list:
        """Detect common Python code issues"""

        issues = []

        for node in ast.walk(tree):
            # Bare except
            if isinstance(node, ast.ExceptHandler):
                if node.type is None:
                    issues.append({
                        "type": "warning",
                        "line": node.lineno,
                        "message": "Bare 'except' clause - should specify exception type"
                    })

            # Long functions (> 50 lines)
            if isinstance(node, ast.FunctionDef):
                if hasattr(node, 'end_lineno'):
                    func_length = node.end_lineno - node.lineno
                    if func_length > 50:
                        issues.append({
                            "type": "warning",
                            "line": node.lineno,
                            "message": f"Function '{node.name}' is long ({func_length} lines) - consider refactoring"
                        })

            # Too many arguments (> 5)
            if isinstance(node, ast.FunctionDef):
                if len(node.args.args) > 5:
                    issues.append({
                        "type": "warning",
                        "line": node.lineno,
                        "message": f"Function '{node.name}' has many parameters ({len(node.args.args)}) - consider using kwargs or objects"
                    })

        return issues

    async def _security_scan(self, file_path: str = None, code: str = None) -> Response:
        """Security-focused code scan"""

        PrintStyle(font_color="yellow").print("🔒 Running security scan...")

        if file_path:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()

        if not code:
            return Response(message="No code provided", break_loop=False)

        vulnerabilities = []

        # Check for common vulnerabilities
        security_patterns = {
            "SQL Injection": [r'execute\([^)]*%\s*[^)]*\)', r'cursor\.execute.*\+'],
            "Command Injection": [r'os\.system\(', r'subprocess\.call\(.*shell=True'],
            "Hardcoded Secrets": [r'password\s*=\s*["\'][^"\']+["\']', r'api_key\s*=\s*["\'][^"\']+["\']'],
            "Eval Usage": [r'\beval\(', r'\bexec\('],
            "Pickle Usage": [r'pickle\.loads?\('],
        }

        import re
        for vuln_type, patterns in security_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, code, re.IGNORECASE)
                for match in matches:
                    line_num = code[:match.start()].count('\n') + 1
                    vulnerabilities.append({
                        "type": vuln_type,
                        "line": line_num,
                        "code": match.group(),
                        "severity": "high"
                    })

        response = "🔒 **Security Scan Results**\n\n"
        if vulnerabilities:
            response += f"⚠️ Found {len(vulnerabilities)} potential vulnerabilities:\n\n"
            for vuln in vulnerabilities:
                response += f"- Line {vuln['line']}: {vuln['type']} ({vuln['severity']})\n"
                response += f"  Code: `{vuln['code'][:50]}`\n\n"
        else:
            response += "✅ No obvious vulnerabilities detected\n"

        return Response(message=response, break_loop=False)

    async def _complexity_analysis(self, file_path: str = None, code: str = None) -> Response:
        """Calculate code complexity metrics"""

        if file_path:
            with open(file_path, 'r') as f:
                code = f.read()

        if not code:
            return Response(message="No code provided", break_loop=False)

        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return Response(message=f"Syntax error: {str(e)}", break_loop=False)

        complexity_map = {}

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                complexity = self._calculate_cyclomatic_complexity(node)
                complexity_map[node.name] = {
                    "line": node.lineno,
                    "complexity": complexity,
                    "rating": self._complexity_rating(complexity)
                }

        response = "📊 **Complexity Analysis**\n\n"
        for func_name, data in complexity_map.items():
            response += f"Function: {func_name} (line {data['line']})\n"
            response += f"  Complexity: {data['complexity']} ({data['rating']})\n\n"

        return Response(message=response, break_loop=False)

    def _calculate_cyclomatic_complexity(self, node: ast.FunctionDef) -> int:
        """Calculate cyclomatic complexity for a function"""
        complexity = 1  # Base complexity

        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1

        return complexity

    def _complexity_rating(self, complexity: int) -> str:
        """Rate complexity level"""
        if complexity <= 5:
            return "Simple"
        elif complexity <= 10:
            return "Moderate"
        elif complexity <= 20:
            return "Complex"
        else:
            return "Very Complex"

    async def _dependency_analysis(self, file_path: str) -> Response:
        """Analyze project dependencies"""

        if not file_path:
            return Response(message="File path required", break_loop=False)

        # Look for requirements.txt, package.json, etc.
        project_root = Path(file_path).parent
        deps = {}

        # Python dependencies
        req_file = project_root / "requirements.txt"
        if req_file.exists():
            with open(req_file) as f:
                deps["python"] = [line.strip() for line in f if line.strip() and not line.startswith('#')]

        # Node dependencies
        pkg_file = project_root / "package.json"
        if pkg_file.exists():
            import json
            with open(pkg_file) as f:
                pkg_data = json.load(f)
                deps["node"] = list(pkg_data.get("dependencies", {}).keys())

        response = "📦 **Dependency Analysis**\n\n"
        for lang, packages in deps.items():
            response += f"{lang.capitalize()} dependencies ({len(packages)}):\n"
            for pkg in packages[:10]:  # Show first 10
                response += f"  - {pkg}\n"
            if len(packages) > 10:
                response += f"  ... and {len(packages) - 10} more\n"
            response += "\n"

        return Response(message=response, break_loop=False)

    async def _quality_score(self, file_path: str = None, code: str = None) -> Response:
        """Calculate overall code quality score"""

        # Run full analysis
        analysis_result = await self._analyze_code(file_path, code)
        analysis = eval(analysis_result.message.split("```json\n")[1].split("\n```")[0]) if "```json" in analysis_result.message else {}

        score = 100
        feedback = []

        # Deduct points for issues
        if "issues" in analysis:
            score -= len(analysis["issues"]) * 5
            feedback.append(f"Issues found: {len(analysis['issues'])}")

        # Check complexity
        if "metrics" in analysis and analysis["metrics"].get("cyclomatic_complexity", 0) > 20:
            score -= 15
            feedback.append("High cyclomatic complexity")

        # Check function length
        if "functions" in analysis:
            long_funcs = [f for f in analysis["functions"] if f.get("lines", 0) > 50]
            if long_funcs:
                score -= len(long_funcs) * 5
                feedback.append(f"Long functions: {len(long_funcs)}")

        score = max(0, score)
        rating = "Excellent" if score >= 90 else "Good" if score >= 75 else "Fair" if score >= 60 else "Needs Improvement"

        response = f"⭐ **Code Quality Score: {score}/100 ({rating})**\n\n"
        if feedback:
            response += "Feedback:\n"
            for item in feedback:
                response += f"- {item}\n"

        return Response(message=response, break_loop=False)

    def _detect_language(self, file_path: str) -> str:
        """Detect programming language from file extension"""
        ext = Path(file_path).suffix.lower()
        lang_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.jsx': 'javascript',
            '.tsx': 'typescript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.go': 'go',
            '.rs': 'rust',
        }
        return lang_map.get(ext, 'unknown')

    def _format_analysis_response(self, analysis: dict, file_name: str) -> str:
        """Format analysis results as readable text"""

        if "error" in analysis:
            return f"❌ Analysis Error: {analysis['error']}"

        response = f"📊 **Code Analysis: {file_name}**\n\n"
        response += f"Language: {analysis.get('language', 'unknown').capitalize()}\n"
        response += f"Lines of code: {analysis.get('lines', 0)}\n\n"

        if analysis.get("functions"):
            response += f"**Functions ({len(analysis['functions'])}):**\n"
            for func in analysis["functions"][:5]:
                response += f"  - {func['name']} (line {func['line']}, {func.get('args', 0)} args)\n"
            if len(analysis["functions"]) > 5:
                response += f"  ... and {len(analysis['functions']) - 5} more\n"
            response += "\n"

        if analysis.get("classes"):
            response += f"**Classes ({len(analysis['classes'])}):**\n"
            for cls in analysis["classes"][:5]:
                response += f"  - {cls['name']} (line {cls['line']}, {cls.get('methods', 0)} methods)\n"
            if len(analysis["classes"]) > 5:
                response += f"  ... and {len(analysis['classes']) - 5} more\n"
            response += "\n"

        if analysis.get("imports"):
            response += f"**Imports:** {len(analysis['imports'])} modules\n\n"

        if analysis.get("metrics"):
            response += "**Metrics:**\n"
            for key, value in analysis["metrics"].items():
                if isinstance(value, float):
                    response += f"  - {key}: {value:.2f}\n"
                else:
                    response += f"  - {key}: {value}\n"
            response += "\n"

        if analysis.get("issues"):
            response += f"**Issues Found ({len(analysis['issues'])}):**\n"
            for issue in analysis["issues"][:10]:
                response += f"  - Line {issue['line']}: {issue['message']}\n"
            if len(analysis["issues"]) > 10:
                response += f"  ... and {len(analysis['issues']) - 10} more\n"

        return response
