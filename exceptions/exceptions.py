class APIServiceError(Exception):
    """Base class for other exceptions in this module."""
    def __init__(self, message=None):
        self.message = message or "API service error"
        super().__init__(self.message)


class OpenAIError(APIServiceError):
    """Raised when OpenAI service failed."""
    def __init__(self, message="OpenAI service error"):
        super().__init__(message)


class MarvinError(APIServiceError):
    """Raised when Marvin generating caption service failed."""
    def __init__(self, message="Marvin service error"):
        super().__init__(message)


class AWSError(APIServiceError):
    """Raised when AWS uploading image service failed."""
    def __init__(self, message="AWS service error"):
        super().__init__(message)
