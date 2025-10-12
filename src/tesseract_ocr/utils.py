import cv2
import imutils
import numpy as np
import pytesseract
from imutils.perspective import four_point_transform


def _evaluate_contour_candidate(contour, image_shape):
    """Evaluate a contour candidate for receipt detection based on multiple
    criteria.

    Args:
        contour: The contour to evaluate
        image_shape: Shape of the original image (height, width)

    Returns:
        dict: Dictionary with evaluation scores
    """
    # Calculate basic properties
    area = cv2.contourArea(contour)
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.02 * peri, True)

    # Must have 4 points after approximation
    if len(approx) != 4:
        return None

    # Get bounding rectangle
    x, y, w, h = cv2.boundingRect(approx)

    # Calculate aspect ratio (receipts are typically taller than wide)
    aspect_ratio = h / w if w > 0 else 0

    # Calculate solidity (ratio of contour area to bounding box area)
    solidity = area / (w * h) if w * h > 0 else 0

    # Calculate position score (prefer contours closer to center)
    image_center_x = image_shape[1] / 2
    image_center_y = image_shape[0] / 2
    contour_center_x = x + w / 2
    contour_center_y = y + h / 2

    distance_from_center = np.sqrt(
        (contour_center_x - image_center_x) ** 2
        + (contour_center_y - image_center_y) ** 2
    )
    max_distance = np.sqrt(image_center_x**2 + image_center_y**2)
    position_score = 1 - (distance_from_center / max_distance)

    # Size score (prefer contours that are reasonably large but not too dominant)
    image_area = image_shape[0] * image_shape[1]
    size_ratio = area / image_area
    size_score = 1 - abs(size_ratio - 0.3)  # Optimal around 30% of image area

    # Aspect ratio score (receipts are typically 1.5-4 times taller than wide)
    if 1.5 <= aspect_ratio <= 4.0:
        aspect_score = 1.0
    elif 1.2 <= aspect_ratio <= 5.0:
        aspect_score = 0.8
    else:
        aspect_score = 0.3

    # Solidity score (prefer well-filled rectangles)
    solidity_score = min(solidity * 2, 1.0)  # Scale up solidity, cap at 1.0

    # Combined score
    total_score = (
        position_score * 0.2
        + size_score * 0.3
        + aspect_score * 0.3
        + solidity_score * 0.2
    )

    return {
        "contour": approx,
        "score": total_score,
        "area": area,
        "aspect_ratio": aspect_ratio,
        "solidity": solidity,
        "bounding_rect": (x, y, w, h),
    }


def perform_ocr(img: np.ndarray):
    img_orig = cv2.imdecode(img, cv2.IMREAD_COLOR)

    receipt = process_receipt_image(img_orig)

    # apply OCR to the receipt image by assuming column data, ensuring
    # the text is *concatenated across the row* (additionally, for your
    # own images you may need to apply additional processing to cleanup
    # the image, including resizing, thresholding, etc.)
    options = "--psm 6"
    text = pytesseract.image_to_string(
        cv2.cvtColor(receipt, cv2.COLOR_BGR2RGB), config=options
    )
    return text


def process_receipt_image(img_orig):
    """Process the receipt image to extract the receipt area using robust
    methods.

    Args:
        img_orig: Original image as numpy array

    Returns:
        receipt: Warped receipt image
    """
    # Detect and correct orientation before processing
    img_orig = _detect_and_correct_orientation(img_orig)

    image = img_orig.copy()
    image = imutils.resize(image, width=500)
    ratio = img_orig.shape[1] / float(image.shape[1])

    # convert the image to grayscale, blur it slightly, and then apply
    # edge detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(
        gray,
        (
            5,
            5,
        ),
        0,
    )
    edged = cv2.Canny(blurred, 75, 200)

    # find contours in the edge map and sort them by size in descending
    # order
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[
        :10
    ]  # Consider top 10 contours

    # Evaluate contour candidates
    candidates = []
    for c in cnts:
        candidate = _evaluate_contour_candidate(c, image.shape)
        if candidate is not None:
            candidates.append(candidate)

    # Select the best candidate
    if not candidates:
        raise Exception(
            (
                "Could not find suitable receipt outline. "
                "Try debugging your edge detection and contour steps."
            )
        )

    # Sort by score and select the best
    candidates.sort(key=lambda x: x["score"], reverse=True)
    best_candidate = candidates[0]

    receiptCnt = best_candidate["contour"]

    # apply a four-point perspective transform to the *original* image to
    # obtain a top-down bird's-eye view of the receipt
    points = receiptCnt.reshape(4, 2) * ratio
    # To make the transformation robust to small edge imperfections,
    # use the bounding box corners instead of the exact contour points
    x, y, w, h = cv2.boundingRect(points.astype(np.int32))
    warped_points = np.array(
        [[x, y], [x + w, y], [x + w, y + h], [x, y + h]], dtype=np.float32
    )
    receipt = _robust_perspective_transform(img_orig, warped_points)

    return receipt


def _robust_perspective_transform(image, src_points, dst_points=None):
    """Apply robust perspective transformation using RANSAC.

    Args:
        image: Input image
        src_points: Source points (4 points)
        dst_points: Destination points (4 points), if None, will be calculated to maintain aspect ratio

    Returns:
        Warped image
    """
    if dst_points is None:
        # Calculate destination points to maintain aspect ratio
        src_rect = cv2.boundingRect(src_points.astype(np.int32))
        x, y, w, h = src_rect

        # Calculate aspect ratio from source bounding box
        aspect_ratio = h / w

        # Create destination rectangle with same aspect ratio
        # Make it large enough to contain the entire warped image
        max_dim = max(w, h)
        dst_w = max_dim
        dst_h = int(max_dim * aspect_ratio)

        dst_points = np.array(
            [[0, 0], [dst_w - 1, 0], [dst_w - 1, dst_h - 1], [0, dst_h - 1]],
            dtype=np.float32,
        )

    # Find homography using RANSAC
    H, mask = cv2.findHomography(src_points, dst_points, cv2.RANSAC, 5.0)

    if H is None:
        # Fallback to original method if RANSAC fails
        return four_point_transform(image, src_points)

    # Apply perspective transformation
    warped = cv2.warpPerspective(
        image, H, (int(dst_points[1][0] + 1), int(dst_points[2][1] + 1))
    )

    return warped


def _detect_and_correct_orientation(image):
    """Detect image orientation and rotate if necessary.

    Args:
        image: Input image

    Returns:
        Corrected image
    """
    try:
        # Get orientation data
        osd = pytesseract.image_to_osd(image)

        # Extract rotation angle
        rotation = 0
        for line in osd.split("\n"):
            if "Rotate:" in line:
                rotation = int(line.split(":")[1].strip())
                break

        # Rotate image if needed
        if rotation != 0:
            (h, w) = image.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, rotation, 1.0)
            rotated = cv2.warpAffine(image, M, (w, h))
            return rotated

    except Exception:
        # If orientation detection fails, return original image
        pass

    return image
