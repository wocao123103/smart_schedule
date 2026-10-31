#!/usr/bin/env python3
"""智能日程助手（网页版）本地服务器：运行后手机连同一 Wi-Fi 即可打开/下载 index.html。

用法：
  python serve.py            # 默认端口 8000
  python serve.py 9000       # 自定义端口

启动后控制台会打印「本机地址」和「手机访问地址」。
手机浏览器打开手机地址即可使用；如需把网页存到手机，可用浏览器菜单“下载/添加到主屏幕”。
"""
import http.server
import socketserver
import socket
import sys
import os

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # 关闭缓存，避免更新后手机仍读旧文件
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, *args):
        pass


def lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()


if __name__ == "__main__":
    with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
        ip = lan_ip()
        print("=" * 48)
        print("智能日程助手（网页版）已启动")
        print(f"  本机访问:  http://127.0.0.1:{PORT}/")
        print(f"  手机访问:  http://{ip}:{PORT}/   (手机与电脑需连同一 Wi-Fi)")
        print("  按 Ctrl+C 停止")
        print("=" * 48)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n已停止。")
