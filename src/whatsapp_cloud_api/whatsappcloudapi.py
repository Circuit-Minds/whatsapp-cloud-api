import requests , uuid, json
from typing import Union

class WhatsApp:
    def __init__(self,phone_number_id,bearer_token,version="v15.0"):
        self.PHONE_NUMBER_ID = phone_number_id
        self.BEARER_TOKEN = bearer_token
        self.VERSION = version

    def upload_media(self,file_name:str,file_binary:bytes,mime_type:str,return_request:bool=False) -> Union[str, requests.Response]:
        media_id = None
        url = f"https://graph.facebook.com/{self.VERSION}/{self.PHONE_NUMBER_ID}/media"
        
        files = [
            ("file",(file_name,file_binary,mime_type))
        ]
        payload={"messaging_product":"whatsapp"}
        headers = {
        'Authorization': 'Bearer '+ self.BEARER_TOKEN
        }

        response = requests.request("POST",url=url,headers=headers,data=payload,files=files)
        if return_request:
            return response
        else:
            response = response.json()
            if "id" in response:
                media_id = response["id"]
            return media_id

    def get_media_url(self,media_id:str,get_all_media_details:bool=False) -> str:

        url = f"https://graph.facebook.com/{self.VERSION}/" + media_id

        payload={}
        headers = {
        'Authorization': 'Bearer '+ self.BEARER_TOKEN
        }

        response       = requests.request("GET", url, headers=headers, data=payload)
        media_details  = response.json()
        if get_all_media_details:
            return media_details
        else:
            media_url      = self.__get_media_file(self.BEARER_TOKEN,media_details)
            return media_url

    def __get_media_file(self,bearer_token,media_details):

        url = media_details["url"]

        payload={}
        headers = {
        'Authorization': 'Bearer '+ bearer_token
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        media_content = response.content
        media_url = self.__get_url_from_binary(media_content,media_details)

        return media_url

    def __get_url_from_binary(self,file_as_binary,media_details,output_path:str='') -> str:
        # ts              = int(time.time())
        mime_type       = media_details["mime_type"]        #Ex : image/jpeg
        media_type      = mime_type.split("/")[0]           #Ex : image/jpeg -> image
        extension       = mime_type.split("/")[1]           #Ex : image/jpeg -> jpeg
        gen_uuid        = str(uuid.uuid4())
        # file_as_binary = io.BytesIO(file_as_binary)
        key = "media/"+media_type+"/"+"whatsapp_"+media_type+"_"+gen_uuid+"."+extension
        with open(key,'wb') as file:
            file.write(file_as_binary)
        return key

    def __get_upload_session(self):


        URL = f"https://graph.facebook.com/{self.VERSION}/app/uploads/"

        HEADERS = {
            "Authorization" : "OAuth "+self.BEARER_TOKEN
        }

        response = requests.request('POST',url=URL,headers=HEADERS)
        session_id  = response.json()["id"]

        return session_id

    def _get_header_handle(self,mime_type:str,binary_data:bytes) -> str:

        session_id = self.__get_upload_session()
        URL = f"https://graph.facebook.com/{self.VERSION}/{session_id}"
        HEADERS = {
            'Content-Type': mime_type,
            'file_offset': '0',
            'Authorization': 'OAuth '+self.BEARER_TOKEN
            }
        DATA = binary_data

        response = requests.request("POST",url=URL,headers=HEADERS,data=DATA)
        header_handle = response.json()["h"]
        return header_handle

    
    def _send_message(self,payload:dict) -> requests.Response:
        url = f'https://graph.facebook.com/{self.VERSION}/{self.PHONE_NUMBER_ID}/messages'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+ self.BEARER_TOKEN
        }

        data = payload
        if isinstance(payload, dict):
            data = json.dumps(payload)
        resp = requests.post(url=url,headers=headers,data=data)
        return resp

    
    
    def send_text_message(self,to:str,message:str,preview_url:bool = False,reply_to_message_id:str=None) -> requests.Response:
        
        payload = _MessageData(to).text_message(message,preview_url,reply_to_message_id)
        response = self._send_message(payload)
        return response
    
    def send_react_to_message(self,to:str,reply_to_message_id:str,emoji:str) -> requests.Response:
        
        payload = _MessageData(to).react_to_message(reply_to_message_id,emoji)
        response = self._send_message(payload)
        return response
    
    def send_image_message(self,to:str,image_id_or_url:str,caption:str=None,reply_to_message_id:str=None) -> requests.Response:
        
        payload = _MessageData(to).image_message(image_id_or_url,caption,reply_to_message_id)
        response = self._send_message(payload)
        return response
    
    def send_audio_message(self,to:str,aduio_id_or_url:str,reply_to_message_id:str=None) -> requests.Response:
        
        payload = _MessageData(to).audio_message(aduio_id_or_url,reply_to_message_id)
        response = self._send_message(payload)
        return response

    def send_video_message(self,to:str,video_id_or_url:str,caption:str=None,reply_to_message_id:str=None) -> requests.Response:
        
        payload = _MessageData(to).video_message(video_id_or_url,caption,reply_to_message_id)
        response = self._send_message(payload)
        return response
    
    def send_document_message(self,to:str,document_id_or_url:str,filename:str='Document',caption:str=None,reply_to_message_id:str=None) -> requests.Response:
        
        payload = _MessageData(to).document_message(document_id_or_url,caption,reply_to_message_id)
        response = self._send_message(payload)
        return response
    
    def send_media_message(self,to:str,media_type:str,media_id_or_url,caption:str=None,file_name="Document",reply_to_message_id:str=None) -> requests.Response:
        
        payload = _MessageData(to).media_message(media_type,media_id_or_url,caption,file_name,reply_to_message_id)
        response = self._send_message(payload)
        return response

