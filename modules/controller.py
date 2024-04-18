class procesamiento_eventos:
    def __init__(self):
        pass

    def procesar_evento_github(self, data):
        print("Procesando evento de GitHub...")
        # Supongamos que queremos registrar el tipo de evento y quién lo envió
        event_type = data.get('action', 'No action specified')
        user = data.get('sender', {}).get('login', 'Unknown user')
        print(f"Evento de GitHub de tipo '{event_type}' enviado por {user}")
        # Añade aquí más lógica de procesamiento según sea necesario
        return "Evento de GitHub procesado"
    
    def procesar_evento_gitlab(self, data):
        print("Procesando evento de GitLab...")
        event_type = data.get('object_kind', 'No object kind specified')
        user = data.get('user', {}).get('name', 'Unknown user')
        print(f"Evento de GitLab de tipo '{event_type}' enviado por {user}")
        # Añade aquí más lógica de procesamiento según sea necesario
        return "Evento de GitLab procesado"

    def procesar_evento_azure(self, data):
        print("Procesando evento de Azure DevOps...")
        event_type = data.get('eventType', 'No eventType specified')
        resource = data.get('resource', {}).get('commits', [])
        print(f"Evento de Azure DevOps de tipo '{event_type}' con {len(resource)} commits")
        # Añade aquí más lógica de procesamiento según sea necesario
        return "Evento de Azure DevOps procesado"