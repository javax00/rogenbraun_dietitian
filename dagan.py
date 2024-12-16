import pyautogui as pg
import random
import time

def ri(int1, int2):
	return random.randint(int1, int2)

s = open("random.txt", "r")
data = s.read()
words = data.split('\n')

pg.FAILSAFE = False

while True:
	# MOUSE MOVE
	ss = pg.size()
	pg.moveTo(ri(10,ss[0]), ri(10,ss[1]), duration=ri(1,5), tween=pg.easeInOutQuad)
	time.sleep(ri(20,120))

	#CHANGE TAB
	pg.click(x=25, y=250)
	for t in range(3, ri(4,10)):
		pg.hotkey('ctrl', str(ri(3,9)), interval=.5)
		pg.scroll(ri(-100, 100))
		time.sleep(ri(10,80))

	# KEYBOARD TYPE
	for t in range(5, ri(5,50)):
		pg.click(x=0, y=0)
		time.sleep(ri(1, 5))
	for t in range(5, ri(5,25)):
		pg.write(words[ri(10,10000)], interval=.25)
	time.sleep(ri(20,120))

	# MOUSE MOVE
	ss = pg.size()
	pg.moveTo(ri(10,ss[0]), ri(10,ss[1]), duration=ri(1,5), tween=pg.easeInOutQuad)
	time.sleep(ri(20,120))

	#CHANGE TAB
	pg.click(x=25, y=250)
	for t in range(3, ri(4,10)):
		pg.hotkey('ctrl', str(ri(3,9)), interval=.5)
		pg.scroll(ri(-100, 100))
		time.sleep(ri(10,80))

	#ALT TAB
	pg.hotkey('alt', 'tab', interval=.5)
	time.sleep(ri(20,120))

	# MOUSE MOVE
	ss = pg.size()
	pg.moveTo(ri(10,ss[0]), ri(10,ss[1]), duration=ri(1,5), tween=pg.easeInOutQuad)
	time.sleep(ri(20,120))

	#CHANGE TAB
	pg.click(x=25, y=250)
	for t in range(3, ri(4,10)):
		pg.hotkey('ctrl', str(ri(3,9)), interval=.5)
		pg.scroll(ri(-100, 100))
		time.sleep(ri(10,80))

	# SCROLL
	for t in range(5, ri(5,50)):
		pg.click(x=25, y=250)
		time.sleep(ri(1, 5))
	for t in range(5, ri(10,100)):
		pg.scroll(ri(-100, 100))
		time.sleep(ri(2,10))
	time.sleep(ri(20,120))

	# MOUSE MOVE
	ss = pg.size()
	pg.moveTo(ri(10,ss[0]), ri(10,ss[1]), duration=ri(1,5), tween=pg.easeInOutQuad)
	time.sleep(ri(20,120))

	#CHANGE TAB
	pg.click(x=25, y=250)
	for t in range(3, ri(4,10)):
		pg.hotkey('ctrl', str(ri(3,9)), interval=.5)
		pg.scroll(ri(-100, 100))
		time.sleep(ri(10,80))

	#ALT TAB
	pg.hotkey('alt', 'tab', interval=.5)
	time.sleep(ri(20,120))
