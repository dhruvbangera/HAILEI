"""
Simple HTTP server for HAILEI agents - no external dependencies
For testing the n8n workflow integration
"""

import http.server
import socketserver
import json
import urllib.parse
from datetime import datetime
from test_workflow import MockIPDAi, MockCAuthAi, MockSearchAi

class HAILEIRequestHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.ipdai = MockIPDAi()
        self.cauthai = MockCAuthAi()
        self.searchai = MockSearchAi()
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "agents": ["ipdai", "cauthai", "searchai"]
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        """Handle POST requests"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON")
            return
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        if self.path == '/ipdai':
            result = self.ipdai.process_course_input(data)
        elif self.path == '/cauthai':
            result = self.cauthai.process_ipdai_output(data)
        elif self.path == '/searchai':
            result = self.searchai.process_cauthai_output(data)
        else:
            result = {"error": f"Unknown endpoint: {self.path}"}
        
        self.wfile.write(json.dumps(result, indent=2).encode())
    
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def start_server(port=8000):
    """Start the HAILEI API server"""
    handler = HAILEIRequestHandler
    
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"🚀 HAILEI Agent API Server running on port {port}")
        print(f"📍 Endpoints:")
        print(f"   http://localhost:{port}/ipdai")
        print(f"   http://localhost:{port}/cauthai")
        print(f"   http://localhost:{port}/searchai")
        print(f"   http://localhost:{port}/health")
        print(f"✋ Press Ctrl+C to stop")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped")

if __name__ == "__main__":
    start_server()