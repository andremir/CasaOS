from fastapi import FastAPI
import gradio as gr
import threading
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
def read_item(name: str):
    return {"message": f"Hello {name}"}

# Gradio interface functions
def get_hello_world():
    return "Hello World"

def get_personalized_greeting(name):
    if not name.strip():
        return "Please enter a name"
    return f"Hello {name}"

# Create Gradio interface
with gr.Blocks(title="CasaOS API Interface", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# CasaOS API Interface")
    gr.Markdown("A user-friendly interface for the CasaOS API endpoints")
    
    with gr.Tab("Hello World"):
        gr.Markdown("### Get Hello World Message")
        hello_btn = gr.Button("Get Hello World", variant="primary")
        hello_output = gr.Textbox(label="Response", interactive=False)
        hello_btn.click(fn=get_hello_world, outputs=hello_output)
    
    with gr.Tab("Personalized Greeting"):
        gr.Markdown("### Get Personalized Greeting")
        name_input = gr.Textbox(label="Enter your name", placeholder="Type your name here...")
        greeting_btn = gr.Button("Get Greeting", variant="primary")
        greeting_output = gr.Textbox(label="Response", interactive=False)
        
        greeting_btn.click(fn=get_personalized_greeting, inputs=name_input, outputs=greeting_output)
        name_input.submit(fn=get_personalized_greeting, inputs=name_input, outputs=greeting_output)

# Mount Gradio app
app = gr.mount_gradio_app(app, demo, path="/ui")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)