import base64
import io
from typing import Union
from PIL import Image


def encode_image_to_base64(
    image: Union[str, bytes, Image.Image], max_size: int = 1080
) -> str:
    """Encode an image to base64 string.

    Args:
        image: Image source (file path, bytes, or PIL Image)
        max_size: Maximum dimension for resizing (maintains aspect ratio)

    Returns:
        Base64 encoded string of the image
    """
    # Handle different image input types
    if isinstance(image, str):
        # File path
        pil_image = Image.open(image)
    elif isinstance(image, bytes):
        # Image bytes
        pil_image = Image.open(io.BytesIO(image))
    elif isinstance(image, Image.Image):
        # PIL Image object
        pil_image = image
    else:
        raise ValueError(f"Unsupported image type: {type(image)}")

    # Convert to RGB if necessary
    if pil_image.mode not in ("RGB", "L"):
        pil_image = pil_image.convert("RGB")

    # Resize if too large (maintain aspect ratio)
    if max(pil_image.size) > max_size:
        w, h = pil_image.size
        if w > h:
            new_w = max_size
            new_h = int(h * max_size / w)
        else:
            new_h = max_size
            new_w = int(w * max_size / h)
        pil_image = pil_image.resize((new_w, new_h), Image.Resampling.LANCZOS)

    # Convert to PNG and encode
    buffered = io.BytesIO()
    pil_image.save(buffered, format="PNG")
    img_bytes = buffered.getvalue()

    return base64.b64encode(img_bytes).decode("utf-8")
