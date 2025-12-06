"""
Cost Tracking and Token Optimization Module
Provides detailed tracking of LLM usage and costs across agent sessions
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from python.helpers import files

@dataclass
class TokenUsage:
    """Track token usage for a single LLM call"""
    timestamp: str
    agent_name: str
    model_type: str  # "chat" or "utility"
    input_tokens: int
    output_tokens: int
    estimated_cost: float
    task_description: str = ""

@dataclass
class SessionStats:
    """Aggregate stats for a session"""
    session_id: str
    start_time: str
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_estimated_cost: float = 0.0
    chat_model_calls: int = 0
    utility_model_calls: int = 0
    tool_executions: int = 0

class CostTracker:
    """
    Track and analyze costs across agent sessions
    Provides optimization insights and budget warnings
    """

    # Approximate costs per 1M tokens (update based on your models)
    # These are examples - adjust for actual models used
    COST_PER_1M_TOKENS = {
        "gpt-4": {"input": 30.0, "output": 60.0},
        "gpt-4-turbo": {"input": 10.0, "output": 30.0},
        "gpt-3.5-turbo": {"input": 0.5, "output": 1.5},
        "claude-3-opus": {"input": 15.0, "output": 75.0},
        "claude-3-sonnet": {"input": 3.0, "output": 15.0},
        "claude-3-haiku": {"input": 0.25, "output": 1.25},
        "ollama": {"input": 0.0, "output": 0.0},  # Local models
        "lmstudio": {"input": 0.0, "output": 0.0},  # Local models
        "default": {"input": 1.0, "output": 2.0},  # Fallback
    }

    def __init__(self, session_id: str = None):
        self.session_id = session_id or datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_stats = SessionStats(
            session_id=self.session_id,
            start_time=datetime.now().isoformat()
        )
        self.usage_log: List[TokenUsage] = []

        # Create logs directory if it doesn't exist
        self.logs_dir = files.get_abs_path("logs", "cost_tracking")
        os.makedirs(self.logs_dir, exist_ok=True)

    def log_usage(
        self,
        agent_name: str,
        model_name: str,
        model_type: str,
        input_tokens: int,
        output_tokens: int,
        task_description: str = ""
    ):
        """Log a single LLM usage event"""

        # Estimate cost based on model
        cost = self._estimate_cost(model_name, input_tokens, output_tokens)

        usage = TokenUsage(
            timestamp=datetime.now().isoformat(),
            agent_name=agent_name,
            model_type=model_type,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            estimated_cost=cost,
            task_description=task_description
        )

        self.usage_log.append(usage)

        # Update session stats
        self.session_stats.total_input_tokens += input_tokens
        self.session_stats.total_output_tokens += output_tokens
        self.session_stats.total_estimated_cost += cost

        if model_type == "chat":
            self.session_stats.chat_model_calls += 1
        else:
            self.session_stats.utility_model_calls += 1

    def log_tool_execution(self):
        """Increment tool execution counter"""
        self.session_stats.tool_executions += 1

    def _estimate_cost(self, model_name: str, input_tokens: int, output_tokens: int) -> float:
        """Estimate cost based on model and token counts"""

        # Extract base model name (handle versions like gpt-4-0125-preview)
        model_key = "default"
        for key in self.COST_PER_1M_TOKENS:
            if key in model_name.lower():
                model_key = key
                break

        costs = self.COST_PER_1M_TOKENS[model_key]
        input_cost = (input_tokens / 1_000_000) * costs["input"]
        output_cost = (output_tokens / 1_000_000) * costs["output"]

        return input_cost + output_cost

    def get_session_summary(self) -> Dict:
        """Get current session statistics"""
        total_tokens = self.session_stats.total_input_tokens + self.session_stats.total_output_tokens

        return {
            "session_id": self.session_stats.session_id,
            "total_tokens": total_tokens,
            "input_tokens": self.session_stats.total_input_tokens,
            "output_tokens": self.session_stats.total_output_tokens,
            "estimated_cost": f"${self.session_stats.total_estimated_cost:.4f}",
            "chat_model_calls": self.session_stats.chat_model_calls,
            "utility_model_calls": self.session_stats.utility_model_calls,
            "tool_executions": self.session_stats.tool_executions,
            "avg_tokens_per_call": total_tokens // max(1, self.session_stats.chat_model_calls + self.session_stats.utility_model_calls)
        }

    def get_optimization_insights(self) -> List[str]:
        """Provide cost optimization suggestions"""
        insights = []

        total_calls = self.session_stats.chat_model_calls + self.session_stats.utility_model_calls
        if total_calls == 0:
            return insights

        avg_tokens = (self.session_stats.total_input_tokens + self.session_stats.total_output_tokens) / total_calls

        # Check for high token usage
        if avg_tokens > 4000:
            insights.append("⚠️ High average token usage. Consider using more concise prompts.")

        # Check output/input ratio
        if self.session_stats.total_input_tokens > 0:
            ratio = self.session_stats.total_output_tokens / self.session_stats.total_input_tokens
            if ratio > 0.5:
                insights.append("💡 High output/input ratio. Consider limiting response length or using structured outputs.")

        # Check cost
        if self.session_stats.total_estimated_cost > 1.0:
            insights.append(f"💰 Session cost: ${self.session_stats.total_estimated_cost:.2f}. Consider using smaller models for simple tasks.")

        # Check if using expensive models
        if self.session_stats.total_estimated_cost > 0 and total_calls > 10:
            avg_cost_per_call = self.session_stats.total_estimated_cost / total_calls
            if avg_cost_per_call > 0.01:
                insights.append("💡 Consider using cheaper models (e.g., GPT-3.5, Claude Haiku) for utility operations.")

        if not insights:
            insights.append("✅ Token usage looks efficient!")

        return insights

    def save_session_log(self):
        """Save session data to file"""
        log_file = os.path.join(self.logs_dir, f"session_{self.session_id}.json")

        session_data = {
            "stats": asdict(self.session_stats),
            "usage_log": [asdict(u) for u in self.usage_log],
            "summary": self.get_session_summary(),
            "insights": self.get_optimization_insights()
        }

        with open(log_file, 'w') as f:
            json.dump(session_data, f, indent=2)

    def print_summary(self):
        """Print formatted session summary"""
        from python.helpers.print_style import PrintStyle

        summary = self.get_session_summary()
        insights = self.get_optimization_insights()

        PrintStyle(bold=True, font_color="yellow", padding=True).print("=" * 50)
        PrintStyle(bold=True, font_color="yellow").print("💰 SESSION COST SUMMARY")
        PrintStyle(bold=True, font_color="yellow", padding=True).print("=" * 50)

        PrintStyle(font_color="white").print(f"Session ID: {summary['session_id']}")
        PrintStyle(font_color="white").print(f"Total Tokens: {summary['total_tokens']:,}")
        PrintStyle(font_color="white").print(f"  Input:  {summary['input_tokens']:,}")
        PrintStyle(font_color="white").print(f"  Output: {summary['output_tokens']:,}")
        PrintStyle(font_color="green", bold=True).print(f"Estimated Cost: {summary['estimated_cost']}")
        PrintStyle(font_color="white").print(f"Model Calls: {summary['chat_model_calls']} chat + {summary['utility_model_calls']} utility")
        PrintStyle(font_color="white").print(f"Tool Executions: {summary['tool_executions']}")

        PrintStyle(bold=True, font_color="cyan", padding=True).print("\n📊 OPTIMIZATION INSIGHTS:")
        for insight in insights:
            PrintStyle(font_color="cyan").print(f"  {insight}")

        PrintStyle(bold=True, font_color="yellow", padding=True).print("=" * 50)


# Global instance for easy access
_global_tracker: Optional[CostTracker] = None

def get_tracker(session_id: str = None) -> CostTracker:
    """Get or create global cost tracker"""
    global _global_tracker
    if _global_tracker is None or session_id:
        _global_tracker = CostTracker(session_id)
    return _global_tracker

def reset_tracker(session_id: str = None):
    """Reset global tracker"""
    global _global_tracker
    _global_tracker = CostTracker(session_id)
    return _global_tracker
