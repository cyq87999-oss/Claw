#!/usr/bin/env python3
"""
图生视频分镜提示词工具 —— 本地启动器（同源代理）
- 托管当前目录的 index.html 等静态文件
- 反向代理（让网页与 API 同域，绕开浏览器 CORS）：
    /ollama/*      -> http://localhost:11434   （本机 Ollama）
    /ollamacloud/* -> https://ollama.com       （Ollama 云端）

用法：  python3 serve.py            # 默认 8000 端口
        python3 serve.py 9000       # 指定端口
然后浏览器打开 http://localhost:8000/index.html
"""
import sys, os, http.server, socketserver, urllib.request, urllib.error

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
ROUTES = {
    "/ollama/": "http://localhost:11434",
    "/ollamacloud/": "https://ollama.com",
}
ROOT = os.path.dirname(os.path.abspath(__file__))


class Handler(http.server.SimpleHTTPRequestHandler):
    def _route(self):
        for prefix, upstream in ROUTES.items():
            if self.path.startswith(prefix):
                return prefix, upstream
        return None

    def _proxy(self):
        m = self._route()
        if not m:
            self.send_error(404)
            return
        prefix, upstream = m
        target = upstream + self.path[len(prefix) - 1:]
        length = int(self.headers.get("Content-Length", 0) or 0)
        body = self.rfile.read(length) if length else None
        req = urllib.request.Request(target, data=body, method=self.command)
        for h in ("Content-Type", "Authorization", "Accept"):
            v = self.headers.get(h)
            if v:
                req.add_header(h, v)
        try:
            resp = urllib.request.urlopen(req, timeout=600)
            data = resp.read()
            self.send_response(resp.status)
            self.send_header("Content-Type", resp.headers.get("Content-Type", "application/json"))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        except urllib.error.HTTPError as e:
            data = e.read()
            self.send_response(e.code)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Type", e.headers.get("Content-Type", "application/json"))
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        except Exception as e:  # noqa
            self.send_error(502, "proxy error: %s" % e)

    def do_GET(self):
        if self._route():
            self._proxy()
        else:
            super().do_GET()

    def do_POST(self):
        if self._route():
            self._proxy()
        else:
            self.send_error(405)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    os.chdir(ROOT)
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("✅ 已启动：http://localhost:%d/index.html" % PORT)
        print("   静态托管 + 代理: /ollama/* -> 本机 Ollama, /ollamacloud/* -> ollama.com")
        print("   Ctrl+C 退出")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n已停止")
