## Getting Started


### Create or open folder where you want to create MCP server

### Installing uv Package Manager

On MacOS/Linux:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Make sure to restart your terminal afterwards to ensure that the `uv` command gets picked up.

### Project Setup

1. Create and initialize the project:
```bash
# Create a new directory for our project
uv init mcp-server
cd mcp-server

# Create virtual environment and activate it
uv venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

# Install dependencies
uv add "mcp[cli]" httpx
```
2. Copy code from mcp-server-creation.py

3. Create the server implementation file:
```bash
touch main.py
```

### Running the Server

1. Start the MCP server:
```bash
uv run main.py
```

2. The server will start and be ready to accept connections

## Connecting to Claude Desktop or Cursor ai ide

For claude desktop
1. Install Claude Desktop from the official website
2. Configure Claude Desktop to use your MCP server:

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

For cursor ai
1. Install cursor ai
2. Open Cursor > Preferences > Cursor settings
3. Go to MCP
4. Click "Add new global mcp server"

```json
{
    "mcpServers": {
        "mcp-server": {
            "command": "uv",  # It's better to use the absolute path to the uv command
            "args": [
                "--directory",
                "/ABSOLUTE/PATH/TO/YOUR/mcp-server",
                "run",
                "main.py"
            ]
        }
    }
}
```

3. Restart Claude Desktop

## Troubleshooting

If your server isn't being picked up by Claude Desktop:

1. Check the configuration file path and permissions
2. Verify the absolute path in the configuration is correct
3. Ensure uv is properly installed and accessible
4. Check Claude Desktop logs for any error messages