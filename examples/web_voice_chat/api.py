# %%
# a fastapi api running on localhost:8080 that calls a python function
from dotenv import load_dotenv
load_dotenv(override=True) # noqa
from workbench.voice import speak
from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import base64
from workbench.transcriber import audio_bytes_to_text
from workbench.LLM import Chat
from pprint import pprint


import os

print(os.getenv("OPENAI_API_KEY"))

origins = [
    "http://localhost",
    "http://localhost:8080",
]
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class Payload(BaseModel):
    audio: str # base64 encoded audio bytes
    messages: str # the messages so far


# @app.post("/chat")
# async def chat(text: Text):
#     print("Processing...")
#     response = text.text
#     audio = speak(response, voice="Nicole", _stream=False, play=False)
#     print(audio)
#     audio = base64.b64encode(audio).decode()

#     return json.dumps({"audio": audio})

system_message = "You are a helpful assistant"



@app.post("/listen")
async def listen(payload: Payload):
    
    chat = Chat(system_message=system_message)

    print("Transcribing...")
    # decode base64 string audio
    # print(audio.audio)
    audio = payload.audio
    audio = base64.b64decode(
        audio)

    # print('audio bytes:', audio[:10])
    # audio = io.BytesIO(audio)
    # # transcribe using whisper API
    text = audio_bytes_to_text(audio)
    print(text)
    
    print("Thinking...")
    
    messages = payload.messages
    messages = json.loads(messages)
    
    message = {"role": "user", "content": text}
    messages.append(message)
    chat.messages.extend(messages) # add chat history to chat
    
    response = chat(text)

    chat.messages.append({"role": "assistant", "content": response})

    print("Generating speech...")
    # response = text.text
    audio = speak(response, voice="Nicole", play=False)
    # print(audio)
    audio = base64.b64encode(audio).decode()

    pprint

    return json.dumps({"audio": audio, "messages": chat.messages})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)

# %%
