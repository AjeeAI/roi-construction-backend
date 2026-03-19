# 🏗️ ROi Construction & Engineering AI Consultant - Backend

**ROi Construction AI Backend** is a specialized FastAPI application that powers an intelligent, SOP-driven AI consultant for ROi Construction & Engineering. Built with LangGraph and OpenAI, this system enforces the company's core philosophies—such as the "Zero Guesswork" policy and the prioritization of "Unseen Quality"—while guiding prospective clients and answering construction-related inquiries.

## ✨ Key Features

* **SOP-Driven AI Agent:** Utilizes a LangGraph `StateGraph` and OpenAI's `gpt-4o` to act as a strict consultant. It is programmed to emphasize structural validation, soil assessment, and "Whole Life Costing" while rejecting non-construction inquiries.
* **Response Limiting & Lead Generation:** Implements a strict conversation limit (default: 4 AI responses per thread). Once the limit is reached, it seamlessly directs users to contact `roiconstructionng@gmail.com` for a detailed project assessment, effectively acting as a lead generation funnel.
* **Streaming Responses:** The `/chat` endpoint uses asynchronous generators and `StreamingResponse` to stream AI tokens back to the client in real-time.
* **Persistent Thread Memory:** Leverages LangGraph's `MemorySaver` to maintain conversational context and state across user sessions based on `thread_id`.
* **Automated SOP Generation:** Includes a standalone Python script (`pdf_down.py`) utilizing the `fpdf` library to programmatically generate the official ROi Construction Internal SOP document (`ROi_SOP.pdf`).

## 🏗️ System Architecture

* **`main.py`:** The core FastAPI application containing the LangGraph builder, routing, and the system prompt enforcing the company's construction standards.
* **`pdf_down.py`:** A utility script to generate the foundational logic and rules engine into a physical PDF document.
* **Dockerized Environment:** The repository includes a `docker-compose.yml` for rapid, consistent deployment with live-reloading enabled via Uvicorn.

## 🛠️ Tech Stack

* **Framework:** Python, FastAPI, Uvicorn
* **AI & Orchestration:** LangChain, LangGraph, OpenAI (`gpt-4o`)
* **Data Models:** Pydantic
* **Deployment:** Docker, Docker Compose
* **Utilities:** `fpdf` for document generation, `python-dotenv` for environment management.

## 🚀 Getting Started

### Prerequisites
* Python 3.11+ or Docker
* OpenAI API Key

### Installation & Execution (Docker)

1.  **Clone the repository and set up environment variables:**
    Create a `.env` file in the `roi-backend` directory and add your key:
    ```env
    OPENAI_KEY=your_api_key_here
    ```

2.  **Run with Docker Compose:**
    ```bash
    docker-compose up --build
    ```
    The API will be available at `http://localhost:8000` with hot-reloading enabled.

### Installation (Manual)

1.  **Install dependencies:**
    ```bash
    cd roi-backend
    pip install -r requirements.txt
    ```
2.  **Run the server:**
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    ```

## 📡 API Endpoints

* `GET /` - Root endpoint to verify the API is running.
* `GET /health` - Health check endpoint returning status `ok`.
* `POST /chat` - Expects a JSON payload `{"message": "string", "thread_id": "string"}`. Streams back the AI consultant's response in `text/plain` format.
