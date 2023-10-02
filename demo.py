import torch
import gradio as gr
import tiktoken
import boto3
import os
from pathlib import Path
from loguru import logger as log

import utils

import os

log = utils.Logger.create_sess("dev")

checkpoints = "checkpoints"
Path(checkpoints).mkdir(exist_ok=True)

BUCKET_NAME = 'gpt-model-scripted'
BUCKET_FILE_NAME = 'hp-gpt-tr.pt'
OUT_FILE_NAME = os.path.join(checkpoints, "hp-gpt-tr.pt")

if not os.path.exists(OUT_FILE_NAME):
    log.info("Downloading Model from s3...")

    s3 = boto3.client('s3',aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION_NAME"))

    s3.download_file(BUCKET_NAME, BUCKET_FILE_NAME, OUT_FILE_NAME)

    log.info("Model Downloaded successfully...")
else:
    log.info("Model already exists...")


log.info("Running Demo")

log.debug("Loading Model...")

model = torch.jit.load("checkpoints/hp-gpt-tr.pt")
model.eval()

log.debug(f"Model Loaded...")

log.debug("Loading tokenizer...")

cl100k_base = tiktoken.get_encoding("cl100k_base")

tokenizer = tiktoken.Encoding(
    name="cl100k_im",
    pat_str=cl100k_base._pat_str,
    mergeable_ranks=cl100k_base._mergeable_ranks,
    special_tokens={
        **cl100k_base._special_tokens,
        "<|im_start|>": 100264,
        "<|im_end|>": 100265,
})

log.debug("Tokenizer Loaded...")

def sentense_completion(text: str, max_tokens:float) -> str:

    encoded_text = tokenizer.encode(text)

    out = model.model.generate(torch.tensor(encoded_text).unsqueeze(0), max_new_tokens=int(max_tokens))
    
    log.info(f"Successfully Predicted...")
    
    return tokenizer.decode(out[0].cpu().numpy().tolist())

demo = gr.Interface(
    fn=sentense_completion,
    inputs=[gr.Textbox(lines=10, placeholder="Enter your text here..."), gr.Number(label="Max Tokens")],
    outputs="text"
)

demo.launch(server_name="0.0.0.0",server_port= 80)
