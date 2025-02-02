import base64


def encrypt(text: str) -> str:
	return base64.b64encode(text.encode('utf-8')).decode('utf-8')
