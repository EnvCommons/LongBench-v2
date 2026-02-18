import asyncio
import json
import os

from openai import AsyncOpenAI
from openreward import AsyncOpenReward


async def main() -> None:
    MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-5.2")
    OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

    or_client = AsyncOpenReward()
    oai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)

    # Local testing
    environment = or_client.environments.get(
        name="local/LongBenchV2",
        base_url="http://localhost:8080"
    )

    # Start with short split for faster testing
    tasks = await environment.list_tasks(split="short")
    tools = await environment.list_tools(format="openai")

    print(f"Found {len(tasks)} tasks in 'short' split")
    print(f"Testing first task...")

    # Test first task
    task = tasks[0]

    async with environment.session(task=task) as session:
        prompt = await session.get_prompt()
        print(prompt)

        input_list = [{
            "role": "user",
            "content": prompt[0].text
        }]

        finished = False
        turn = 0

        while not finished:
            turn += 1
            print(f"\n--- Turn {turn} ---")

            response = await oai_client.responses.create(
                model=MODEL_NAME,
                tools=tools,
                input=input_list
            )

            input_list += response.output

            for item in response.output:
                if item.type == "function_call":
                    print(f"Tool call: {item.name}")
                    print(f"Arguments: {item.arguments}")

                    tool_result = await session.call_tool(
                        item.name,
                        json.loads(str(item.arguments))
                    )

                    finished = tool_result.finished

                    input_list.append({
                        "type": "function_call_output",
                        "call_id": item.call_id,
                        "output": json.dumps({
                            "result": tool_result.blocks[0].text if tool_result.blocks else ""
                        })
                    })

                    print(f"Reward: {tool_result.reward}")
                    print(f"Result: {tool_result.blocks[0].text if tool_result.blocks else 'No message'}")

                    if tool_result.metadata:
                        print(f"Metadata: {tool_result.metadata}")

            # Break if no tool calls (shouldn't happen in this environment)
            if not any(i.type == "function_call" for i in response.output):
                print("No tool calls in response, ending session")
                break

        print(f"\nSession finished after {turn} turn(s)")


if __name__ == "__main__":
    asyncio.run(main())
