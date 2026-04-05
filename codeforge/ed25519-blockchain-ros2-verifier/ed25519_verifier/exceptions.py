class Ed25519VerificationError(Exception):
    """Exception raised when Ed25519 signature verification fails."""
    
    def __init__(self, message="Ed25519 signature verification failed"):
        self.message = message
        super().__init__(self.message)


class InvalidSignatureFormatError(Exception):
    """Exception raised when signature format is invalid."""
    
    def __init__(self, message="Invalid signature format provided"):
        self.message = message
        super().__init__(self.message)


class ROS2SignatureError(Exception):
    """Exception raised for errors in ROS2 signature handling."""
    
    def __init__(self, message="ROS2 signature handling error occurred"):
        self.message = message
        super().__init__(self.message)