# ----- IMPORT STATEMENTS ----
import turtle as trtl
import random
from turtle import Screen, Turtle
from threading import Thread, active_count
from queue import Queue
import time


# ----- BACKGROUND -----
# add background image from files
wn = trtl.Screen()
wn.bgpic("background.gif")

# ----- START BUTTON -----
wn = trtl.Screen()
trtl.hideturtle() 

# draw start button
def start_button():

  trtl.speed(0)
  
  trtl.penup()
  trtl.setposition(-100,0)
  trtl.pencolor("lightsteelblue")
  trtl.pensize(3)
  trtl.pendown()
  
  for i in range(2):
    trtl.forward(220)
    trtl.left(90)
    trtl.forward(60)
    trtl.left(90) 
    
  trtl.penup()
  trtl.goto(-90,20)
  trtl.pendown()
  trtl.color("lightsteelblue")
  trtl.write("PRESS [SPACE] TO START!", font=("Verdana",10,"bold"))

# clear start button when pressed
def start_pressed():
  trtl.clear()

wn.listen()
wn.onkey(start_pressed,'space')
  
start_button()


# ----- PLAYER NAME -----
# create a box for asking for the user's name
def name_box():
  text = "ENTER YOUR NAME: "
  box = wn.textinput("PUPPY PRANCE", text)
  return box 

player_name = name_box()

name = trtl.Turtle()
name.color("steelblue")
name.hideturtle()
name.penup()
name.goto(-220,160)

display_name = player_name.upper()
name.write(str(display_name), font=("Verdana",18,"bold"))


# ----- DOG MOVEMENT -----
QUEUE_SIZE = 1
screen = Screen()
actions = Queue(QUEUE_SIZE)  # a thread-safe data structure

def process_queue():
  while not actions.empty():
    action, *arguments = actions.get()
    action(*arguments)

  if active_count() > 1:
    screen.ontimer(process_queue, 10)

# add dog images from files as frames
wn.addshape('frame1.gif')
wn.addshape('frame2.gif')
wn.addshape('frame3.gif')
wn.addshape('frame4.gif')
wn.addshape('frame5.gif')
wn.addshape('frame6.gif')
wn.addshape('frame7.gif')
wn.addshape('frame8.gif')

is_jumping = False

# reposition frames to make dog appear to jump
def dog_animation(dog):
  global is_jumping
  is_jumping = True
    
  actions.put((dog.turtlesize, 0.001))  
  actions.put((dog.goto, (-150, -80)))
  actions.put((dog.turtlesize, 1))  

  actions.put((dog.shape,("frame1.gif")))

  actions.put((dog.left,(90)))
  actions.put((dog.forward,(40)))
  actions.put((dog.shape,("frame3.gif")))
  time.sleep(0.1)

  actions.put((dog.forward,(40)))
  actions.put((dog.shape,("frame5.gif")))
  time.sleep(0.1)

  actions.put((dog.right,(180)))
  actions.put((dog.forward,(40)))
  actions.put((dog.shape,("frame7.gif")))
  time.sleep(0.2)

  actions.put((dog.forward,(40)))
  actions.put((dog.shape,("frame1.gif")))
  time.sleep(0.2)

  actions.put((dog.left,(90)))

  is_jumping = False

# detect if dog and ball have collided
def is_collided_with():
  global dog, ball
  dx = abs(dog.xcor() - ball.xcor())
  dy = abs(dog.ycor() - ball.ycor())
  # print ("dx = " + str(dx) + "  dy = " + str(dy))

  if dx < 60 and dy < 80:
    return True
  else:  
    return False


# ----- BALL MOVEMENT -----
# lists for random ball color and shape
ball_colors = ["lightsteelblue", "lightsalmon", "lemonchiffon", "cadetblue", "honeydew", "thistle"]
ball_shapes = ["turtle", "circle", "square", "triangle"]

# move ball across screen repeatedly
def ball_move(ball):
  quit = False
  while quit == False:    
    # minumun ball size is 0.001 since cannot run "hideturtle()"
    actions.put((ball.turtlesize, 0.001))

    # 
    actions.put((ball.color, ball_colors[random.randint(0,5)]))

    # actions.put((ball.shape, ball_shapes[random.randint(0,3)]))
    actions.put((ball.shape, 'circle'))

    # reset ball position to right
    actions.put((ball.goto, (300, -140)))

    # restore ball size to normal
    actions.put((ball.turtlesize, 2))  

    # move ball to left
    for i in range(120):
      actions.put((ball.backward, 5))

      if is_collided_with():
        game_over()
        quit = True
        break

# ----- GAME -----
# create new turtle for ball
ball = Turtle('circle', visible=False)
ball.speed('slow')
ball.color('lightsteelblue')
ball.turtlesize(2)
ball.penup()
ball.showturtle()

# create new turtle for dog
dog = trtl.Turtle()
dog.color("lightsteelblue")
dog.turtlesize(0.001)
dog.penup()

def dog_thread():
  global is_jumping
  global dog

  if is_jumping == True:
    return

  Thread(target=dog_animation, args=[dog], daemon=True).start()
 
wn.onkeypress(dog_thread, "space")
wn.listen()

Thread(target=ball_move, args=[ball], daemon=True).start()


# ----- TIMER -----
# create new turtle for timer
counter = trtl.Turtle()
counter.color("steelblue")

counter.hideturtle()
counter.penup()
counter.goto(85,160)

timer = 0
counter_interval = 1000

# draw a timer incrementing by seconds
def countup():
  global timer, timer_up
  counter.clear()
  counter.write("TIMER: " + str(timer), font=("Verdana",18,"bold"))
  timer = timer + 1
  counter.getscreen().ontimer(countup, counter_interval)

wn.ontimer(countup, counter_interval)


# ----- GAME OVER SCREEN -----
# draw game over screen
def game_over():
  trtl.speed(0)
  trtl.penup()
  trtl.setposition(-100,0)
  trtl.pencolor("lightsteelblue")
  trtl.pendown()
  
  for i in range(2):
    trtl.forward(220)
    trtl.left(90)
    trtl.forward(60)
    trtl.left(90) 
    
  trtl.penup()
  trtl.goto(-55,20)
  trtl.pendown()
  trtl.color("lightsteelblue")
  trtl.write("GAME OVER :(", font=("Verdana",12,"bold"))

  trtl.penup()
  trtl.setposition(-55,125)
  trtl.pendown()
  trtl.color("steelblue")
  trtl.write("YOUR SCORE: ", font=("Verdana",12,"bold"))

  trtl.penup()
  trtl.setposition(0,90)
  trtl.pendown()
  trtl.color("steelblue")
  trtl.write(timer, font=("Verdana",18,"bold"))
  
  '''
  trtl.hideturtle()
  trtl.penup()
  trtl.setposition(-115,-70)
  trtl.showturtle()
  trtl.pendown()
  trtl.color("white")
  trtl.write("PRESS [ENTER] TO CONTINUE", font=("Verdana",12,"bold"))
  trtl.penup()
  trtl.setposition(-50, 90)
  trtl.hideturtle()
  '''

process_queue()

'''
def press():
  trtl.clear()
  start_button()

wn.listen()
wn.onkey(press,'enter')
'''

wn.mainloop()
