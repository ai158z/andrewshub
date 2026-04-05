import json
from ed25519_verifier.ros2_integration import TestROS2Integration
from ed25519_verifier.core import Ed25519Verifier
from ed25519_exception import InvalidSignatureFormatError
import base64
import pytest
from unittest.mock import patch, MagicMock

# Test data for signing
test_private_key = base64.b64decode(b'jg4DdWN25V2VLk1rWQ==')
test_public_key = base64.b6