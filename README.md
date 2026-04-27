# LLM Observability Demo: Grafana + LangChain + Anthropic + OpenLit

A demo application showing how to instrument a LangChain/Anthropic Claude app with [OpenLit](https://openlit.io/) and ship telemetry to [Grafana Cloud](https://grafana.com/products/cloud/) via [Grafana Alloy](https://grafana.com/docs/alloy/).

## What it does

- Runs a LangChain agent using Claude (claude-opus-4-7) with two simple math tools (`add`, `multiply`)
- Auto-instruments all LLM calls with OpenLit (traces, metrics, logs via OpenTelemetry)
- Forwards telemetry through Grafana Alloy to Grafana Cloud
- Loops every 20 seconds, continuously generating telemetry for demonstration

## Architecture

```
app.py (LangChain + OpenLit)
    │
    ▼ OTLP/HTTP :4318
Grafana Alloy
    │
    ▼ OTLP/HTTPS
Grafana Cloud
```

## Prerequisites

- Docker and Docker Compose
- An [Anthropic API key](https://console.anthropic.com/)
- A [Grafana Cloud](https://grafana.com/products/cloud/) account (free tier works)

## Setup

1. Copy the environment template and fill in your credentials:

```bash
cp env.example .env
```

| Variable | Description |
|----------|-------------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key |
| `GRAFANA_CLOUD_OTLP_ENDPOINT` | Grafana Cloud OTLP endpoint (e.g. `https://otlp-gateway-prod-us-east-0.grafana.net/otlp`) |
| `GRAFANA_CLOUD_INSTANCE_ID` | Your Grafana Cloud instance ID |
| `GRAFANA_CLOUD_API_KEY` | Your Grafana Cloud API token (with MetricsPublisher + TracesPublisher roles) |

Optional variables (with defaults):

| Variable | Default | Description |
|----------|---------|-------------|
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `http://alloy:4318` | OTLP endpoint for the app to send telemetry to |
| `OPENLIT_APPLICATION_NAME` | `langchain-demo` | App name shown in Grafana |
| `OPENLIT_ENVIRONMENT` | `development` | Environment label |

2. Start the stack:

```bash
docker-compose up
```

This starts the Python app and Grafana Alloy together. The app will begin generating traces immediately.

## Running locally (without Docker)

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
python app.py
```

> When running locally, update `OTEL_EXPORTER_OTLP_ENDPOINT` to point to a locally running Alloy instance (e.g. `http://localhost:4318`).

## Viewing telemetry in Grafana

Once the app is running, open your Grafana Cloud instance and navigate to:

- **Explore → Traces** — view LLM invocation traces and tool calls
- **Explore → Metrics** — view token usage and latency metrics
- **Explore → Logs** — view LLM prompt/response logs

OpenLit also provides a pre-built [Grafana dashboard](https://grafana.com/grafana/dashboards/21988) you can import for an out-of-the-box LLM monitoring view.

## Project structure

```
.
├── app.py                  # Main app: LangChain agent with OpenLit instrumentation
├── alloy/
│   └── config.alloy        # Grafana Alloy OTEL collector config
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── env.example             # Environment variable template
```
