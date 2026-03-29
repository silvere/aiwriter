#!/usr/bin/env python3
"""
下载图片并保存到指定路径。
用法: python3 download_image.py <url> <output_path>
退出码: 0=成功, 1=失败
"""
import sys
import urllib.request
from pathlib import Path


def download(url: str, output_path: str) -> bool:
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
        "Referer": "https://unsplash.com/",
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as resp:
            content_type = resp.headers.get("Content-Type", "")
            if not any(t in content_type for t in ["image", "jpeg", "png", "webp", "gif"]):
                print(f"ERROR: Not an image (Content-Type: {content_type})", file=sys.stderr)
                return False

            data = resp.read()
            if len(data) < 1024:
                print(f"ERROR: File too small ({len(data)} bytes), likely not a valid image", file=sys.stderr)
                return False

            out.write_bytes(data)
            size_kb = len(data) // 1024
            print(f"OK: {out} ({size_kb}KB)")
            return True

    except urllib.error.HTTPError as e:
        print(f"ERROR: HTTP {e.code} - {url}", file=sys.stderr)
        return False
    except urllib.error.URLError as e:
        print(f"ERROR: URL failed - {e.reason}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return False


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法: python3 download_image.py <url> <output_path>", file=sys.stderr)
        sys.exit(1)

    success = download(sys.argv[1], sys.argv[2])
    sys.exit(0 if success else 1)
