import cv2
import av
from pyzbar.pyzbar import decode
from streamlit_webrtc import VideoProcessorBase
from database import add_scan


class QRScanner(VideoProcessorBase):
    """
    Video processor for detecting QR codes and barcodes
    from the browser webcam.
    """

    def __init__(self):
        self.last_scan = ""
        self.last_type = ""

    def recv(self, frame):

        image = frame.to_ndarray(format="bgr24")

        detected_codes = decode(image)

        for code in detected_codes:

            x, y, w, h = code.rect

            barcode_value = code.data.decode("utf-8")
            barcode_type = code.type

            cv2.rectangle(
                image,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

            cv2.putText(
                image,
                barcode_type,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

            if barcode_value != self.last_scan:
                self.last_scan = barcode_value
                self.last_type = barcode_type

                # Save to SQLite
                add_scan(barcode_type, barcode_value)

        return av.VideoFrame.from_ndarray(
            image,
            format="bgr24"
        )
