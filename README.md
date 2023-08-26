# whatsapp-cloud-api
# WhatsApp Cloud API Python Module

The **whatsapp-cloud-api** Python module provides a simple and convenient way to interact with WhatsApp Cloud API. This module allows you to send various types of messages, including text messages, images, audio, videos, documents, and media messages. It abstracts away the complexity of the API calls and provides easy-to-use methods for sending different types of messages to WhatsApp users.

## Installation

You can install the **whatsapp-cloud-api** module using pip:

```bash
pip install whatsapp-cloud-api
```

## Usage

To use the **whatsapp-cloud-api** module, you need to import it into your Python script and create an instance of the `WhatsApp` class by providing the required parameters: `phone_number_id` and `bearer_token`.

```python
from whatsapp_cloud_api import WhatsApp

phone_number_id = "your_phone_number_id"
bearer_token = "your_bearer_token"

whatsapp = WhatsApp(phone_number_id, bearer_token)
```

### Sending Text Messages

You can send text messages to WhatsApp users using the `send_text_message` method.

```python
to = "recipient_phone_number"
message = "Hello, this is a text message."

response = whatsapp.send_text_message(to, message)
print(response.json())
```

### Sending Images

You can send images to WhatsApp users using the `send_image_message` method.

```python
to = "recipient_phone_number"
image_id_or_url = "image_id_or_url"

response = whatsapp.send_image_message(to, image_id_or_url)
print(response.json())
```

### Sending Audio

You can send audio messages to WhatsApp users using the `send_audio_message` method.

```python
to = "recipient_phone_number"
audio_id_or_url = "audio_id_or_url"

response = whatsapp.send_audio_message(to, audio_id_or_url)
print(response.json())
```

### Sending Videos

You can send videos to WhatsApp users using the `send_video_message` method.

```python
to = "recipient_phone_number"
video_id_or_url = "video_id_or_url"

response = whatsapp.send_video_message(to, video_id_or_url)
print(response.json())
```

### Sending Documents

You can send documents to WhatsApp users using the `send_document_message` method.

```python
to = "recipient_phone_number"
document_id_or_url = "document_id_or_url"

response = whatsapp.send_document_message(to, document_id_or_url)
print(response.json())
```

### Sending Media Messages

You can send media messages (such as images, audio, videos, and documents) to WhatsApp users using the `send_media_message` method.

```python
to = "recipient_phone_number"
media_type = "image"  # Replace with the desired media type
media_id_or_url = "media_id_or_url"

response = whatsapp.send_media_message(to, media_type, media_id_or_url)
print(response.json())
```

### Sending Reactions

You can send reactions to specific messages using the `send_react_to_message` method.

```python
to = "recipient_phone_number"
reply_to_message_id = "message_id"
emoji = "👍"  # Replace with the desired emoji

response = whatsapp.send_react_to_message(to, reply_to_message_id, emoji)
print(response.json())
```

## Contributing

If you'd like to contribute to the development of this module or report issues, please feel free to submit a pull request or create an issue on the [GitHub repository](https://github.com/your/repository).

## License

This module is released under the [MIT License](LICENSE).

## Disclaimer

This module is not officially affiliated with WhatsApp or Facebook. It's an independent project developed by the community.

**Note:** Make sure to replace placeholders (`your_phone_number_id`, `your_bearer_token`, etc.) with actual values when using the module.

For more detailed information about the methods and classes provided by the **whatsapp-cloud-api** module, refer to the module's source code or docstrings.