import requests

class __SendMessageData:
    def __init__(self, to: str) -> None:
        self.to = to
    
    def text_message(self,text) -> dict:
        payload = {
            "messaging_product": "whatsapp",
            "to": str(self.to),
            "text": {
                "body": text
            }
        }

        return payload

class SendSessionMessages(__SendMessageData):
    def __init__(self,to) -> None:
        self.to = to
        
    def send_text_message(self,message:str) -> requests.Response:
        
        payload = self.text_message()
        response = self.send_message(payload)
        return response
