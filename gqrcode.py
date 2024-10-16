import qrcode
import qrcode.constants

def generate_qr(qrData):
    print("Process start....")
    qr=qrcode.QRCode(version=1,error_correction=qrcode.constants.ERROR_CORRECT_L,box_size=20,border=2)
    qr.add_data(qrData)
    qr.make(fit=True)
    img=qr.make_image(fill_color="black",back_color="white")
    imageQrPath="EasyOneQrCode"+".png"
    img.save(imageQrPath)
    print("Process done!")
    return f'{imageQrPath}'


# print(generate_qr(qrData,"aa"))