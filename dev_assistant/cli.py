import asyncio
import typer
from dev_assistant.agents.pr_review import pr_review_agent


app = typer.Typer()

@app.command()
def review_pr(user_prompt: str):

    async def _review_pr(user_prompt: str):
        result = await pr_review_agent.run(user_prompt=user_prompt)
        print(result.output)

    asyncio.run(_review_pr(user_prompt))
