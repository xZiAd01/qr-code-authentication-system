# Import required libraries
import cv2
from pdf2image import convert_from_path
import numpy as np
import os

class QRCodeReader:
    """
    QRCodeReader class
    - Reads & decodes QR codes from image or PDF.
    - Uses OpenCV for detection & decoding.
    - Supports fallback strategies if detection fails initially.
    """

    def __init__(self):
        # Initialize OpenCV QR code detector
        self.detector = cv2.QRCodeDetector()

    def smart_decode(self, file_path, return_image=False):
        """
        Detects file type (image or PDF) and decodes QR code accordingly.
        
        Args:
            file_path (str): Path to the file to process.
            return_image (bool): If True, returns cropped QR code region as well.

        Returns:
            str or tuple: Decoded QR code string (or None), optionally with image.
        """
        # Determine the file extension
        ext = os.path.splitext(file_path)[1].lower()

        if ext == '.pdf':
            # Handle PDF: convert all pages to images and try decoding each
            pil_pages = convert_from_path(file_path)
            for pil_page in pil_pages:
                img = self._pil_to_cv2(pil_page)
                result = self._decode_image(img, return_image)
                if (return_image and result[0]) or (not return_image and result):
                    # Return as soon as a QR is detected
                    return result
            # If no QR found in any page
            return (None, None) if return_image else None

        else:
            # Assume it's an image file
            img = cv2.imread(file_path)
            result = self._decode_image(img, return_image)
            return result

    def _decode_image(self, img, return_image):
        """
        Tries to decode QR code from the given image using different strategies.
        If initial detection fails, applies adaptive techniques to improve chances.
        
        Args:
            img (np.ndarray): Image array.
            return_image (bool): Whether to return cropped QR region.

        Returns:
            str or tuple: Decoded data (and optionally image) or None.
        """
        # Try decoding as-is
        data, points, _ = self.detector.detectAndDecode(img)

        if data:
            if return_image:
                cropped = self._extract_qr_region(img, points)
                return data, cropped
            return data

        # If failed: try grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        data, points, _ = self.detector.detectAndDecode(gray)
        if data:
            if return_image:
                cropped = self._extract_qr_region(img, points)
                return data, cropped
            return data

        # If still failed: try with thresholding
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        data, points, _ = self.detector.detectAndDecode(thresh)
        if data:
            if return_image:
                cropped = self._extract_qr_region(img, points)
                return data, cropped
            return data

        # No QR found
        return (None, None) if return_image else None

    def _pil_to_cv2(self, pil_image):
        """
        Converts a PIL Image to an OpenCV-compatible numpy array (BGR).

        Args:
            pil_image (PIL.Image): Image from PDF page.

        Returns:
            np.ndarray: OpenCV image.
        """
        return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    def _extract_qr_region(self, img, points):
        """
        Crops the region containing the QR code from the image.

        Args:
            img (np.ndarray): Original image.
            points (np.ndarray): Corner points of QR code.

        Returns:
            np.ndarray: Cropped QR code image.
        """
        if points is None:
            return None

        # Convert points to int and find bounding box
        points = points[0].astype(int)
        x_min = max(min(points[:, 0]), 0)
        y_min = max(min(points[:, 1]), 0)
        x_max = min(max(points[:, 0]), img.shape[1])
        y_max = min(max(points[:, 1]), img.shape[0])

        cropped = img[y_min:y_max, x_min:x_max]
        return cropped
