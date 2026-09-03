import gradio as gr
import spaces
from fastapi.middleware.cors import CORSMiddleware
from routes.anonymize import router as anonymize_router

# Dummy function required to satisfy HF's ZeroGPU tier — not used for actual GPU work.
@spaces.GPU(duration=1)
def _dummy_gpu_check():
    return "ok"

with gr.Blocks() as demo:
    gr.Markdown("## Sentinel-PII Backend\nThis is the API server.")

app = demo.app

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(anonymize_router)

if __name__ == "__main__":
    demo.launch()