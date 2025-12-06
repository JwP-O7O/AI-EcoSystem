from python.helpers.extension import Extension
from agent import LoopData

class CostSummary(Extension):
    """
    Display cost summary and optimization insights at the end of each monologue
    Only shows for Agent 0 to avoid clutter
    """

    async def execute(self, tools_result: str = "", **kwargs):
        # Only show summary for main agent
        if self.agent.number != 0:
            return

        # Get the cost tracker if it exists
        try:
            from python.helpers.cost_tracker import get_tracker
            tracker = get_tracker()

            # Save session log
            tracker.save_session_log()

            # Print summary (only if there was meaningful usage)
            if tracker.session_stats.chat_model_calls > 0:
                tracker.print_summary()

        except ImportError:
            # Cost tracker not available
            pass
        except Exception as e:
            # Silent fail - don't interrupt agent operation
            pass
