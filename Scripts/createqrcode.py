from PIL import Image
from subprocess import check_output
import qrcode
import os

'''
This script generates a QR code based on the 
Raspberry Pi's ip address, and overlays it
onto the decorative background
'''

def make():
    ip_address = check_output(['hostname', '-I'])[:-2].decode()
    full_ip_address = 'http:/' + ip_address + ':5000/'

    qrbase = Image.open(os.path.abspath('../Assets/Misc/QR_BASE.png'))

    qr = qrcode.QRCode(
        version = 2,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=1,
        border=1
    )
    qr.add_data(full_ip_address)
    qr.make(fit=True)
    img = qr.make_image(fill_color = "black", back_color="white")

    qrbase.paste(img, (18, 2), img)

    return qrbase