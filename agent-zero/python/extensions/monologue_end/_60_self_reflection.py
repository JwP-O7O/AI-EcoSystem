from python.helpers.extension import Extension
from agent import LoopData
from python.helpers.print_style import PrintStyle
import json

class SelfReflection(Extension):
    """
    Self-Reflection Extension: Evaluates agent performance after task completion
    Implements metacognitive learning through self-evaluation
    """

    async def execute(self, tools_result: str = "", **kwargs):
        # Only reflect for Agent 0 (main agent) on substantial tasks
        if self.agent.number != 0:
            return

        # Skip reflection for very short interactions (simple questions)
        if len(self.agent.history) < 4:
            return

        # Count tool usages in this monologue
        tool_uses = sum(1 for msg in self.agent.history if "```tool" in str(msg.content))

        # Only reflect if agent actually worked on a task (used tools)
        if tool_uses == 0:
            return

        PrintStyle(
            bold=True, font_color="cyan", padding=True, background_color="white"
        ).print(f"{self.agent.agent_name}: Self-Reflection")

        # Build reflection prompt
        reflection_prompt = self._build_reflection_prompt(tools_result, tool_uses)

        # Get reflection from utility model
        log_item = self.agent.context.log.log(
            type="reflection", heading=f"{self.agent.agent_name}: Task Reflection"
        )

        printer = PrintStyle(italic=True, font_color="cyan", padding=False)

        def log_callback(content):
            printer.print(content)
            log_item.stream(content=content)

        reflection = await self.agent.call_utility_llm(
            system=self._get_system_prompt(),
            msg=reflection_prompt,
            callback=log_callback
        )

        # Try to parse structured reflection
        try:
            reflection_data = self._parse_reflection(reflection)
            self._store_reflection_insights(reflection_data)
        except:
            # If parsing fails, just log the raw reflection
            pass

    def _build_reflection_prompt(self, result: str, tool_count: int) -> str:
        """Build the reflection prompt based on conversation history"""

        # Get last few messages for context
        recent_history = self.agent.history[-10:]  # Last 10 messages
        history_text = "\n".join([
            f"{'User' if msg.type == 'human' else 'Assistant'}: {msg.content[:500]}..."  # Truncate long messages
            for msg in recent_history
        ])

        prompt = f"""Reflect on the task you just completed:

**Task Context:**
{history_text}

**Final Result:**
{result[:1000]}  # Truncate if very long

**Tools Used:** {tool_count} tool calls

**Reflection Questions:**
1. Was the task completed successfully? (Yes/No/Partially)
2. What went well?
3. What could have been done better?
4. Were there any errors or challenges? How were they handled?
5. What did you learn that could help with future similar tasks?
6. Efficiency: Could this have been solved with fewer steps?

Please provide a structured reflection addressing these points.
"""
        return prompt

    def _get_system_prompt(self) -> str:
        """System prompt for reflection analysis"""
        return """You are a metacognitive evaluator for an AI agent system.
Your role is to provide honest, constructive self-reflection on task performance.

Focus on:
- **Accuracy**: Was the solution correct?
- **Efficiency**: Were resources used optimally?
- **Problem-solving**: Was the approach logical and effective?
- **Learning**: What insights can improve future performance?

Be specific and actionable in your feedback. Acknowledge both successes and areas for improvement.
Keep your reflection concise but insightful (2-4 short paragraphs)."""

    def _parse_reflection(self, reflection: str) -> dict:
        """
        Try to extract structured data from reflection
        Returns dict with reflection insights
        """
        reflection_data = {
            "success": "unknown",
            "strengths": [],
            "improvements": [],
            "learnings": [],
            "raw_reflection": reflection
        }

        # Simple keyword-based parsing
        reflection_lower = reflection.lower()

        # Determine success
        if any(word in reflection_lower for word in ["successfully", "completed", "accomplished"]):
            reflection_data["success"] = "yes"
        elif any(word in reflection_lower for word in ["failed", "unsuccessful", "could not"]):
            reflection_data["success"] = "no"
        elif "partially" in reflection_lower:
            reflection_data["success"] = "partial"

        return reflection_data

    def _store_reflection_insights(self, reflection_data: dict):
        """
        Store reflection insights in agent data for potential future use
        Could be extended to save to memory/database
        """
        if not hasattr(self.agent, 'reflections'):
            self.agent.data['reflections'] = []

        self.agent.data['reflections'].append({
            "task_id": len(self.agent.history),
            "success": reflection_data["success"],
            "timestamp": "now",  # Could use actual timestamp
            "insights": reflection_data.get("learnings", [])
        })

        # Keep only last 10 reflections to avoid memory bloat
        if len(self.agent.data['reflections']) > 10:
            self.agent.data['reflections'] = self.agent.data['reflections'][-10:]
