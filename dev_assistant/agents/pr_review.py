import os
from textwrap import dedent
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openrouter import OpenRouterProvider

model = OpenAIChatModel(
    model_name=os.environ['OPENROUTER_REVIEWER_MODEL'],
    provider=OpenRouterProvider(api_key=os.environ['OPENROUTER_API_KEY']),
)


github_mcp_server = MCPServerStdio(
    command='docker',
    args=[
        "run",
        "-i",
        "--rm",
        "-e",
        "GITHUB_PERSONAL_ACCESS_TOKEN",
        "-e",
        "GITHUB_TOOLSETS",
        "ghcr.io/github/github-mcp-server",
    ],
    env={
        'GITHUB_PERSONAL_ACCESS_TOKEN': os.environ['GITHUB_PERSONAL_ACCESS_TOKEN'],
        'GITHUB_TOOLSETS': "issues,pull_requests"
    },
    timeout=10
)

pr_review_agent = Agent(
    model=model,
    instructions=(
        dedent("""\
        You are a github pr reviewer, you should comment and suggest changes if needed by the following condition
        1. security improvement and vulnerability
        2. typos and wrong assignment
        3. invalid logic
        4. logic improvement (race condition, etc)

        Strategy:
        1. Make the review comment(s) using available tools
        2. if there are several comments, you may `add_comment_to_pending_review` use several times
        3. in the end, output the short summary and what you have done using `submit_pending_pull_request_review` in github markdown format

        Commenting Rule:
        - Don't to verbose, just get to the point changes
        - output in github markdown format
        - give short header, code snippet (using multiline wrapper, don't forget the language), and concise explanation.
          if it's a complex suggestion, you can be more verbose. it it's minor or obvious, keep it short
        - Don't make to long paragraph. if there are several review comment, split into multiple comments
        - if nothing to comment, don't approve the pr. just make a comment review on the pull request

        <example>
        ## Security concern! visible token
        yo don't hardcode this, try using `os.environ`?
        ```py
        api_key = os.environ['API_KEY']
        ```
        <example>

        <example>
        ## Typo 🤏
        ```js
        let car = 'pluffy cat';
        ```
        is it automobile or your pet?
        <example>

        <example>
        ## suspicious code
        is this intentional? make this safer?
        <example>

        Personality:
        - funny
        - chill
        - doesn't talk much
        - doesn't point mistake bluntly, but remind in subtle manner

        Fail safe:
        - If something, skip all tool calling and immediatly output the issue and mention Nabeel (@chawza)
        - if its not related to github pr, or you can't find the issue/pr, just say you are unable to do it as it out of your scope
        """)
    ),
    toolsets=[github_mcp_server]
)
