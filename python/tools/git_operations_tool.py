from python.helpers.tool import Tool, Response
import subprocess
import os

class GitOperations(Tool):
    async def execute(self, **kwargs):
        """
        Advanced Git operations tool for version control
        """
        operation = kwargs.get("operation", "")
        path = kwargs.get("path", ".")
        message = kwargs.get("message", "")
        branch = kwargs.get("branch", "")
        remote = kwargs.get("remote", "origin")
        files = kwargs.get("files", [])

        self.log.log(type="info", heading=f"Git Operation: {operation}")

        try:
            if operation == "status":
                return await self._git_status(path)
            elif operation == "init":
                return await self._git_init(path)
            elif operation == "clone":
                return await self._git_clone(kwargs.get("url", ""), path)
            elif operation == "add":
                return await self._git_add(path, files)
            elif operation == "commit":
                return await self._git_commit(path, message)
            elif operation == "push":
                return await self._git_push(path, remote, branch)
            elif operation == "pull":
                return await self._git_pull(path, remote, branch)
            elif operation == "branch":
                return await self._git_branch(path, branch)
            elif operation == "checkout":
                return await self._git_checkout(path, branch)
            elif operation == "log":
                return await self._git_log(path, kwargs.get("limit", 10))
            elif operation == "diff":
                return await self._git_diff(path)
            elif operation == "reset":
                return await self._git_reset(path, kwargs.get("mode", "soft"))
            elif operation == "stash":
                return await self._git_stash(path, kwargs.get("action", "save"))
            else:
                return Response(
                    message=f"Unknown Git operation: {operation}\n"
                    f"Available: status, init, clone, add, commit, push, pull, "
                    f"branch, checkout, log, diff, reset, stash",
                    break_loop=False
                )

        except Exception as e:
            return Response(message=f"Git error: {str(e)}", break_loop=False)

    def _run_git_command(self, cmd, cwd="."):
        """Execute a git command"""
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode != 0:
            raise Exception(result.stderr or "Git command failed")

        return result.stdout

    async def _git_status(self, path):
        """Get repository status"""
        output = self._run_git_command(['git', 'status'], cwd=path)
        return Response(message=f"Git Status:\n\n{output}", break_loop=False)

    async def _git_init(self, path):
        """Initialize a new repository"""
        output = self._run_git_command(['git', 'init'], cwd=path)
        return Response(message=f"Repository initialized:\n{output}", break_loop=False)

    async def _git_clone(self, url, path):
        """Clone a repository"""
        output = self._run_git_command(['git', 'clone', url, path])
        return Response(message=f"Repository cloned:\n{output}", break_loop=False)

    async def _git_add(self, path, files):
        """Stage files for commit"""
        if not files:
            files = ['.']

        cmd = ['git', 'add'] + (files if isinstance(files, list) else [files])
        output = self._run_git_command(cmd, cwd=path)
        return Response(message=f"Files staged:\n{output or 'Success'}", break_loop=False)

    async def _git_commit(self, path, message):
        """Commit staged changes"""
        if not message:
            return Response(message="Commit message is required", break_loop=False)

        output = self._run_git_command(['git', 'commit', '-m', message], cwd=path)
        return Response(message=f"Commit created:\n{output}", break_loop=False)

    async def _git_push(self, path, remote, branch):
        """Push commits to remote"""
        cmd = ['git', 'push', remote]
        if branch:
            cmd.append(branch)

        output = self._run_git_command(cmd, cwd=path)
        return Response(message=f"Pushed to remote:\n{output}", break_loop=False)

    async def _git_pull(self, path, remote, branch):
        """Pull changes from remote"""
        cmd = ['git', 'pull', remote]
        if branch:
            cmd.append(branch)

        output = self._run_git_command(cmd, cwd=path)
        return Response(message=f"Pulled from remote:\n{output}", break_loop=False)

    async def _git_branch(self, path, branch):
        """Create or list branches"""
        if branch:
            output = self._run_git_command(['git', 'branch', branch], cwd=path)
            return Response(message=f"Branch created: {branch}\n{output}", break_loop=False)
        else:
            output = self._run_git_command(['git', 'branch', '-a'], cwd=path)
            return Response(message=f"Branches:\n{output}", break_loop=False)

    async def _git_checkout(self, path, branch):
        """Checkout a branch"""
        if not branch:
            return Response(message="Branch name is required", break_loop=False)

        output = self._run_git_command(['git', 'checkout', branch], cwd=path)
        return Response(message=f"Checked out: {branch}\n{output}", break_loop=False)

    async def _git_log(self, path, limit):
        """Show commit history"""
        output = self._run_git_command(
            ['git', 'log', f'-{limit}', '--oneline', '--graph'],
            cwd=path
        )
        return Response(message=f"Commit History:\n{output}", break_loop=False)

    async def _git_diff(self, path):
        """Show changes"""
        output = self._run_git_command(['git', 'diff'], cwd=path)

        if not output:
            output = "No changes in working directory"

        # Truncate if too long
        max_length = self.agent.config.max_tool_response_length
        if len(output) > max_length:
            output = output[:max_length] + f"\n\n[... truncated {len(output) - max_length} characters]"

        return Response(message=f"Git Diff:\n{output}", break_loop=False)

    async def _git_reset(self, path, mode):
        """Reset changes"""
        output = self._run_git_command(['git', 'reset', f'--{mode}', 'HEAD'], cwd=path)
        return Response(message=f"Reset ({mode}):\n{output or 'Success'}", break_loop=False)

    async def _git_stash(self, path, action):
        """Stash changes"""
        if action == "save":
            output = self._run_git_command(['git', 'stash'], cwd=path)
        elif action == "pop":
            output = self._run_git_command(['git', 'stash', 'pop'], cwd=path)
        elif action == "list":
            output = self._run_git_command(['git', 'stash', 'list'], cwd=path)
        else:
            return Response(message=f"Unknown stash action: {action}", break_loop=False)

        return Response(message=f"Stash {action}:\n{output}", break_loop=False)
