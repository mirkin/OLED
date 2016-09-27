#!/usr/bin/python
from Adafruit_I2C import Adafruit_I2C
import time
from PIL import ImageFont,Image,ImageDraw
buffer=[0x00]*(1024) # 128 columns x 8 pages

SSD1306_DISPLAY_OFF=0xAE
SSD1306_DISPLAY_ON=0xAF
SSD1306_DISPLAY_ALL_ON=0xA5
SSD1306_SET_FREQUENCY=0xD5 # suggested 0x80
SSD1306_SET_MUX_RATIO=0xA8 # multiplex ration suggested 0x3F
SSD1306_SET_DISPLAY_OFFSET=0xD3
SSD1306_SET_START_LINE=0x40
SSD1306_ENABLE_CHARGE_PUMP=0x8D # 0x14 enable charge pump

SSD1306_SET_COLUMN_ADDRESS=0x21 # followed by start then end column
SSD1306_SET_PAGE_ADDRESS=0x22 # followed by start then end page

SSD1306_SET_NORMAL_DISPLAY=0xA6
SSD1306_SET_INVERSE_DISPLAY=0xA7

SSD1306_ENTIRE_DISPLAY_ON=0xA4 # output follows ram content

SSD1306_SET_SCAN_DIRECTION_NORMAL=0xC0
SSD1306_SET_SCAN_DIRECTION_FLIP=0xC8
SSD1306_SET_ADDRESSING_MODE_HORIZONTAL=0x20 # follow with 0x00 for horizontal
SSD1306_SET_COM_PINS=0xDA #
SSD1306_SET_SEGMENT_REMAP=0xA0 # A0 SEG0 0 A1 SEG0 127

i2c=Adafruit_I2C(address=0x3c)

def command(c):
    i2c.write8(0x00,c)

def data(c):
    i2c.write8(0x40,c)

def setPixel(x,y,v):
    yy=63-y
    xx=x
    if v:
        buffer[( xx << 3) + yy//8]|=1 << (yy % 8);
    else:
        buffer[( xx << 3)+ yy//8]&=0xff-(1 << (yy % 8));

command(SSD1306_DISPLAY_OFF)
command(SSD1306_SET_FREQUENCY)
command(0x80)
command(SSD1306_SET_MUX_RATIO)
command(0x3F)
command(SSD1306_SET_DISPLAY_OFFSET)
command(0x00)
command(SSD1306_SET_START_LINE | 0x0) # line 0
command(SSD1306_ENABLE_CHARGE_PUMP)
command(0x14)
command(SSD1306_SET_ADDRESSING_MODE_HORIZONTAL)
command(0x01)
command(SSD1306_SET_SEGMENT_REMAP | 0x01)
# Need to do this before we set column and page address ranges
# command(SSD1306_SET_SCAN_DIRECTION_FLIP)
command(SSD1306_SET_SCAN_DIRECTION_NORMAL)
command(SSD1306_SET_COM_PINS)
command(0x12)
# command(SSD1306_DISPLAY_ALL_ON)
command(SSD1306_ENTIRE_DISPLAY_ON)
command(SSD1306_DISPLAY_ON)
command(SSD1306_SET_NORMAL_DISPLAY)
command(SSD1306_SET_COLUMN_ADDRESS)
command(0x00)
command(0x7f) # 127
# command(0x3f) # 63
command(SSD1306_SET_PAGE_ADDRESS)
command(0x00)
command(0x07)
# for i in range(0,1024):
    # time.sleep(1)
    # # i2c.writeList(0x40,[0x55]*16)
    # data(0xff)
font=ImageFont.truetype('fonts/Roboto-Regular.ttf',12)
font2=ImageFont.truetype('fonts/Roboto-Regular.ttf',14)
image=Image.new('1',(128,64))
draw=ImageDraw.Draw(image)
# draw.rectangle((30,30,100,60),outline=255,fill=0)
draw.text((0,0),"SSD1306 I2C RasPi Test",font=font,fill=255)
draw.text((0,15),"--0123456789--",font=font,fill=255)
draw.text((0,30),"[Game Over]",font=font,fill=255)
draw.text((0,45),"Play Again ????????",font=font2,fill=255)
pix=list(image.getdata())
for y in range(0,64):
    for x in range(0,128):
        setPixel(x,y,pix[y*128+x])
image.save("test.png","PNG")
# for i in range(0,63):
    # setPixel(i,i,1)
# for i in range(0,127):
    # setPixel(i,0,1)
for i in range(0,64):
    i2c.writeList(0x40,buffer[i*16:i*16+16])
