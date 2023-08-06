import asyncio
import logging
from asyncio.locks import Event
from typing import List, Optional
from PIL.Image import Image
from VideoCapture import Device
from pyzbar.pyzbar import Decoded, decode

# from qgrabber.grabber import WxGrabber
# from qgrabber.pygrabber.dshow_graph import FilterGraph, FilterType
# from qgrabber.pygrabber.dshow_ids import MediaSubtypes, MediaTypes

_LOGGER = logging.getLogger(__name__)


class ScannerModel:
    """Scanner model managing the webcam.

    Use the start function to start scanning with callbacks carrying results.
    Use the async scan function to start scanning a wait for a scanned result.
    """

    def __init__(self):
        self._graph = None
        self._crop_x = None
        self._crop_y = None
        self._camera_callback = None
        self._evt = Event()
        self._camera = None

    async def scan(self, camera_callback, crop_x=None, crop_y=None) -> Optional[str]:
        self._camera_callback = camera_callback
        self._crop_x = crop_x
        self._crop_y = crop_y

        self._camera = Device(devnum=0, showVideoWindow=0)

        continue_scanning = True
        code = None
        while continue_scanning:
            buffer = self._camera.getImage()
            buffer = crop(buffer, self._crop_x, self._crop_y)
            self._camera_callback(buffer)
            code = decode(buffer)
            if code:

                break
            await asyncio.sleep(0.1)

        self.stop()
        return code

    def stop(self):
        """Stop the webcam."""
        if self._camera:
            del self._camera


def crop(data: Image, crop_x, crop_y):
    x, y = data.size
    return data.crop(
        ((x - crop_x) // 2, (y - crop_y) // 2, (x + crop_x) // 2, (y + crop_y) // 2)
    )
