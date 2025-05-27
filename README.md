A stateless chat graph using LangGraph with console input/output. Supports a tool `get_current_time` which returns the current UTC time in ISO-8601 format.

The bot will start in console mode:

- Type any message and press Enter.
- Ask "What time is it?", and the bot will call `get_current_time` and print the UTC time.
- Ask anything else, and the bot will respond via the LLM.
