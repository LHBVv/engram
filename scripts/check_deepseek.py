"""最小脚本:验证 DeepSeek API key 是否可用。

用法:
    1. 复制 .env.example 为 .env,填入真实 DEEPSEEK_API_KEY
    2. uv run python scripts/check_deepseek.py

成功:打印 HTTP 200 与模型回复,exit 0。
失败:缺 key / 非 200 / 网络错误 → 打印原因,exit 1。
"""

import sys
from pathlib import Path

# 让脚本能 import 到 src/ 下的 config(应用式布局,src 不作为已安装包)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import httpx  # noqa: E402

from config import settings  # noqa: E402


def main() -> int:
    if not settings.deepseek_api_key:
        print("❌ DEEPSEEK_API_KEY 未设置。请在 .env 中填入真实 key 后重试。")
        return 1

    url = f"{settings.deepseek_base_url.rstrip('/')}/chat/completions"
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": "ping"}],
        "max_tokens": 8,
        "stream": False,
    }
    headers = {"Authorization": f"Bearer {settings.deepseek_api_key}"}

    try:
        resp = httpx.post(url, json=payload, headers=headers, timeout=30.0)
    except httpx.HTTPError as exc:
        print(f"❌ 网络请求失败:{type(exc).__name__}: {exc}")
        return 1

    if resp.status_code != 200:
        print(f"❌ HTTP {resp.status_code}: {resp.text[:500]}")
        return 1

    data = resp.json()
    reply = data["choices"][0]["message"]["content"]
    usage = data.get("usage", {})
    print("✅ HTTP 200 — DeepSeek key 可用")
    print(f"   模型回复: {reply!r}")
    print(f"   token 用量: {usage}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
