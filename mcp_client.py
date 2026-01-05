import subprocess
import json
import time


class McpClient:
    def __init__(self):
        self.process = subprocess.Popen(
            ["python", "mcp_server.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        self.request_id = 0

    def search(self, query):
        self.request_id += 1

        request = {
            "jsonrpc": "2.0",
            "method": "search",
            "params": {"query": query},
            "id": self.request_id
        }

        self.process.stdin.write(json.dumps(request) + "\n")
        self.process.stdin.flush()

        start = time.time()
        while True:
            if time.time() - start > 5:
                raise TimeoutError("MCP Server Timeout")

            line = self.process.stdout.readline()
            if line:
                response = json.loads(line)
                if "error" in response:
                    return {"error": response["error"]}
                return {"result": response["result"]}
