from python.helpers.tool import Tool, Response
import os
import re
import subprocess
import shutil

class SearchGrep(Tool):
    async def execute(self, **kwargs):
        """
        Advanced search and grep tool for finding patterns in files
        """
        pattern = kwargs.get("pattern", "")
        path = kwargs.get("path", ".")
        file_pattern = kwargs.get("file_pattern", "*")
        case_sensitive = kwargs.get("case_sensitive", False)
        whole_word = kwargs.get("whole_word", False)
        context_lines = kwargs.get("context_lines", 2)

        if not pattern:
            return Response(message="Please provide a search pattern", break_loop=False)

        self.log.log(type="info", heading=f"Searching for: {pattern}")

        try:
            # Use ripgrep if available (faster), otherwise fallback to grep
            if shutil.which('rg'):
                results = self._ripgrep_search(
                    pattern, path, file_pattern, case_sensitive, context_lines
                )
            elif shutil.which('grep'):
                results = self._grep_search(
                    pattern, path, file_pattern, case_sensitive, whole_word, context_lines
                )
            else:
                # Python fallback
                results = self._python_search(
                    pattern, path, file_pattern, case_sensitive, whole_word, context_lines
                )

            # Truncate if too long
            max_length = self.agent.config.max_tool_response_length
            if len(results) > max_length:
                results = results[:max_length] + f"\n\n[... truncated {len(results) - max_length} characters]"

            message = f"Search results for '{pattern}' in {path}:\n\n{results}"
            return Response(message=message, break_loop=False)

        except Exception as e:
            return Response(message=f"Search error: {str(e)}", break_loop=False)

    def _ripgrep_search(self, pattern, path, file_pattern, case_sensitive, context_lines):
        """Search using ripgrep (rg)"""
        cmd = ['rg', pattern, path]

        if not case_sensitive:
            cmd.insert(1, '-i')

        if file_pattern != "*":
            cmd.extend(['-g', file_pattern])

        if context_lines > 0:
            cmd.extend(['-C', str(context_lines)])

        cmd.extend(['--max-count', '100'])  # Limit results

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.stdout if result.stdout else "No matches found"
        except Exception as e:
            return f"Ripgrep error: {str(e)}"

    def _grep_search(self, pattern, path, file_pattern, case_sensitive, whole_word, context_lines):
        """Search using grep"""
        cmd = ['grep', '-r', pattern, path]

        if not case_sensitive:
            cmd.insert(1, '-i')

        if whole_word:
            cmd.insert(1, '-w')

        if context_lines > 0:
            cmd.extend(['-C', str(context_lines)])

        if file_pattern != "*":
            cmd.extend(['--include', file_pattern])

        cmd.extend(['-m', '100'])  # Limit results

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.stdout if result.stdout else "No matches found"
        except Exception as e:
            return f"Grep error: {str(e)}"

    def _python_search(self, pattern, path, file_pattern, case_sensitive, whole_word, context_lines):
        """Python-based search fallback"""
        import fnmatch

        results = []
        flags = 0 if case_sensitive else re.IGNORECASE

        if whole_word:
            pattern = r'\b' + pattern + r'\b'

        regex = re.compile(pattern, flags)

        for root, dirs, files in os.walk(path):
            for filename in files:
                if fnmatch.fnmatch(filename, file_pattern):
                    filepath = os.path.join(root, filename)

                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            lines = f.readlines()

                        for i, line in enumerate(lines):
                            if regex.search(line):
                                # Add context
                                start = max(0, i - context_lines)
                                end = min(len(lines), i + context_lines + 1)

                                context = []
                                for j in range(start, end):
                                    marker = '> ' if j == i else '  '
                                    context.append(f"{marker}{j+1}: {lines[j].rstrip()}")

                                results.append(
                                    f"\n{filepath}:{i+1}\n" + "\n".join(context)
                                )

                                if len(results) >= 100:
                                    break

                    except Exception:
                        continue

                if len(results) >= 100:
                    break

            if len(results) >= 100:
                break

        if not results:
            return "No matches found"

        return "\n".join(results)
