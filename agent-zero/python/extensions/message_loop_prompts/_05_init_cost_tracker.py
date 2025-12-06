from python.helpers.extension import Extension
from agent import Agent, LoopData

class InitCostTracker(Extension):
    """
    Initialize cost tracker for the session
    Runs once at the beginning of the first message loop
    """

    async def execute(self, loop_data: LoopData = LoopData(), **kwargs):
        # Only initialize for Agent 0 and only on first iteration
        if self.agent.number != 0 or loop_data.iteration != 0:
            return

        # Initialize cost tracker if not already done
        if not hasattr(self.agent.context, 'cost_tracker'):
            try:
                from python.helpers.cost_tracker import get_tracker
                self.agent.context.cost_tracker = get_tracker(self.agent.context.id)

                # Also monkey-patch the agent to log token usage
                self._patch_agent_for_tracking()
            except ImportError:
                # Cost tracker module not available, skip
                pass

    def _patch_agent_for_tracking(self):
        """
        Add cost tracking to agent's LLM calls
        Non-invasive monkey-patching approach
        """
        original_rate_limiter_set_output = self.agent.rate_limiter.set_output_tokens

        def tracked_set_output_tokens(tokens: int):
            # Call original method
            original_rate_limiter_set_output(tokens)

            # Log to cost tracker
            if hasattr(self.agent.context, 'cost_tracker'):
                try:
                    # Estimate input tokens from last call
                    input_tokens = getattr(self.agent.rate_limiter, '_last_input_tokens', 0)

                    # Determine model name (fallback to "unknown")
                    model_name = "unknown"
                    if hasattr(self.agent.config.chat_model, 'model_name'):
                        model_name = self.agent.config.chat_model.model_name
                    elif hasattr(self.agent.config.chat_model, 'model'):
                        model_name = self.agent.config.chat_model.model

                    self.agent.context.cost_tracker.log_usage(
                        agent_name=self.agent.agent_name,
                        model_name=model_name,
                        model_type="chat",
                        input_tokens=input_tokens,
                        output_tokens=tokens,
                        task_description=f"Iteration {getattr(self.agent, '_current_iteration', 0)}"
                    )
                except Exception:
                    # Silent fail
                    pass

        # Also track input tokens
        original_rate_limiter_limit_call = self.agent.rate_limiter.limit_call_and_input

        def tracked_limit_call_and_input(input_tokens: int):
            # Store for later use
            self.agent.rate_limiter._last_input_tokens = input_tokens
            # Call original
            return original_rate_limiter_limit_call(input_tokens)

        # Apply patches
        self.agent.rate_limiter.set_output_tokens = tracked_set_output_tokens
        self.agent.rate_limiter.limit_call_and_input = tracked_limit_call_and_input
