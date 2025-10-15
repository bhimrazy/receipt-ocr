import base64
import io

import pytest
from PIL import Image

from receipt_ocr.utils import encode_image_to_base64


def test_encode_image_from_path(tmp_path):
    # Create a dummy image file
    dummy_image = Image.new("RGB", (100, 100), color="red")
    image_path = tmp_path / "test_image.png"
    dummy_image.save(image_path)

    result = encode_image_to_base64(str(image_path))

    # Verify it's a valid base64 string
    assert isinstance(result, str)
    # Decode to verify it's valid base64
    decoded = base64.b64decode(result)
    assert len(decoded) > 0


def test_encode_image_from_bytes():
    # Create image bytes
    dummy_image = Image.new("RGB", (50, 50), color="blue")
    buffered = io.BytesIO()
    dummy_image.save(buffered, format="PNG")
    image_bytes = buffered.getvalue()

    result = encode_image_to_base64(image_bytes)

    assert isinstance(result, str)
    decoded = base64.b64decode(result)
    assert len(decoded) > 0


def test_encode_image_from_pil():
    dummy_image = Image.new("RGB", (30, 30), color="green")

    result = encode_image_to_base64(dummy_image)

    assert isinstance(result, str)
    decoded = base64.b64decode(result)
    assert len(decoded) > 0


def test_encode_image_resizing():
    # Create a large image
    large_image = Image.new("RGB", (2000, 1500), color="yellow")

    result = encode_image_to_base64(large_image, max_size=1000)

    assert isinstance(result, str)
    decoded = base64.b64decode(result)
    # Reconstruct image to check size
    reconstructed = Image.open(io.BytesIO(decoded))
    assert max(reconstructed.size) <= 1000


def test_encode_image_unsupported_type():
    with pytest.raises(ValueError, match="Unsupported image type"):
        encode_image_to_base64(123)


def test_encode_image_mode_conversion():
    # Create image with different mode
    rgba_image = Image.new("RGBA", (50, 50), color=(255, 0, 0, 128))

    result = encode_image_to_base64(rgba_image)

    assert isinstance(result, str)
    decoded = base64.b64decode(result)
    reconstructed = Image.open(io.BytesIO(decoded))
    # Should be converted to RGB
    assert reconstructed.mode == "RGB"
