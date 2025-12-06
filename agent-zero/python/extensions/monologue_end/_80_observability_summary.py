from python.helpers.extension import Extension
from agent import LoopData

class ObservabilitySummary(Extension):
    """
    Display observability summary at the end of monologue
    Shows agent behavior insights and performance metrics
    """

    async def execute(self, tools_result: str = "", **kwargs):
        # Only show for Agent 0
        if self.agent.number != 0:
            return

        try:
            from python.helpers.observability import get_logger
            logger = get_logger()

            # Export trace file
            logger.export_trace()

            # Print summary (only if there were meaningful events)
            if logger.stats["total_events"] > 0:
                logger.print_summary()

        except ImportError:
            pass
        except Exception:
            # Silent fail
            pass
