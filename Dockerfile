FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple \
    -r requirements.txt

COPY src /app/src
COPY proxy /app/proxy

ENV PYTHONPATH=/app/src:/app/proxy

# 单 worker:内存状态是节点身份的一部分,多 worker 会破坏单点串行假设
CMD ["uvicorn", "leaderboard.node:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
