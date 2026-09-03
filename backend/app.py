import gradio as gr
from fastapi.middleware.cors import CORSMiddleware
from routes.anonymize import router as anonymize_router

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