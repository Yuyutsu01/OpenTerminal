# OpenTerminal (The Hummingbird Project)

> **A High-Density, Cinematic Trading Terminal Blueprint**

OpenTerminal is an open-source architectural blueprint for building a professional, high-performance financial desktop application. It is designed to mimic the core user experience of top-tier trading platforms (like Interactive Brokers TWS or Bloomberg) using modern web technologies. 

## 🚀 The Vision

The goal is to demystify complex financial UI/UX and provide a learning sandbox for financial engineers, developers, and designers. 

The terminal utilizes a dark, cinematic aesthetic—deep slate backgrounds, high-contrast typography (green/red indicators), and information-dense panels that can be arranged and interacted with via a keyboard-driven command palette.

## 🏗️ System Architecture

The project is split into a high-performance Single Page Application (SPA) frontend and an asynchronous Python backend.

### 1. Frontend (React) - *Planned*
*   **Grid Workspace**: Resizable, drag-and-drop panels.
*   **Modules**:
    *   **Charts**: Interactive candlestick and volume charts via TradingView Lightweight Charts.
    *   **Watchlist**: Real-time data grid for streaming quotes.
    *   **Order Entry**: A mock trade submission ticket.
    *   **Activity**: Open orders and portfolio tracking.
    *   **News**: Streaming financial headlines.

### 2. Backend (FastAPI)
The backend acts as a high-speed data router and mock execution engine.
*   **API Gateway**: Standard REST endpoints for historical data and configuration.
*   **WebSocket Manager**: Pushes live quotes, order updates, and news to the frontend.
*   **Market Data Service**: Integrates with free-tier APIs (e.g., Yahoo Finance, Polygon) for quotes and historical bars.
*   **Order Management System (OMS)**: Simulates trade execution and portfolio state.

## 💻 Technology Stack

*   **Frontend**: React (Vite), Tailwind CSS, Zustand (State), React-Grid-Layout
*   **Backend**: Python, FastAPI, Uvicorn, WebSockets
*   **Data Sources**: `yfinance` (MVP mock data), standard REST/RSS feeds.
*   **Database**: SQLite (MVP) migrating to PostgreSQL.

## 🛠️ Getting Started (Backend)

We are currently scaffolding the backend architecture. 

### Prerequisites
*   Python 3.9+

### Setup

1.  Navigate to the backend directory:
    ```bash
    cd backend
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3.  Start the FastAPI Server:
    ```bash
    uvicorn main:app --reload
    ```
    The server will start at `http://localhost:8000`. You can view the API documentation at `http://localhost:8000/docs`.

## 🗺️ Roadmap

- [x] Define System Architecture & Modules
- [x] Scaffold FastAPI Backend Engine
- [ ] Implement WebSocket Manager for streaming quotes
- [ ] Scaffold React (Vite) Frontend with Tailwind
- [ ] Build Chart & Watchlist Panel UI
- [ ] Integrate mock OMS (Order Management System)
- [ ] Build global Command Bar (Omnibox)

---
*Disclaimer: This project is for educational purposes only. It does not connect to real brokerage accounts and uses delayed/mock data.*
