import turtle
import math
import winsound
import random

#To locate the file - cd Desktop\Python Practice\Space Invaders

#Challenge:
#1. Implement a level up system with additional enemies and speed - DONE (speed)
#2. Reset enemies when they go beyond the floor - DONE
#3. Have bonuses available that allows rocket upgrade
#4. Let the player win after they get a certain amount of score

#Set up the screen
canvas = turtle.Screen()
canvas.bgcolor("black")
canvas.title("Space Invaders")
canvas.bgpic("sparkles.gif")

#Shape registry
turtle.register_shape("spaceship_small.gif")
turtle.register_shape("enemy.gif")
turtle.register_shape("rocket.gif")

#Drawing a border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-300,-300)
border_pen.pendown()
border_pen.pensize(3)
for side in range(4):
	border_pen.fd(600)
	border_pen.lt(90)
border_pen.hideturtle()

#Set the score
score = 0

#Draw the score
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290,270)
scorestring = "Score: {}".format(score)
score_pen.write(scorestring, False, align="left", font=("Arial",14, "normal"))
score_pen.hideturtle()

#Create the player
player = turtle.Turtle()
player.shape("spaceship_small.gif")
player.penup()
player.speed(0)
player.setposition(0,-250)
player.setheading(90)

playerspeed = 20

#Multiple enemies
enemy_number = 5
enemies = []

#Adding enemies to list
for i in range(enemy_number):
	#Create an enemy
	enemies.append(turtle.Turtle())

for enemy in enemies:
	enemy.shape("enemy.gif")
	enemy.penup()
	enemy.speed(0)
	enemy.shapesize(1.5,1.5)
	x = random.randint(-200,200)
	y = random.randint(150,250)
	enemy.setposition(x,y)

enemyspeed = 3

#Create rockets
rocket = turtle.Turtle()
rocket.color("yellow")
rocket.shape("rocket.gif")
rocket.penup()
rocket.speed(0)
rocket.setheading(90)
rocket.shapesize(0.5,0.5)
rocket.hideturtle()

rocketspeed = 25

#Define rocket state - ready & fire
rocketstate = "ready"

#Player movement
def move_left():
	x = player.xcor()
	x -= playerspeed
	if x < -280:
		x = -280
	player.setx(x)

def move_right():
	x = player.xcor()
	x += playerspeed
	if x > 280:
		x = 280
	player.setx(x)


#Player rockets
def fire_rocket():
	#Declare rocketstate as a global if it needs to be changed
	global rocketstate
	#Move rockets
	if rocketstate == "ready":
		winsound.PlaySound("laser.wav", winsound.SND_ASYNC)
		rocketstate = "fire"
		x = player.xcor()
		y = player.ycor() + 15
		rocket.setposition(x,y)
		rocket.showturtle()

def isCollision(t1,t2):
	distance = math.sqrt( math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2) )
	if distance < 20:
		return True
	else:
		return False



#Keyboard bindings
turtle.listen()
turtle.onkey(move_left, "Left")
turtle.onkey(move_right, "Right")
turtle.onkey(fire_rocket, "space")

#Main game loop
while True:

	#Increase Game difficulty
	if score >= 50 and score < 100:
		if enemyspeed > 0:
			enemyspeed = 5
		else:
			enemyspeed = -5
	elif score >= 100 and score < 150:
		if enemyspeed > 0:
			enemyspeed = 7
		else:
			enemyspeed = -7
	elif score >= 150 < 200:
		if enemyspeed > 0:
			enemyspeed = 8
		else:
			enemyspeed = -8
    #Condition for winning

#Loop through each enemy element in the enemies array
	for enemy in enemies:
		#Move the enemy
		x = enemy.xcor()
		x += enemyspeed
		enemy.setx(x)

		#When enemy goes bellow screen
		if enemy.ycor() < -280:
			y = enemy.ycor()
			y += 400
			enemy.sety(y)

		#Move the enemy when it reaches the wall
		if enemy.xcor() >= 280:
			#Move all enemies down and backwards
			for e in enemies:
				x = e.xcor()
				x = 275
				y = e.ycor()
				y -= 40
				e.sety(y)
			enemyspeed *= -1

		if enemy.xcor() <= -280:
			#Move all enemies down and backwards
			for e in enemies:
				x = e.xcor()
				x = -275
				y = e.ycor()
				y -= 40
				e.sety(y)
			enemyspeed *= -1

		#Check for collision for the rockets
		if isCollision(rocket,enemy):
			winsound.PlaySound("explosion.wav", winsound.SND_ASYNC)
			#reset the rocket
			rocket.hideturtle()
			rocketstate = "ready"
			rocket.setposition(0,-400)
			#Reset the enemy
			x = random.randint(-200,200)
			y = random.randint(100,200)
			enemy.setposition(x,y)
			#Update score
			score += 10
			scorestring = "Score: {}".format(score)
			score_pen.clear()
			score_pen.write(scorestring, False, align="left", font=("Arial",14, "normal"))
            
        #Collision between player and enemy
		if isCollision(player, enemy):
			player.hideturtle()
			enemies = []
			game_over = turtle.Turtle()
			game_over.speed(0)
			game_over.color("white")
			game_over.penup()
			game_over.setposition(0,0)
			gameoverstring = "Game Over"
			game_over.write(gameoverstring, False, align="center", font=("Arial",20, "normal"))
			game_over.hideturtle()
			print("Game Over")
			break

	#Move the rocket
	if rocketstate == "fire":
		y = rocket.ycor()
		y += rocketspeed
		rocket.sety(y)

	#Check if rocket reaches top
	if rocket.ycor() > 275:
		rocket.hideturtle()
		rocketstate = "ready"


canvas.mainloop()
