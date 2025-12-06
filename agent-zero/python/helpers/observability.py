"""
Enhanced Observability and Monitoring for Agent Zero
Lightweight, file-based logging system optimized for Termux/Android
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from python.helpers import files

@dataclass
class AgentEvent:
    """Single agent event/action"""
    timestamp: str
    agent_name: str
    event_type: str  # "llm_call", "tool_use", "error", "decision", "delegation"
    event_data: Dict[str, Any]
    duration_ms: Optional[float] = None
    success: bool = True

class ObservabilityLogger:
    """
    Lightweight observability logger for agent actions
    Tracks agent behavior, decisions, and performance
    """

    def __init__(self, session_id: str = None):
        self.session_id = session_id or datetime.now().strftime("%Y%m%d_%H%M%S")
        self.events: List[AgentEvent] = []

        # Create logs directory
        self.logs_dir = files.get_abs_path("logs", "observability")
        os.makedirs(self.logs_dir, exist_ok=True)

        # Session file
        self.session_file = os.path.join(self.logs_dir, f"session_{self.session_id}.jsonl")

        # Statistics
        self.stats = {
            "total_events": 0,
            "llm_calls": 0,
            "tool_uses": 0,
            "errors": 0,
            "delegations": 0,
            "total_duration_ms": 0
        }

    def log_event(
        self,
        agent_name: str,
        event_type: str,
        event_data: Dict[str, Any],
        duration_ms: float = None,
        success: bool = True
    ):
        """Log a single agent event"""
        event = AgentEvent(
            timestamp=datetime.now().isoformat(),
            agent_name=agent_name,
            event_type=event_type,
            event_data=event_data,
            duration_ms=duration_ms,
            success=success
        )

        self.events.append(event)
        self.stats["total_events"] += 1

        # Update specific counters
        if event_type == "llm_call":
            self.stats["llm_calls"] += 1
        elif event_type == "tool_use":
            self.stats["tool_uses"] += 1
        elif event_type == "error":
            self.stats["errors"] += 1
        elif event_type == "delegation":
            self.stats["delegations"] += 1

        if duration_ms:
            self.stats["total_duration_ms"] += duration_ms

        # Write to file (JSONL format - one JSON per line)
        self._append_to_file(event)

    def _append_to_file(self, event: AgentEvent):
        """Append event to JSONL file"""
        try:
            with open(self.session_file, 'a') as f:
                f.write(json.dumps(asdict(event)) + '\n')
        except Exception as e:
            # Silent fail - don't interrupt agent operation
            pass

    def log_llm_call(
        self,
        agent_name: str,
        model: str,
        prompt_length: int,
        response_length: int,
        duration_ms: float,
        success: bool = True
    ):
        """Log an LLM API call"""
        self.log_event(
            agent_name=agent_name,
            event_type="llm_call",
            event_data={
                "model": model,
                "prompt_length": prompt_length,
                "response_length": response_length
            },
            duration_ms=duration_ms,
            success=success
        )

    def log_tool_use(
        self,
        agent_name: str,
        tool_name: str,
        tool_args: Dict,
        result_summary: str,
        duration_ms: float,
        success: bool = True
    ):
        """Log a tool execution"""
        self.log_event(
            agent_name=agent_name,
            event_type="tool_use",
            event_data={
                "tool_name": tool_name,
                "args": str(tool_args)[:200],  # Truncate long args
                "result": result_summary[:500]  # Truncate long results
            },
            duration_ms=duration_ms,
            success=success
        )

    def log_error(
        self,
        agent_name: str,
        error_type: str,
        error_message: str,
        context: Dict = None
    ):
        """Log an error"""
        self.log_event(
            agent_name=agent_name,
            event_type="error",
            event_data={
                "error_type": error_type,
                "message": error_message,
                "context": context or {}
            },
            success=False
        )

    def log_decision(
        self,
        agent_name: str,
        decision: str,
        reasoning: str,
        alternatives: List[str] = None
    ):
        """Log an agent decision point"""
        self.log_event(
            agent_name=agent_name,
            event_type="decision",
            event_data={
                "decision": decision,
                "reasoning": reasoning[:200],  # Truncate
                "alternatives": alternatives or []
            }
        )

    def log_delegation(
        self,
        agent_name: str,
        subordinate_name: str,
        task: str,
        reason: str
    ):
        """Log task delegation to subordinate agent"""
        self.log_event(
            agent_name=agent_name,
            event_type="delegation",
            event_data={
                "subordinate": subordinate_name,
                "task": task[:200],  # Truncate
                "reason": reason[:200]
            }
        )

    def get_statistics(self) -> Dict:
        """Get session statistics"""
        avg_duration = 0
        if self.stats["total_events"] > 0:
            avg_duration = self.stats["total_duration_ms"] / self.stats["total_events"]

        return {
            "session_id": self.session_id,
            "total_events": self.stats["total_events"],
            "llm_calls": self.stats["llm_calls"],
            "tool_uses": self.stats["tool_uses"],
            "errors": self.stats["errors"],
            "delegations": self.stats["delegations"],
            "avg_event_duration_ms": round(avg_duration, 2),
            "success_rate": self._calculate_success_rate()
        }

    def _calculate_success_rate(self) -> float:
        """Calculate percentage of successful events"""
        if not self.events:
            return 100.0

        successful = sum(1 for e in self.events if e.success)
        return round((successful / len(self.events)) * 100, 2)

    def get_error_summary(self) -> List[Dict]:
        """Get summary of all errors"""
        errors = [e for e in self.events if e.event_type == "error"]

        return [{
            "timestamp": e.timestamp,
            "agent": e.agent_name,
            "error_type": e.event_data.get("error_type"),
            "message": e.event_data.get("message")
        } for e in errors]

    def get_performance_insights(self) -> List[str]:
        """Generate performance insights"""
        insights = []
        stats = self.get_statistics()

        # Error rate check
        error_rate = (stats["errors"] / max(1, stats["total_events"])) * 100
        if error_rate > 10:
            insights.append(f"⚠️ High error rate: {error_rate:.1f}% of events failed")

        # Tool usage check
        if stats["tool_uses"] == 0 and stats["llm_calls"] > 5:
            insights.append("💡 No tools used - agent might be stuck in reasoning loops")

        # Delegation check
        if stats["delegations"] > stats["tool_uses"]:
            insights.append("🔄 More delegations than tool uses - check if delegation is efficient")

        # Duration check
        if stats["avg_event_duration_ms"] > 5000:
            insights.append(f"⏱️ Slow operations detected (avg {stats['avg_event_duration_ms']:.0f}ms)")

        if not insights:
            insights.append("✅ No performance issues detected")

        return insights

    def export_trace(self) -> str:
        """Export full event trace as formatted JSON"""
        trace_file = os.path.join(self.logs_dir, f"trace_{self.session_id}.json")

        trace_data = {
            "session_id": self.session_id,
            "statistics": self.get_statistics(),
            "insights": self.get_performance_insights(),
            "events": [asdict(e) for e in self.events]
        }

        with open(trace_file, 'w') as f:
            json.dump(trace_data, f, indent=2)

        return trace_file

    def print_summary(self):
        """Print formatted session summary"""
        from python.helpers.print_style import PrintStyle

        stats = self.get_statistics()
        insights = self.get_performance_insights()

        PrintStyle(bold=True, font_color="magenta", padding=True).print("=" * 50)
        PrintStyle(bold=True, font_color="magenta").print("📊 OBSERVABILITY SUMMARY")
        PrintStyle(bold=True, font_color="magenta", padding=True).print("=" * 50)

        PrintStyle(font_color="white").print(f"Session: {stats['session_id']}")
        PrintStyle(font_color="white").print(f"Total Events: {stats['total_events']}")
        PrintStyle(font_color="white").print(f"  LLM Calls: {stats['llm_calls']}")
        PrintStyle(font_color="white").print(f"  Tool Uses: {stats['tool_uses']}")
        PrintStyle(font_color="white").print(f"  Delegations: {stats['delegations']}")
        PrintStyle(font_color="red" if stats['errors'] > 0 else "green").print(f"  Errors: {stats['errors']}")
        PrintStyle(font_color="white").print(f"Success Rate: {stats['success_rate']}%")
        PrintStyle(font_color="white").print(f"Avg Duration: {stats['avg_event_duration_ms']:.2f}ms")

        PrintStyle(bold=True, font_color="cyan", padding=True).print("\n💡 INSIGHTS:")
        for insight in insights:
            PrintStyle(font_color="cyan").print(f"  {insight}")

        PrintStyle(bold=True, font_color="magenta", padding=True).print("=" * 50)


# Global instance
_global_logger: Optional[ObservabilityLogger] = None

def get_logger(session_id: str = None) -> ObservabilityLogger:
    """Get or create global observability logger"""
    global _global_logger
    if _global_logger is None or session_id:
        _global_logger = ObservabilityLogger(session_id)
    return _global_logger
