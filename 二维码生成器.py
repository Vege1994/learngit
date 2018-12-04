import qrcode

qr = qrcode.QRCode(version = 2,error_correction = qrcode.constants.ERROR_CORRECT_L,box_size=10,border=10)
qr.add_data('https://dcyzmap.dcyz.com/monthmenu.html')
qr.make(fit=True)
img = qr.make_image()
img.save(r'E:\CWZ\都城快餐.png')