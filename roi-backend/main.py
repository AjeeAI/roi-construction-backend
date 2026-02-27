from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from typing import AsyncGenerator
import json
from langgraph.graph import START, END, StateGraph, MessagesState
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# SOP-Driven System Prompt
ROI_SYSTEM_PROMPT = """You are the ROi Construction & Engineering AI Consultant. 
Your primary goal is to represent the 'Zero Guesswork' policy.

TECHNICAL STANDARDS TO ENFORCE:
- NO construction begins without soil assessment and structural validation.
- Prioritize 'Unseen Quality': foundations, rebar, and compaction.
- Emphasize 'Whole Life Costing' to explain long-term savings and ROI.
- Strictly prohibit skipping soil testing or rushing compaction.

If the user has technical inquiries beyond your scope, direct them to roiconstructionng@gmail.com."""

api_key = os.getenv("OPENAI_KEY")
llm = ChatOpenAI(model="gpt-4o", temperature=0.5, api_key=api_key)

# SOP-Driven System Prompt [cite: 1, 2, 3]
# This incorporates the ROi Philosophy and Technical Standards directly.
ROI_SYSTEM_PROMPT = """You are the ROi Construction & Engineering AI Consultant. 
Your primary goal is to represent the 'Zero Guesswork' policy.
If user asks about ROI, know that they mean ROI construction, not Return on Investment.
Also, don't answer questions that are not greetings or are unrelated to construction, and/or ROI construction. Instead, remind the user that you are a chatbot created specifically for ROi Construction & Engineering and direct them to roiconstructionng@gmail.com or tell them to use the contact form in the website.

CORE PHILOSOPHY:
- Zero Guesswork: Operate on a 100% precision mandate.
- Pre-Construction: No construction begins without rigorous planning, soil assessment, and structural validation.
- Unseen Quality: Prioritize structural elements eventually hidden like foundations, rebar, and compaction.

TECHNICAL STANDARDS:
- Lean Project Management: Use 'Whole Life Costing' to ensure long-term savings and guaranteed ROI.
- Prohibitions: Skipping soil testing or rushing compaction is strictly prohibited as it creates structural risks.
- Quality: Every beam, block, and brick must represent safety, honesty, and precision.

REGION: Nigeria, with active operations in Lagos and surrounding areas.
CONTACT: Direct technical inquiries to roiconstructionng@gmail.com."""

# Use a model with a long context window


RESPONSE_LIMIT = 4

def assistant_node(state: MessagesState):
    """Processes messages using the ROi SOP context with a response limit."""
    
    # Count how many responses the AI has already given in this thread
    ai_responses = [m for m in state["messages"] if isinstance(m, AIMessage)]
    
    if len(ai_responses) >= RESPONSE_LIMIT:
        # If limit reached, return a final instruction instead of calling the LLM
        limit_message = (
            "The limit for this initial AI consultation has been reached. For detailed project assessment and structural validation, please contact ROi Construction directly at roiconstructionng@gmail.com or via the contact form."
        )
        return {"messages": [AIMessage(content=limit_message)]}

    # Otherwise, proceed with the standard ROi Philosophy [cite: 1, 3]
    messages = [SystemMessage(content=ROI_SYSTEM_PROMPT)] + state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}

# Build the Graph
builder = StateGraph(MessagesState)
builder.add_node("assistant", assistant_node)
builder.add_edge(START, "assistant")
builder.add_edge("assistant", END)

# Add memory to persist state across turns
memory = MemorySaver()
agent = builder.compile(checkpointer=memory)

class ChatRequest(BaseModel):
    message: str
    thread_id: str


@app.get('/')
def read_root():
    return {"message": "Welcome to the ROi Construction & Engineering AI Consultant API!"}

@app.get('/health')
def health_check():
    return {"status": "ok"}

@app.post("/chat")
async def chat(request: ChatRequest):
    config = {"configurable": {"thread_id": request.thread_id}}
    
    async def stream_generator() -> AsyncGenerator[str, None]:
        # astream allows us to yield tokens as they arrive
        async for msg, metadata in agent.astream(
            {"messages": [HumanMessage(content=request.message)]},
            config=config,
            stream_mode="messages"
        ):
            # We filter for AIMessage chunks coming from the assistant node
            if isinstance(msg, AIMessage) and msg.content:
                yield msg.content

    return StreamingResponse(stream_generator(), media_type="text/plain")