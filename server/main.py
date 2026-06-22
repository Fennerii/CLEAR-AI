# || Start of Imports ||
from fastapi import FastAPI, File, UploadFile
# Imports three things from FastAPI:
# FastAPI    -> the main application class, everything attaches to this
# File       -> tells FastAPI to expect a file in the incoming request
# UploadFile -> the type representing an uploaded file, gives access to its contents and metadata
# Docs: https://fastapi.tiangolo.com/tutorial/request-files/

from fastapi.middleware.cors import CORSMiddleware
# Imports CORS middleware. Browsers block requests between different ports by default
# (Vue on 5173, FastAPI on 8000). This middleware tells the browser those two are
# allowed to talk to each other.
# Docs: https://fastapi.tiangolo.com/tutorial/cors/

from detector import detect_image
# Imports the detect_image function from detector.py
# This is how main.py connects to the YOLO detection logic — without this import,
# main.py has no way to run object detection.

from disposer import get_disposal_instructions
# Imports the get_disposal_instructions function from disposer.py
# This connects main.py to the RAG / Ollama logic for generating disposal instructions.
# || End of Imports ||


# || Start of App Setup ||
app = FastAPI()
# Creates the FastAPI application instance.
# Every route, every middleware, everything attaches to this single app object.
# Docs: https://fastapi.tiangolo.com/tutorial/first-steps/

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
# Registers the CORS middleware on the app:
# allow_origins=["http://localhost:5173"] -> only requests from Vue's dev server are
#   allowed. More secure than ["*"] which would allow any website to call this API
# allow_methods=["*"]  -> allows all HTTP methods (GET, POST, PUT, DELETE)
# allow_headers=["*"]  -> allows any headers in the incoming request
# Docs: https://fastapi.tiangolo.com/tutorial/cors/
# || End of App Setup ||


# || Start of Routes ||
@app.get("/")
def root():
    return {"message": "CLEAR-AI API is running"}
# A decorator based route. @app.get("/") means this function runs whenever someone
# sends a GET request to the root URL (http://localhost:8000/).
# Simple health check — visiting that URL in a browser confirms the server is alive.
# Docs: https://fastapi.tiangolo.com/tutorial/first-steps/


@app.post("/detect")
# Registers a route that responds to POST requests at /detect.
# POST is used here (not GET) because Vue is sending data — an image file —
# not just requesting information.
# Docs: https://fastapi.tiangolo.com/tutorial/request-files/

async def detect(file: UploadFile = File(...)):
    # Defines the function that handles requests to /detect.
    # async      -> allows this function to handle multiple requests concurrently
    #               without blocking other requests while waiting for I/O operations
    # file: UploadFile -> tells FastAPI to expect a file upload, typed as UploadFile
    # = File(...)       -> the ... (Ellipsis) marks this parameter as required, not
    #                      optional. If Vue doesn't send a file, FastAPI automatically
    #                      returns an error
    # Docs: https://fastapi.tiangolo.com/tutorial/request-files/

    image_bytes = await file.read()
    # Reads the entire uploaded file into memory as raw bytes.
    # await is required because file.read() is an asynchronous operation — Python
    # waits for the file to fully load before moving to the next line, but doesn't
    # block other requests while waiting.
    # Docs: https://fastapi.tiangolo.com/tutorial/request-files/

    detections = detect_image(image_bytes)
    # Calls detect_image from detector.py, passing in the raw image bytes.
    # Returns a list of dictionaries, each containing a label, confidence score,
    # and bounding box coordinates for every object YOLO found.

    instructions = get_disposal_instructions(detections)
    # Calls get_disposal_instructions from disposer.py, passing in the detections list.
    # Internally this searches the knowledge base in ChromaDB for relevant disposal
    # rules, then sends that context plus the detected item labels to Ollama, which
    # returns disposal instructions as a string.

    return {
        "detections": detections,
        "instructions": instructions
    }
    # Returns a dictionary containing both pieces of information. FastAPI
    # automatically converts this Python dictionary into JSON before sending it
    # back to Vue. The response Vue receives looks like:
    # {
    #   "detections": [
    #     {"label": "plastic bottle", "confidence": 0.94, "box": [120, 45, 380, 290]}
    #   ],
    #   "instructions": "Place the plastic bottle in the recycling bin after..."
    # }
    # Docs: https://fastapi.tiangolo.com/tutorial/response-model/
# || End of Routes ||