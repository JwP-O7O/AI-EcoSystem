import asyncio
import shlex
import time
from dataclasses import dataclass
from python.helpers.tool import Tool, Response
from python.helpers.print_style import PrintStyle
from python.helpers.shell_local import LocalInteractiveSession
from python.helpers.shell_ssh import SSHInteractiveSession
from python.helpers.docker import DockerContainerManager

@dataclass
class State:
    shell: LocalInteractiveSession | SSHInteractiveSession
    docker: DockerContainerManager | None

class StaticAnalysis(Tool):
    async def execute(self, **kwargs):
        await self.prepare_state()
        
        tool_name = self.args.get("tool", "pylint")
        target = self.args.get("target", ".")
        target = shlex.quote(target)
        
        if tool_name == "pylint":
            command = f"pylint {target}"
        elif tool_name == "bandit":
            command = f"bandit -r {target}"
        else:
            return Response(message=f"Unknown tool: {tool_name}", break_loop=False)
        
        output = await self.terminal_session(command)
        
        return Response(message=output, break_loop=False)

    async def before_execution(self, **kwargs):
        PrintStyle(font_color="#1B4F72", padding=True, background_color="white", bold=True).print(
            f"{self.agent.agent_name}: Running {self.args.get('tool', 'pylint')} on '{self.args.get('target', '.')}'"
        )

    async def prepare_state(self, reset=False):
        self.state = self.agent.get_data("cot_state")
        if not self.state or reset:
            if self.agent.config.code_exec_docker_enabled:
                docker = DockerContainerManager(
                    logger=self.agent.context.log,
                    name=self.agent.config.code_exec_docker_name,
                    image=self.agent.config.code_exec_docker_image,
                    ports=self.agent.config.code_exec_docker_ports,
                    volumes=self.agent.config.code_exec_docker_volumes,
                )
                docker.start_container()
            else:
                docker = None

            if self.agent.config.code_exec_ssh_enabled:
                shell = SSHInteractiveSession(
                    self.agent.context.log,
                    self.agent.config.code_exec_ssh_addr,
                    self.agent.config.code_exec_ssh_port,
                    self.agent.config.code_exec_ssh_user,
                    self.agent.config.code_exec_ssh_pass,
                )
            else:
                shell = LocalInteractiveSession()

            self.state = State(shell=shell, docker=docker)
            await shell.connect()
        self.agent.set_data("cot_state", self.state)

    async def terminal_session(self, command: str):
        self.state.shell.send_command(command)
        return await self.get_terminal_output()

    async def get_terminal_output(
        self, wait_with_output=3, wait_without_output=10, max_exec_time=60
    ):
        idle = 0
        SLEEP_TIME = 0.1
        start_time = time.time()
        full_output = ""

        while max_exec_time <= 0 or time.time() - start_time < max_exec_time:
            await asyncio.sleep(SLEEP_TIME)
            _, partial_output = await self.state.shell.read_output(max_exec_time)

            if partial_output:
                PrintStyle(font_color="#85C1E9").stream(partial_output)
                full_output += partial_output
                idle = 0
            else:
                idle += 1
                if (full_output and idle > wait_with_output / SLEEP_TIME) or (
                    not full_output and idle > wait_without_output / SLEEP_TIME
                ):
                    break
        return full_output
