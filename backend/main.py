import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from engine import create_query_engine

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"])

query_engine = None


@app.on_event("startup")
def startup_event():
    global query_engine
    query_engine = create_query_engine()


@app.get('/health')
def health():
    return {
        "status": "ok" if query_engine is not None else "initializing",
        "query_engine_ready": query_engine is not None,
    }


@app.get('/stream_chat')
async def stream_chat(param: str = "你好"):
    if query_engine is None:
        raise HTTPException(status_code=503, detail="Query engine is not initialized")

    response_stream = query_engine.query(param)

    def generate():
        for text in response_stream.response_gen:
            yield text

    return StreamingResponse(generate(), media_type='text/event-stream')


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=5000)
