# Supertrader

Supertrader is an autonomous cryptocurrency trading system for Binance spot markets. It supports live, paper and backtest modes and includes a Streamlit dashboard for monitoring and control.

> **Disclaimer**
> This project is provided for educational purposes only and does **not** constitute financial advice. Use at your own risk.

## Setup

### Requirements
* Python 3.12+
* Docker (for containerised deployment)

### Installation

```bash
make install
```

The dependencies are version pinned in `requirements.txt` to ensure
reproducible environments.

### Environment Variables

| Variable | Description |
|----------|-------------|
| `BINANCE_API_KEY` | Binance API key |
| `BINANCE_API_SECRET` | Binance API secret |
| `DATABASE_URL` | PostgreSQL connection string |
| `MAX_RISK_PCT` | Fraction of account balance allowed per trade (0.0-1.0) |

### Running

Run the dashboard locally:

```bash
make run
```

Run inside Docker:

```bash
docker-compose up
```

## Architecture

The architecture diagram is defined in `docs/architecture.mmd`.
Generate a PNG with:

```bash
make diagram
```

The generated file will be located at `docs/architecture.png`.

## Testing

Run unit tests with:

```bash
make test
```
