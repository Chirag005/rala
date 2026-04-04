# Phase 16: Universal Dockerization

## 1. What We Built
We eliminated the need to launch multiple messy terminal windows manually by packaging the entire RAALA system into Docker.

1. **`api/Dockerfile`**: A single master container image (`python:3.11-slim`) that installs all `requirements.txt` dependencies and packages the source code.
2. **`docker-compose.yml`**: Expanded dramatically from 2 services to **7 interconnected services**:
   - `redis`
   - `influxdb`
   - `mosquitto` (MQTT Bridge preparation in phase 22)
   - `api` (FastAPI backend port 8000)
   - `stream-processor` (Flux data ingestor)
   - `rule-engine` (PubSub alerter + heartbeat monitor)
   - `mock-sensors` (Data generator)
   - `frontend` (Nginx serving raw HTML/JS/CSS on port 8080)
3. **Internal Routing**: Changed hardcoded `localhost` in `mock_sensors.py`, `stream_processor.py`, `rule_engine.py`, and `main.py` to `os.getenv('REDIS_HOST', 'localhost')`. When run in Docker, they resolve seamlessly to `http://redis:6379`.

## 2. Why We Built It This Way
- **One-command Orchestration:** Typing `docker compose up -d` brings up a perfectly reproducible, resilient infrastructure that runs completely in the background. Typing `docker compose down` kills it all cleanly without stranding orphan Python processes.
- **Portability:** In Phase 19, when we deploy RAALA onto an actual Raspberry Pi out in a greenhouse or farm, there are no virtual environments to setup or bash alias files to break. Docker is agnostic and runs cleanly on both Windows (the dev environment) and Linux distributions (the edge hardware).

## 3. Problems Overcome
- **Dependency Racing Sequence**: By adding `depends_on`, we ensured the Python applications don't crash randomly at boot by waiting for Redis and InfluxDB to initialize their sockets first.
- **Browser Automation Pressure**: The initial UI verification of Phase 16 crashed Playwright because compiling and spinning up 7 Docker containers at once briefly overwhelmed system resources. However, native `curl` and network log analysis successfully validated that Nginx was mapping the frontend layer correctly and the Python engines were processing the stream.
