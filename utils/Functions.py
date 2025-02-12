import base64


def encrypt(text: str) -> str:
	return base64.b64encode(text.encode()).decode()
