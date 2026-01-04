import subprocess
import json

class McpClient:
    def __init__(self):
        self.process = subprocess.Popen(
            ["python", "mcp_server.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True
        )
        self.id = 0

    def search(self, query):
        self.id += 1
        request = {
            "jsonrpc": "2.0",
            "method": "search",
            "params": {"query": query},
            "id": self.id
        }

        self.process.stdin.write(json.dumps(request) + "\n")
        self.process.stdin.flush()

        response = self.process.stdout.readline()
        return json.loads(response)["result"]