class _MessageData:
    def __init__(self, to: str):
        self.to = to
    
    def text_message(self,text:str,preview_url:bool = False,reply_to_message_id:str=None) -> dict:
        payload = {
            "messaging_product": "whatsapp",
            "to": str(self.to),
            "text": {
                "preview_url": preview_url,
                "body": text
            }
        }
        
        if reply_to_message_id:
            payload['context'] = {
                "message_id": reply_to_message_id
            }

        return payload
    
    def react_to_message(self,reply_to_message_id:str,emoji:str) -> dict:
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": self.to,
            "type": "reaction",
            "reaction": {
                "message_id": reply_to_message_id,
                "emoji": emoji
            }
        }
        
        return payload
    
    def image_message(self,image_id_or_url:str,caption:str=None,reply_to_message_id:str=None) -> dict:
        handle_type = 'id'
        if 'https' in image_id_or_url:
            handle_type = 'link'
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": self.to,
            "type": "image",
            "image": {
                handle_type : image_id_or_url
            }
        }
        
        if caption:
            payload['image']['caption'] = caption
        if reply_to_message_id:
            payload['context'] = {
                "message_id": reply_to_message_id
            }
        
        return payload
    
    def audio_message(self,audio_id_or_url:str,reply_to_message_id:str=None) -> dict:
        handle_type = 'id'
        if 'https' in audio_id_or_url:
            handle_type = 'link'
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": self.to,
            "type": "audio",
            "audio": {
                handle_type : audio_id_or_url
            }
        }
        
        if reply_to_message_id:
            payload['context'] = {
                "message_id": reply_to_message_id
            }
        
        return payload
    
    def video_message(self,video_id_or_url:str,caption:str=None,reply_to_message_id:str=None) -> dict:
        handle_type = 'id'
        if 'https' in video_id_or_url:
            handle_type = 'link'
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": self.to,
            "type": "video",
            "video": {
                handle_type : video_id_or_url
            }
        }
        if caption:
            payload['video']['caption'] = caption
        if reply_to_message_id:
            payload['context'] = {
                "message_id": reply_to_message_id
            }
        
        return payload
    
    def document_message(self,document_id_or_url,filename:str='Document',caption:str=None,reply_to_message_id:str=None) -> dict:
        handle_type = 'id'
        if 'https' in document_id_or_url:
            handle_type = 'link'
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": self.to,
            "type": "document",
            "document": {
                handle_type : document_id_or_url,
                "filename": filename
            }
        }
        if caption:
            payload['document']['caption'] = caption
        if reply_to_message_id:
            payload['context'] = {
                "message_id": reply_to_message_id
            }
        
        return payload
    
    
    def media_message(self,media_type:str,media_id_or_url,caption:str=None,file_name="Document",reply_to_message_id:str=None) -> dict:
        handle_type = 'id'
        if 'https' in media_id_or_url:
            handle_type = 'link'
        media_type = media_type.lower()

        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": self.to,
            "type": media_type,
            media_type: {
                handle_type: media_id_or_url,

            }
        }
        if caption:
            payload['document']['caption'] = caption
        if reply_to_message_id:
            payload['context'] = {
                "message_id": reply_to_message_id
            }
            
        return payload
