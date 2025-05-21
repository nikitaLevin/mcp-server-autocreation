from mcp.server.fastmcp import FastMCP
import subprocess
import os
import sys
from pathlib import Path

mcp = FastMCP("Creation")

@mcp.tool()
def create_mcp_server(project_name: str, project_location: str, server_description: str = "Custom MCP Server") -> str:
    """
    Automatically creates an MCP server based on the instructions.
    
    Args:
        project_name: The name of the MCP server project to create
        project_location: The location of the MCP server project to create
        server_description: A brief description of what your server does
        
    Returns:
        A message indicating the result of the server creation process
    """
    result_log = []
    
    # Expand user directory if needed (e.g., ~/projects)
    project_location = os.path.expanduser(project_location)
    
    # Create project location directory if it doesn't exist
    if not os.path.exists(project_location):
        try:
            os.makedirs(project_location)
            result_log.append(f"✅ Created directory: {project_location}")
        except Exception as e:
            return f"❌ Failed to create directory {project_location}: {str(e)}"
    
    # Remember original directory
    original_dir = os.getcwd()
    
    # Check if uv is installed
    try:
        subprocess.run(["uv", "--version"], check=True, capture_output=True)
        result_log.append("✅ uv package manager is installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        # If uv is not installed, install it
        result_log.append("Installing uv package manager...")
        try:
            if sys.platform == "darwin" or sys.platform.startswith("linux"):
                subprocess.run(
                    ["curl", "-LsSf", "https://astral.sh/uv/install.sh"],
                    stdout=subprocess.PIPE,
                    check=True
                ).stdout | subprocess.run(["sh"], check=True)
                result_log.append("✅ uv package manager installed successfully")
            else:
                return "❌ Automatic installation of uv is only supported on MacOS and Linux. Please install uv manually."
        except subprocess.CalledProcessError:
            return "❌ Failed to install uv package manager. Please install it manually."
    
    # Create project directory
    project_dir = Path(project_location) / project_name
    if project_dir.exists():
        return f"❌ Directory {project_dir} already exists. Please choose a different name or location."
    
    project_dir.mkdir(parents=True)
    result_log.append(f"✅ Created project directory: {project_dir}")
    
    # Change to project directory
    os.chdir(project_dir)
    
    # Initialize the project with uv
    try:
        subprocess.run(["uv", "init"], check=True, capture_output=True)
        result_log.append("✅ Initialized uv project")
    except subprocess.CalledProcessError:
        os.chdir(original_dir)  # Return to original directory before exiting
        return "❌ Failed to initialize uv project"
    
    # Create and activate virtual environment
    try:
        subprocess.run(["uv", "venv"], check=True, capture_output=True)
        result_log.append("✅ Created virtual environment")
    except subprocess.CalledProcessError:
        os.chdir(original_dir)  # Return to original directory before exiting
        return "❌ Failed to create virtual environment"
    
    # Install dependencies
    try:
        subprocess.run(["uv", "add", "mcp[cli]", "httpx"], check=True, capture_output=True)
        result_log.append("✅ Installed required dependencies")
    except subprocess.CalledProcessError:
        os.chdir(original_dir)  # Return to original directory before exiting
        return "❌ Failed to install dependencies"
    
    # Create main.py with basic MCP server implementation
    main_py_content = f"""from mcp.server.fastmcp import FastMCP

mcp = FastMCP("{server_description}")

@mcp.tool()
def example_tool(input_text: str) -> str:
    \"\"\"An example tool that echoes back the input text\"\"\"
    return f"You said: {{input_text}}"

if __name__ == "__main__":
    mcp.run(transport="stdio")
"""
    
    with open("main.py", "w") as f:
        f.write(main_py_content)
    result_log.append("✅ Created main.py with basic MCP server implementation")
    
    # Create README.md with usage instructions
    readme_content = f"""# {project_name}

{server_description}

## Running the Server

1. Activate the virtual environment:
   ```bash
   # On macOS/Linux:
   source .venv/bin/activate
   
   # On Windows:
   .venv\\Scripts\\activate
   ```

2. Start the MCP server:
   ```bash
   uv run main.py
   ```

## Connecting to Claude Desktop

1. Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{{
    "mcpServers": {{
        "{project_name}": {{
            "command": "uv",
            "args": [
                "--directory",
                "{os.path.abspath('.')}",
                "run",
                "main.py"
            ]
        }}
    }}
}}
```

2. Restart Claude Desktop

## Connecting to Cursor AI IDE

1. Open Cursor > Preferences > Cursor settings
2. Go to MCP
3. Click "Add new global mcp server"
4. Configure with the following:
   - Command: uv
   - Arguments: --directory {os.path.abspath('.')} run main.py
"""
    
    with open("README.md", "w") as f:
        f.write(readme_content)
    result_log.append("✅ Created README.md with usage instructions")
    
    # Return to original directory
    os.chdir(original_dir)
    
    # Compile final result message
    result_message = f"""
MCP Server created successfully!

Project: {project_name}
Location: {project_dir.absolute()}

To run your server:
1. cd {project_dir}
2. source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate
3. uv run main.py

Setup log:
{"".join([f"- {log}\n" for log in result_log])}
"""
    
    return result_message

if __name__ == "__main__":
    mcp.run(transport="stdio") 