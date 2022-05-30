# By Bartłomiej Wujec

from PIL import Image
import hashlib

input_image = Image.open("plain.bmp")

image_data = input_image.tobytes()
width, height = input_image.size

new_data = []
keys = []
block = 8

for x in range(block):
    key = hashlib.sha1(str(x ** 15 + x).encode("UTF-8")).digest()
    keys.append(key)

for x in range(width):
    for y in range(height):
        index = x * height + y
        old_value = image_data[index]
        new_value = old_value ^ keys[x % block][y % block]
        new_data.append(new_value)

fill = [i for n in range(3) for i in new_data]
output_ecb = Image.new("RGB", (width, height))
output_ecb.frombytes(bytes(fill))
output_ecb.save("ecb_crypto.bmp")

new_key = 274991 % 256
new_data = [image_data[0] ^ new_key]
for x in range(width * height):
    new_data.append(new_data[x - 1] ^ image_data[x] ^ keys[x % 64 // 8][x % 8])

fill = [i for n in range(3) for i in new_data]

output_cbc = Image.new("RGB", (width, height))
output_cbc.frombytes(bytes(fill))
output_cbc.save("cbc_crypto.bmp")
