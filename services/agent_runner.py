import asyncio
from google.antigravity import Agent, LocalAgentConfig, CapabilitiesConfig

class AgentRunner:
    def __init__(self):
        self.config = LocalAgentConfig(
            system_instructions="You are a helpful assistant responding to commands from a mobile app.",
            capabilities=CapabilitiesConfig()
        )
    
    async def process_message(self, text: str) -> str:
        async with Agent(self.config) as agent:
            response = await agent.chat(text)
            
            # Since the response stream tokens, we accumulate them.
            output = ""
            async for token in response:
                output += token
            return output

agent_runner = AgentRunner()
