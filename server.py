#!/usr/bin/env python3
"""
JLPT Mock Test Local Development Server
Serves static web files and proxies /api/send-score requests to Telegram Bot API.
Run with: python server.py
"""

import http.server
import socketserver
import json
import urllib.request
import urllib.error
import os
import sys

# Ensure UTF-8 output on Windows consoles
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

PORT = 8000

class JLPTMockTestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/send-score':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            try:
                payload = json.loads(post_data.decode('utf-8'))
                bot_token = payload.get('botToken') or os.environ.get('TELEGRAM_BOT_TOKEN')
                chat_id = payload.get('chatId') or os.environ.get('TELEGRAM_CHAT_ID')
                message = payload.get('message', '')

                if not bot_token or not chat_id:
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Missing Telegram botToken or chatId"}).encode('utf-8'))
                    return

                tg_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
                tg_payload = json.dumps({
                    "chat_id": chat_id,
                    "text": message,
                    "parse_mode": "Markdown"
                }).encode('utf-8')

                req = urllib.request.Request(
                    tg_url,
                    data=tg_payload,
                    headers={'Content-Type': 'application/json'},
                    method='POST'
                )

                with urllib.request.urlopen(req) as response:
                    res_body = response.read()
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(res_body)

            except urllib.error.HTTPError as e:
                err_body = e.read()
                self.send_response(e.code)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(err_body)

            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
        else:
            self.send_error(444, "Endpoint not found")

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

if __name__ == '__main__':
    web_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(web_dir)
    
    with socketserver.TCPServer(("", PORT), JLPTMockTestHandler) as httpd:
        print("==================================================")
        print(" [JLPT Mock Test System] Local Server Running!")
        print(f" Access in browser: http://localhost:{PORT}")
        print(" Press Ctrl+C to stop the server")
        print("==================================================")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")

