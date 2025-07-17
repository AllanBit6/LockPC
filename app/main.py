from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True, # Allows cookies to be sent
    allow_methods=["*"],    # Allows all HTTP methods
    allow_headers=["*"],    # Allows all headers
)

connectedClients = {}

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    connectedClients[client_id] = websocket

    try:
        while True:
            data = await websocket.receive_text()
            print(f"[{client_id}] dice {data}")
    except WebSocketDisconnect:
        print(f"{client_id} desconectado")
        del connectedClients[client_id]

@app.post("/send/{client_id}")
async def send_command(client_id: str, command: str):
    if client_id in connectedClients:
        await connectedClients[client_id].send_text(command)
        return {"message": f"Comando '{command}' enviado a {client_id}"}
    else:
        return {"error": "Cliente no conectado"}
