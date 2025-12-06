from python.helpers.extension import Extension
from agent import Agent, LoopData
import os

class LoadSpecializedRole(Extension):
    """
    Load specialized agent role if specified via AGENT_ZERO_ROLE environment variable
    This allows users to start Agent Zero with a specific role
    """

    async def execute(self, loop_data: LoopData = LoopData(), **kwargs):
        # Only load role once at the beginning for Agent 0
        if self.agent.number != 0 or loop_data.iteration != 0:
            return

        # Check if a specialized role is requested
        agent_role = os.getenv('AGENT_ZERO_ROLE', '').strip()

        if not agent_role or agent_role == 'default':
            # No specialized role, use default behavior
            return

        # Map role names to prompt files
        role_files = {
            'master_orchestrator': 'role.master_orchestrator.md',
            'code_specialist': 'role.code_specialist.md',
            'knowledge_researcher': 'role.knowledge_researcher.md',
            'memory_manager': 'role.memory_manager.md',
            'web_scraper': 'role.web_scraper.md',
            'task_orchestrator': 'role.task_orchestrator.md',
            'solution_architect': 'role.solution_architect.md',
            'prime_orchestrator': 'role.prime_orchestrator.md',
            'nexus_architect': 'role.nexus_architect.md',
            'system_core': 'role.system_core.md',
            'quantum_trader': 'role.quantum_trader.md',
            'content_synapse': 'role.content_synapse.md',
        }

        if agent_role not in role_files:
            # Unknown role, ignore
            return

        # Load the specialized role prompt
        try:
            from python.helpers import files
            role_file = role_files[agent_role]
            role_path = files.get_abs_path('prompts/specialized-agents', role_file)

            # Read the role prompt
            with open(role_path, 'r') as f:
                role_prompt = f.read()

            # Also load communication guidelines
            comm_path = files.get_abs_path('prompts/specialized-agents', 'communication.md')
            try:
                with open(comm_path, 'r') as f:
                    comm_prompt = f.read()
                role_prompt = role_prompt + "\n\n" + comm_prompt
            except:
                pass

            # Add the specialized role prompt to system messages
            loop_data.system.append(role_prompt)

            # Log that we loaded a specialized role
            from python.helpers.print_style import PrintStyle
            role_name = agent_role.replace('_', ' ').title()
            PrintStyle(bold=True, font_color="magenta", padding=True).print(
                f"🎭 Loaded Specialized Role: {role_name}"
            )
            self.agent.context.log.log(
                type="info",
                heading=f"Specialized Role: {role_name}",
                content=f"Agent 0 initialized with {role_name} capabilities"
            )

        except Exception as e:
            # Silent fail if role file doesn't exist
            pass
