### code_analyzer_tool:
Advanced static code analysis with security scanning, complexity metrics, and quality assessment.
Supports Python (AST-based) and JavaScript analysis with detailed insights.

**Operations:**

**1. Full Code Analysis:**
```json
{
    "thoughts": [
        "I need to understand this codebase structure",
        "Let me analyze the code to identify functions, classes, and complexity"
    ],
    "tool_name": "code_analyzer_tool",
    "tool_args": {
        "action": "analyze",
        "file_path": "/path/to/code/module.py"
    }
}
```

Or with code string:
```json
{
    "tool_name": "code_analyzer_tool",
    "tool_args": {
        "action": "analyze",
        "code": "def complex_function(a, b, c, d, e, f):\n    if a > b:\n        return c\n    return d"
    }
}
```

**2. Security Scan:**
```json
{
    "thoughts": [
        "Before deploying this code, I should check for security vulnerabilities",
        "Let me run a security-focused scan"
    ],
    "tool_name": "code_analyzer_tool",
    "tool_args": {
        "action": "security",
        "file_path": "/path/to/api/handler.py"
    }
}
```

**3. Complexity Analysis:**
```json
{
    "thoughts": [
        "This function seems overly complex",
        "Let me calculate its cyclomatic complexity to see if refactoring is needed"
    ],
    "tool_name": "code_analyzer_tool",
    "tool_args": {
        "action": "complexity",
        "file_path": "/path/to/complex_module.py"
    }
}
```

**4. Dependency Analysis:**
```json
{
    "thoughts": [
        "I need to understand what dependencies this project has",
        "Let me check the requirements and packages"
    ],
    "tool_name": "code_analyzer_tool",
    "tool_args": {
        "action": "dependencies",
        "file_path": "/path/to/project/main.py"
    }
}
```

**5. Code Quality Score:**
```json
{
    "thoughts": [
        "How good is the overall code quality?",
        "Let me get a quality assessment with actionable feedback"
    ],
    "tool_name": "code_analyzer_tool",
    "tool_args": {
        "action": "quality",
        "file_path": "/path/to/module.py"
    }
}
```

**Analysis Output:**

Full analysis provides:
- **Language Detection**: Automatic detection from file extension
- **Code Metrics**: Lines of code, function count, class count
- **Functions**: Name, line number, argument count, decorators, async status
- **Classes**: Name, line number, method count, inheritance
- **Imports**: All imported modules and packages
- **Complexity**: Cyclomatic complexity score
- **Issues**: Code quality warnings and suggestions

**Security Scan Detections:**
- **SQL Injection**: Unsafe string formatting in SQL queries
- **Command Injection**: os.system() and subprocess with shell=True
- **Hardcoded Secrets**: Passwords, API keys in source code
- **Eval Usage**: Dangerous eval() and exec() calls
- **Pickle Usage**: Unsafe pickle.loads() that can execute code
- **Path Traversal**: Unsafe file path handling

**Complexity Ratings:**
- **Simple** (1-5): Easy to understand and maintain
- **Moderate** (6-10): Manageable but watch for growth
- **Complex** (11-20): Consider refactoring soon
- **Very Complex** (21+): Refactor immediately - hard to maintain

**When to Use Code Analyzer:**

**Before Deployment:**
- Security scan to catch vulnerabilities
- Quality check to ensure maintainability
- Dependency audit for outdated packages

**During Development:**
- Analyze complexity before functions get too large
- Check code structure and organization
- Validate best practices compliance

**Code Review:**
- Get objective quality metrics
- Identify refactoring candidates
- Ensure security standards

**Legacy Code:**
- Understand unfamiliar codebases
- Assess technical debt
- Plan refactoring priorities

**Learning:**
- Analyze well-written code to learn patterns
- Compare before/after refactoring
- Understand complexity impact

**Best Practices:**

1. **Run Security Scans Regularly**: Before commits, especially on authentication/API code
2. **Monitor Complexity**: Keep functions under 10 complexity points
3. **Limit Function Parameters**: More than 5 parameters is a code smell
4. **Keep Functions Short**: Over 50 lines suggests refactoring needed
5. **Address Issues Promptly**: Don't accumulate technical debt
6. **Use with Code Execution**: Analyze before running untrusted code

