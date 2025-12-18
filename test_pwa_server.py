"""
NutriSnap PWA 测试服务器

这个简单的HTTP服务器用于测试PWA功能（无需Streamlit）。

## 使用方法

1. 运行此脚本:
   ```bash
   python test_pwa_server.py
   ```

2. 在浏览器中打开: http://localhost:8000

3. 在Chrome DevTools中:
   - 打开 Application 标签
   - 检查 Manifest
   - 检查 Service Workers
   - 测试安装提示

## 注意

这只是用于测试PWA基础设施（manifest.json, sw.js, icons）。
完整的应用功能需要运行Streamlit: `streamlit run app.py`
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

class PWAHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # 添加PWA所需的CORS和缓存头
        self.send_header('Cache-Control', 'no-cache')
        self.send_header('Access-Control-Allow-Origin', '*')
        SimpleHTTPRequestHandler.end_headers(self)

    def do_GET(self):
        # 路由测试页面
        if self.path == '/':
            self.path = '/test_pwa.html'
        return SimpleHTTPRequestHandler.do_GET(self)

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    port = 8000
    print(f"🌐 PWA测试服务器启动在 http://localhost:{port}")
    print(f"📱 在Chrome中打开上述URL，然后查看Application标签验证PWA配置")
    print(f"⏹️  按 Ctrl+C 停止服务器\n")
    
    httpd = HTTPServer(('localhost', port), PWAHandler)
    httpd.serve_forever()
