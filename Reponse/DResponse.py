class DResponse:

    def __init__(self, content, content_type: str = "text/html", status_code: int = 200):
        self.content_type = content_type
        self.content = content
        self.status_code = status_code

    def __repr__(self):
        return f"ResponseModel(content_type='{self.content_type}', status_code={self.status_code})"

    def __str__(self):
        return f"Status: {self.status_code} | Type: {self.content_type}"