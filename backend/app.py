import gradio as gr
import spaces
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.anonymize import router as anonymize_router

@spaces.GPU(duration=1)
def _dummy_gpu_check():
    return "ok"

_dummy_gpu_check()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(anonymize_router)

@app.get("/")
def root():
    return {"status": "running"}

with gr.Blocks() as demo:
    gr.Markdown("## Sentinel-PII Backend")

app = gr.mount_gradio_app(app, demo, path="/ui")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)