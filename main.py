from machine import Pin,SPI,PWM
from LCD_1inch8 import LCD_1inch8
import framebuf
# import time
import utime
import random
import math

BL = 13

# if __name__=='__main__':
# 
#     LCD = LCD_1inch8()
#     #color BRG
#     LCD.fill(LCD.WHITE)
#  
#     LCD.show()
#     
#     LCD.fill_rect(0,0,160,20,LCD.RED)
#     LCD.rect(0,0,160,20,LCD.RED)
#     LCD.text("Raspberry Pi Pico",2,8,LCD.WHITE)
#     
#     LCD.fill_rect(0,20,160,20,LCD.BLUE)
#     LCD.rect(0,20,160,20,LCD.BLUE)
#     LCD.text("PicoGo",2,28,LCD.WHITE)
#     
#     LCD.fill_rect(0,40,160,20,LCD.GREEN)
#     LCD.rect(0,40,160,20,LCD.GREEN)
#     LCD.text("Pico-LCD-1.8",2,48,LCD.WHITE)
#     
#     LCD.fill_rect(0,60,160,10,0X07FF)
#     LCD.rect(0,60,160,10,0X07FF)
#     LCD.fill_rect(0,70,160,10,0xF81F)
#     LCD.rect(0,70,160,10,0xF81F)
#     LCD.fill_rect(0,80,160,10,0x7FFF)
#     LCD.rect(0,80,160,10,0x7FFF)
#     LCD.fill_rect(0,90,160,10,0xFFE0)
#     LCD.rect(0,90,160,10,0xFFE0)
#     LCD.fill_rect(0,100,160,10,0XBC40)
#     LCD.rect(0,100,160,10,0XBC40)
#     LCD.fill_rect(0,110,160,10,0XFC07)
#     LCD.rect(0,110,160,10,0XFC07)
#     LCD.fill_rect(0,120,160,10,0X8430)
#     LCD.rect(0,120,160,10,0X8430)
# 
# 
#             
#             
#     LCD.show()
#     time.sleep(1)
#     LCD.fill(0xFFFF)

pwm = PWM(Pin(BL))
pwm.freq(1000)

pwm.duty_u16(32768) # max 65535
LCD = LCD_1inch8()
# Background colour is BLACK
LCD.fill(0x0) # BLACK
LCD.show()
# ============= END OF SCREEN DRIVER & SETUP ==================


def colour(R,G,B):
# Get RED value
    rp = int(R*31/255) # range 0 to 31
    if rp < 0: rp = 0
    r = rp *8
# Get Green value - more complicated!
    gp = int(G*63/255) # range 0 - 63
    if gp < 0: gp = 0
    g = 0
    if gp & 1:  g = g + 8192
    if gp & 2:  g = g + 16384
    if gp & 4:  g = g + 32768
    if gp & 8:  g = g + 1
    if gp & 16: g = g + 2
    if gp & 32: g = g + 4
# Get BLUE value       
    bp =int(B*31/255) # range 0 - 31
    if bp < 0: bp = 0
    b = bp *256
    colour = r+g+b
    return colour
    
def ring(cx,cy,r,cc):   # Centre (x,y), radius
    for angle in range(0, 90, 2):  # 0 to 90 degrees in 2s
        y3=int(r*math.sin(math.radians(angle)))
        x3=int(r*math.cos(math.radians(angle)))
        LCD.pixel(cx-x3,cy+y3,cc)  # 4 quadrants
        LCD.pixel(cx-x3,cy-y3,cc)
        LCD.pixel(cx+x3,cy+y3,cc)
        LCD.pixel(cx+x3,cy-y3,cc)
#=============== MAIN ============

LCD.rect(0,0,159,127,colour(0,0,255)) # Blue Frame
LCD.text("WaveShare", 38,20,colour(255,0,0))
LCD.text('Pico Display 1.8"', 10,40,colour(255,255,0))
LCD.text("159x128 SPI", 30,60,colour(0,255,0))
LCD.text("WORKOUT", 50,80,colour(255,128,0))
LCD.text("Tony Goodhew", 30,110,colour(100,100,100))
LCD.show()
utime.sleep(6)
LCD.fill(0)
LCD.show()

LCD.rect(0,0,159,127,colour(0,0,255)) # Blue Frame
# White Corners
LCD.pixel(0,0,0xFFFF)     # LT
LCD.pixel(0,127,0xFFFF)   # LB
LCD.pixel(159,0,0xFFFF)   # RT
LCD.pixel(159,127,0xFFFF) # RB
LCD.text("200 Pixels", 40,20,0xFFFF)
LCD.rect(29,49,103,53,colour(0,255,0))
LCD.show()
for i in range (200):
    x = random.randint(30, 130)
    y = random.randint(50, 100)
    LCD.pixel(x,y,0xFFFF)
    LCD.show()
utime.sleep(1.5)
LCD.fill(0)
LCD.show()

