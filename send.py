import requests

# URL del server Flask
server_url = "http://192.168.150.17:5000/"  # Indirizzo IP del server Flask

# Messaggio da inviare
payload = {"name": "Alice", "message": "Ciao, come va?"}

# Funzione per inviare messaggio
def invia_messaggio(server_url, payload):
    try:
        response = requests.post(server_url, json=payload)
        print("Status Code:", response.status_code)
        print("Risposta del server:", response.json())
    except requests.exceptions.RequestException as e:
        print("Errore durante la connessione al server:", e)

# Invio messaggio
invia_messaggio(server_url, payload)
