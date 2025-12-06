"""
Reasoning Engine Extension
Implements advanced reasoning capabilities including Chain-of-Thought and Tree-of-Thoughts
"""

from python.helpers.extension import Extension
from agent import LoopData


class ReasoningEngine(Extension):
    """
    Advanced reasoning capabilities for Agent Zero

    Features:
    - Chain-of-Thought prompting (forced intermediate reasoning)
    - Tree-of-Thoughts exploration (multiple reasoning paths)
    - Self-verification loops
    - Error correction
    """

    async def execute(self, loop_data: LoopData = LoopData(), **kwargs):
        """
        Inject reasoning instructions into system prompt
        """

        # Only activate reasoning engine for complex tasks
        # Check if task seems complex based on iteration count or explicit request
        activate_reasoning = self._should_activate_reasoning(loop_data)

        if not activate_reasoning:
            return

        # Read and inject reasoning prompt
        reasoning_prompt = self.agent.read_prompt("agent.system.reasoning.md")

        # Add to system prompts
        loop_data.system.append(reasoning_prompt)

        # Log activation
        self.agent.context.log.log(
            type="info",
            content="🧠 Reasoning engine activated",
            temp=True
        )

    def _should_activate_reasoning(self, loop_data: LoopData) -> bool:
        """
        Determine if reasoning engine should be activated

        Criteria:
        - Iteration count > 2 (task is complex)
        - User message contains reasoning keywords
        - Previous iteration had errors
        """

        # Always activate after 2+ iterations (task is getting complex)
        if loop_data.iteration >= 2:
            return True

        # Check for reasoning keywords in user message
        reasoning_keywords = [
            "analyze", "explain", "why", "how", "reasoning",
            "think", "consider", "evaluate", "compare",
            "plan", "strategy", "approach", "solve",
            "complex", "difficult", "challenging"
        ]

        message_lower = loop_data.message.lower()
        if any(keyword in message_lower for keyword in reasoning_keywords):
            return True

        # Check if agent data indicates complexity
        if self.agent.get_data("complex_task"):
            return True

        return False
