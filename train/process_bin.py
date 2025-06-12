import PIL.Image
import numpy as np
import matplotlib.pyplot as plt
import struct
from struct import unpack
import PIL
from PIL import Image, ImageDraw
#=nb
path = 'C:\\Users\\pro\\Documents\\GitHub\\doodle\\train\\data\\full_binary_The Eiffel Tower.bin'

class addData:
    def unpack_drawing(self,file_handle):
        key_id, = unpack('Q', file_handle.read(8))
        country_code, = unpack('2s', file_handle.read(2))
        recognized, = unpack('b', file_handle.read(1))
        timestamp, = unpack('I', file_handle.read(4))
        n_strokes, = unpack('H', file_handle.read(2))
        image = []
        for i in range(n_strokes):
            n_points, = unpack('H', file_handle.read(2))
            fmt = str(n_points) + 'B'
            x = unpack(fmt, file_handle.read(n_points))
            y = unpack(fmt, file_handle.read(n_points))
            image.append((x, y))

        return {
            'image': image
        }
    def unpack_drawings(self,path):
        with open(path, 'rb') as f:
            while True:
                try:
                    yield self.unpack_drawing(f)
                except struct.error:
                    break
    def image(self, path):
        img = []
        for drawing in self.unpack_drawings(path): 
             img.append(drawing['image'])
        return img
    def loadData(self, path):
        imgs = self.image(path)
        large_size = 256
        img = Image.new("L", (large_size, large_size), color = 'white')
        draw = ImageDraw.Draw(img)
        img_arr = []
        for image in imgs:    
            for stroke in image:
                points = list(zip(stroke[0], stroke[1]))
                draw.line(points, fill=0, width=6)
            img = img.resize((28,28))            
            img_arr.append(img)
        img_arr = 255 - np.array(img_arr)
        return img_arr.reshape(img_arr.shape[0], 1, 28, 28)




d = addData()
images = d.loadData(path)
print(images.shape)