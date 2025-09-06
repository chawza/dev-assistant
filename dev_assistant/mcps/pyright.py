from pydantic_ai.mcp import MCPServerStdio


def create_pyright_mcp_server(mcm_language_server_bin: str, workspace: str):
    return MCPServerStdio(
        command=mcm_language_server_bin,
        args=[
            '--workspace',
            workspace,
            '--lsp',
            'pyright-langserver',
            '--',
            '--stdio',
        ],
        timeout=10
    )
