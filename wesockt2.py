import asyncio
import websockets
import json

# Dicionário para armazenar as conexões de clientes associadas aos IDs de usuário
clientes_por_id = {}

async def chat(websocket, path):
    # Espera receber uma mensagem inicial contendo o ID do usuário
    id_usuario = await websocket.recv()
    
    # Associa a conexão do cliente ao ID do usuário
    clientes_por_id[id_usuario] = websocket
    
    try:
        # Loop para receber e transmitir mensagens
        async for message in websocket:
            # Envia a mensagem recebida para o cliente destinatário (se existir)
            data = json.loads(message)
            destinatario = data.get('destinatario')
            if destinatario in clientes_por_id:
                await clientes_por_id[destinatario].send(json.dumps({'remetente': id_usuario, 'mensagem': data['mensagem']}))
    finally:
        # Remove a conexão do cliente ao desconectar
        if id_usuario in clientes_por_id:
            del clientes_por_id[id_usuario]

# Inicia o servidor na porta 8765
start_server = websockets.serve(chat, "localhost", 8765)

# Inicia o loop de evento para esperar por conexões
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()