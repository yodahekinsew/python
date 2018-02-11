#!/usr/bin/env python3

import sys
import math
import base64
import tkinter

from io import BytesIO
from PIL import Image as PILImage
from PIL import ImageFilter

## NO ADDITIONAL IMPORTS ALLOWED!

class Image:
    def __init__(self, width, height, pixels):
        self.width = width
        self.height = height
        self.pixels = pixels
    
    def get_pixel(self, x, y):
        #x and y are both integers
        #Function indexes self.pixels using x and y in order to get a pixel value
        if x < 0:
            x = 0
        elif x > self.width - 1:
            x = self.width - 1
        if y < 0:
            y = 0
        elif y > self.height - 1:
            y = self.height -1
        return self.pixels[x+(self.width)*y]
        
    def set_pixel(self, x, y, color):
        #x and y are both integers
        #color is an integer assigned to a pixel value (between 0 and 255)
        #Function is used to place pixel value in Image
        self.pixels[x + self.width*(y)] = color
      
    def edges(self):
        #function takes in no arguments besides the picture itself
        #function returns an image that shows all the edges in original image
        result = Image.new(self.width, self.height)
        kernel_x = [-1, 0, 1, -2, 0, 2, -1, 0, 1]
        kernel_y = [-1, -2, -1, 0, 0, 0, 1, 2, 1]
        for y in range(result.height):
            for x in range(result.width):
                color_x = 0
                color_y = 0
                kernel_index = 0
                for j in range(-1,2): 
                    for i in range(-1,2):
                        color_x += (self.get_pixel(x+i,y+j)*kernel_x[kernel_index])
                        color_y += (self.get_pixel(x+i,y+j)*kernel_y[kernel_index])
                        kernel_index += 1
                new_color = int(round(((((color_x)**2)+(((color_y)**2)))**.5)))
                if new_color > 255:
                    new_color = 255
                if new_color < 0:
                    new_color = 0
                result.set_pixel(x,y,new_color)
        return result

    def rescale(self, numdeletions):
        result = Image.new(self.width - numdeletions, self.height)
        print(self.width,'width')
        print(self.height, 'height')
        numpixels = 0
        pixels = self.pixels
        energy_map = self.edges(numpixels)
        energy_pixels = energy_map.pixels
        total = 0
        values = {}
        for x in range(result.width):
            total = 0
            for y in range(result.height):
                total += energy_pixels[x+(self.width)*y]
            values[x] = total
        while numpixels < numdeletions:
            min_x = min(values, key = values.get)
            for y in range(result.height):
                pixels[min_x+self.width*y] = -1
            values = {key:value for key,value in values.items() if key is not min_x}
            numpixels += 1
        while -1 in pixels:
            pixels.remove(-1)
        index = 0
        while index < len(pixels):
            color = pixels[index]
            result.pixels[index] = color
            index += 1
        return result
    # Below this point are utilities for loading, saving, and displaying
    # images, as well as for testing.

    def __eq__(self, other):
        return all(getattr(self, i) == getattr(other, i)
                   for i in ('height', 'width', 'pixels'))

    @classmethod
    def load(cls, fname):
        """
        Loads an image from the given file and returns an instance of this
        class representing that image.  This also performs conversion to
        grayscale.

        Invoked as, for example:
           i = Image.load('test_images/cat.png')
        """
        with open(fname, 'rb') as img_handle:
            img = PILImage.open(img_handle)
            img_data = img.getdata()
            if img.mode.startswith('RGB'):
                pixels = [round(.299*p[0] + .587*p[1] + .114*p[2]) for p in img_data]
            elif img.mode == 'LA':
                pixels = [p[0] for p in img_data]
            elif img.mode == 'L':
                pixels = list(img_data)
            else:
                raise ValueError('Unsupported image mode: %r' % img.mode)
            w, h = img.size
            return cls(w, h, pixels)

    @classmethod
    def new(cls, width, height):
        """
        Creates a new blank image (all 0's) of the given height and width.

        Invoked as, for example:
            i = Image.new(640, 480)
        """
        return cls(width, height, [0 for i in range(width*height)])

    def save(self, fname, mode='PNG'):
        """
        Saves the given image to disk or to a file-like object.  If fname is
        given as a string, the file type will be inferred from the given name.
        If fname is given as a file-like object, the file type will be
        determined by the 'mode' parameter.
        """
        out = PILImage.new(mode='L', size=(self.width, self.height))
        out.putdata(self.pixels)
        if isinstance(fname, str):
            out.save(fname)
        else:
            out.save(fname, mode)
        out.close()

    def gif_data(self):
        """
        Returns a base 64 encoded string containing the given image as a GIF
        image.

        Utility function to make show_image a little cleaner.
        """
        buff = BytesIO()
        self.save(buff, mode='GIF')
        return base64.b64encode(buff.getvalue())

    def show(self):
        """
        Shows the given image in a new Tk window.
        """
        global WINDOWS_OPENED
        if tk_root is None:
            # if tk hasn't been properly initialized, don't try to do anything.
            return
        WINDOWS_OPENED = True
        toplevel = tkinter.Toplevel()
        # highlightthickness=0 is a hack to prevent the window's own resizing
        # from triggering another resize event (infinite resize loop).  see
        # https://stackoverflow.com/questions/22838255/tkinter-canvas-resizing-automatically
        canvas = tkinter.Canvas(toplevel, height=self.height,
                                width=self.width, highlightthickness=0)
        canvas.pack()
        canvas.img = tkinter.PhotoImage(data=self.gif_data())
        canvas.create_image(0, 0, image=canvas.img, anchor=tkinter.NW)
        def on_resize(event):
            # handle resizing the image when the window is resized
            # the procedure is:
            #  * convert to a PIL image
            #  * resize that image
            #  * grab the base64-encoded GIF data from the resized image
            #  * put that in a tkinter label
            #  * show that image on the canvas
            new_img = PILImage.new(mode='L', size=(self.width, self.height))
            new_img.putdata(self.pixels)
            new_img = new_img.resize((event.width, event.height), PILImage.NEAREST)
            buff = BytesIO()
            new_img.save(buff, 'GIF')
            canvas.img = tkinter.PhotoImage(data=base64.b64encode(buff.getvalue()))
            canvas.configure(height=event.height, width=event.width)
            canvas.create_image(0, 0, image=canvas.img, anchor=tkinter.NW)
        # finally, bind that function so that it is called when the window is
        # resized.
        canvas.bind('<Configure>', on_resize)
        toplevel.bind('<Configure>', lambda e: canvas.configure(height=e.height, width=e.width))


try:
    tk_root = tkinter.Tk()
    tk_root.withdraw()
    tcl = tkinter.Tcl()
    def reafter():
        tcl.after(500,reafter)
    tcl.after(500,reafter)
except:
    tk_root = None
WINDOWS_OPENED = False

if __name__ == '__main__':
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place for
    # generating images, etc.

    
    # the following code will cause windows from Image.show to be displayed
    # properly, whether we're running interactively or not:
    if WINDOWS_OPENED and not sys.flags.interactive:
        tk_root.mainloop()