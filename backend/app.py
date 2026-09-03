import gradio as gr
import spaces
from routes.anonymize import router as anonymize_router

# Dummy function to satisfy HF's ZeroGPU requirement — not actually used for GPU work.
@spaces.GPU(duration=1)
def _dummy_gpu_check():
    return "ok"

with gr.Blocks() as demo:
    gr.Markdown("## Sentinel-PII Backend\nThis is the API server. See `/docs` for the interactive API.")

app = demo.app
app.include_router(anonymize_router)

if __name__ == "__main__":
    demo.launch()