**Example Workflow:**

```json
// Step 1: Analyze unknown code file
{
    "tool_name": "code_analyzer_tool",
    "tool_args": {
        "action": "analyze",
        "file_path": "/home/user/project/api.py"
    }
}

// Output shows:
// - 15 functions, 3 classes
// - 250 lines of code
// - 12 imports
// - Complexity: 25 (Complex)
// - Issues: 3 warnings

// Step 2: Check specific security concerns
{
    "tool_name": "code_analyzer_tool",
    "tool_args": {
        "action": "security",
        "file_path": "/home/user/project/api.py"
    }
}

// Output shows:
// - SQL Injection risk on line 45
// - Hardcoded API key on line 12

// Step 3: Get detailed complexity metrics
{
    "tool_name": "code_analyzer_tool",
    "tool_args": {
        "action": "complexity",
        "file_path": "/home/user/project/api.py"
    }
}

// Output shows per-function complexity:
// - process_request: 15 (Complex)
// - validate_input: 3 (Simple)
// - handle_error: 8 (Moderate)

// Step 4: Overall quality score
{
    "tool_name": "code_analyzer_tool",
    "tool_args": {
        "action": "quality",
        "file_path": "/home/user/project/api.py"
    }
}

// Output: 65/100 (Fair)
// - High cyclomatic complexity (-15)
// - Security issues found (-10)
// - Long functions (-10)
```

**Common Issues Detected:**

**Python-Specific:**
- Bare `except:` clauses (should specify exception type)
- Functions longer than 50 lines
- More than 5 function parameters
- Missing docstrings (if available in AST)
- Unused imports (advanced analysis)

**JavaScript-Specific:**
- Missing semicolons (if strict mode)
- var instead of let/const
- Callback hell indicators
- Missing error handling

**Cross-Language:**
- High cyclomatic complexity
- Deep nesting levels
- Code duplication patterns
- Long parameter lists
- Magic numbers (hardcoded values)

**Quality Score Factors:**

**Positive:**
- Clear function/class structure
- Reasonable complexity (<10 per function)
- Proper error handling
- Good naming conventions

**Negative:**
- Security vulnerabilities (-10 to -30 per issue)
- High complexity (-15 points if >20)
- Long functions (-5 per function >50 lines)
- Many parameters (-5 per function >5 params)
- Code smell patterns (-5 per smell)

**Integration with Other Tools:**

```json
// Combine with code execution for testing
{
    "thoughts": [
        "Code analysis shows complexity issues",
        "Let me refactor and test the improved version"
    ],
    "tool_name": "code_execution_tool",
    "tool_args": {
        "runtime": "python",
        "code": "# Refactored code here..."
    }
}

// Store analysis insights in memory
{
    "thoughts": [
        "This security pattern is important to remember",
        "I should store it for future code reviews"
    ],
    "tool_name": "vector_memory_tool",
    "tool_args": {
        "operation": "store",
        "content": "Avoid using execute() with string formatting in SQL - use parameterized queries instead",
        "memory_type": "pattern",
        "importance": "high"
    }
}
```

**Advanced Tips:**

1. **Analyze Before Modifying**: Run analysis on existing code before refactoring
2. **Set Complexity Budgets**: Keep functions under complexity 10
3. **Automate Security Scans**: Run on every file with user input handling
4. **Track Quality Trends**: Compare scores over time to measure improvement
5. **Use for Code Generation**: After generating code, analyze to ensure quality
6. **Combine with Testing**: High complexity = needs more test coverage

**Supported Languages:**
- **Python**: Full AST analysis (recommended)
- **JavaScript/TypeScript**: Pattern-based analysis
- **Other Languages**: Basic structure detection

**Limitations:**
- Security scan catches common patterns, not all vulnerabilities
- JavaScript analysis is pattern-based (no full AST parser)
- Quality score is heuristic-based, not comprehensive
- Requires valid syntax (won't analyze broken code)