# Lines
LCD.text("Lines",10,10,colour(200,200,200))
LCD.show()
c = colour(255,0,0)
b = colour(0,0,255)
LCD.vline(0,0,127,c)
LCD.hline(0,127,127,c)
LCD.vline(159,0,127,b)
LCD.hline(159-127,1,128,b)
for i in range(0,127,5):
    ii = i +1
    LCD.line(1,ii,ii,128,c)
    LCD.line(159,128-ii,159-ii,1,b)
    utime.sleep(0.03)
    LCD.show()

LCD.text("Circles",95,112,colour(200,200,200))
LCD.show()
ring(80,64,47,colour(70,70,70))
ring(80,64,41,colour(100,100,100))
ring(80,64,35,colour(150,150,150))
LCD.show()
ring(80,64,30,colour(255,255,0))
ring(80,64,25,colour(255,0,255))
ring(80,64,20,colour(0,255,255))
LCD.show()
utime.sleep(1)
for r in range(5):
    ring(80,64,10+r,colour(255,0,0))
LCD.show()
utime.sleep(1)
for r in range(5):
    ring(80,64,5+r,colour(0,255,0))
LCD.show()
utime.sleep(1)
for r in range(5):
    ring(80,64,r,colour(0,0,255))
LCD.show()
utime.sleep(2.5)
LCD.fill(0)
LCD.show()

# === Sin & Cos graphs ====
factor = 361 /159    
LCD.show()
cr = colour(255,0,0)
LCD.hline(1,60,159,0xFFFF)
LCD.text("Sine", 70, 20, cr)
for x in range(1,159):
    y = int ((math.sin(math.radians(x * factor)))* -50) + 60
    LCD.pixel(x,y,cr)
    LCD.show()
LCD.show()

cg = colour(0,255,0)
LCD.text("Cosine", 5, 90, cg)
for x in range(0,240):
    y = int((math.cos(math.radians(x * factor)))* -50) + 60
    LCD.pixel(x,y,cg)
LCD.show()
utime.sleep(3)
LCD.fill(0)
LCD.show()

# Text on a Sin wave
msg ='  WS Pico Display'
LCD.text("Text on a Sine Curve",1,115,0xFFFF)
factor = 361 /159
for i in range(len(msg)):
    y = int ((math.sin(math.radians(i*7 * factor)))* -40) + 40
    ch = msg[i]
    LCD.text(ch, i*8,y +10,colour(255,255,0))
    LCD.show()
utime.sleep(3)
LCD.fill(0)
LCD.show()

# Set up potentiometers
rpot=machine.ADC(28)
gpot=machine.ADC(27)
bpot=machine.ADC(26)
LCD.fill(0)
LCD.show()
LCD.text(" Turn the Pots",20,112,0xFFFF)
LCD.hline(0,127,159,0xFFFF) # Draw edge frame Bottom
LCD.line(0,1,159,1,0xFFFF)                  # Top  
LCD.vline(0,1,127,0xFFFF)                   # Left
LCD.line(159,0,159,127,0xFFFF)              # Right
while True:
# Get RED value
    rp = int(rpot.read_u16() / 2000) # range 0 to 31
    if rp < 0: rp = 0
    if rp > 31: rp = 31
    r = rp *8
# Get Green value - more complicated!
    gp = int(gpot.read_u16() / 1000) # range 0 - 63
    if gp < 0: gp = 0
    if gp > 63: gp = 63
    g = 0
    if gp & 1:  g = g + 8192
    if gp & 2:  g = g + 16384
    if gp & 4:  g = g + 32768
    if gp & 8:  g = g + 1
    if gp & 16: g = g + 2
    if gp & 32: g = g + 4
# Get BLUE value       
    bp =int(bpot.read_u16() / 2090) # range 0 - 31
    if bp < 0: bp = 0
    if bp > 31: gp = 31
    b = bp *256

    colour = r+g+b

    LCD.fill_rect(4,20,152,20,colour)
    LCD.fill_rect(50,5,80,10,0) # Black out old value
    LCD.text(str(hex(colour)),58,7,0xFFFF)
    
    LCD.fill_rect(10,55,140,10,0)
    LCD.text(str(rp),10,55,0xF8) # RED
    LCD.fill_rect(120,55,25,10,r)
    LCD.rect(120,55,25,10,0xAA52) # Grey2 frame
    if rp > 0: LCD.fill_rect(35,55,rp*2,10,0x76AD) # GREY
    
    LCD.fill_rect(10,75,140,10,0)
    LCD.text(str(gp),10,75,0xE007) # GREEN
    LCD.fill_rect(120,75,25,10,g)
    LCD.rect(120,75,25,10,0xAA52)
    if gp > 0: LCD.fill_rect(35,75,gp,10,0x76AD)
    
    LCD.fill_rect(10,95,140,10,0)
    LCD.text(str(bp),10,95,0x1F00) # BLUE   
    LCD.fill_rect(120,95,25,10,b)
    LCD.rect(120,95,25,10,0xAA52)
    if bp > 0: LCD.fill_rect(35,95,bp*2,10,0x76AD)
    
    LCD.show()



