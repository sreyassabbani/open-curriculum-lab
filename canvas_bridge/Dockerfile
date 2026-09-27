FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

COPY canvas_bridge/requirements.txt /app/canvas_bridge/requirements.txt
RUN python -m pip install --no-cache-dir -r /app/canvas_bridge/requirements.txt

ARG TUNNEL_VERSION=v0.0.15
ARG TUNNEL_SHA256=8c836dc5d68d68b663d9a5c5b28ff9fa780d9f7a3fffb1c306880b8f32fab5f1
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl unzip && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://github.com/openai/tunnel-client/releases/download/${TUNNEL_VERSION}/tunnel-client-${TUNNEL_VERSION}-linux-amd64.zip" -o /tmp/tunnel.zip && echo "${TUNNEL_SHA256}  /tmp/tunnel.zip" | sha256sum -c - && mkdir /tmp/tunnel && unzip -q /tmp/tunnel.zip -d /tmp/tunnel && find /tmp/tunnel -type f -name tunnel-client -exec install -m 0755 {} /usr/local/bin/tunnel-client \; && test -x /usr/local/bin/tunnel-client && rm -rf /tmp/tunnel /tmp/tunnel.zip

COPY .agents/skills/build-math1554-lesson/scripts/canvas_lesson.py /app/.agents/skills/build-math1554-lesson/scripts/canvas_lesson.py
COPY .agents/skills/build-math2551-lesson/scripts/canvas_lesson.py /app/.agents/skills/build-math2551-lesson/scripts/canvas_lesson.py
COPY canvas_bridge/server.py /app/canvas_bridge/server.py
COPY canvas_bridge/run.sh /app/canvas_bridge/run.sh
RUN chmod 0755 /app/canvas_bridge/run.sh && useradd --create-home app && chown -R app:app /app
USER app

ENTRYPOINT ["/app/canvas_bridge/run.sh"]
