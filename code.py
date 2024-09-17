#The documentation for pygame (Which is where the majority fo the code comes from) can be found at https://www.pygame.org/docs/

import pygame #Import the pygame library to make the game
import sys #Just used to close the window instead of having to stop the program?
import random #Import random library to make random number generator for apple
pygame.init() #Allows everything in pygame to be used

SW, SH = 700, 700 #Sets the screen size that the grid and snake use

BLOCK_SIZE = 50 #Sets the size of the blocks that the snake moves along
FONT = pygame.font.Font("font.ttf", BLOCK_SIZE*2) #Makes and sets the size of the font
DIRECTION = "right" #Sets the snakes initial direction
maxscore = 0 #Sets the players initial maxscore

screen = pygame.display.set_mode((1200, 700)) #Sets the actual size of the window that we can put stuff in
pygame.display.set_caption("Snake!") #Titles the window Snake!
clock = pygame.time.Clock() #Starts the clock that controls how often the game updates

class Snake: #Defines the properties and how to generate a snake so the code doesnt have to be rewritten at a later point

    def __init__(self): #Code to make the first snake
        self.x, self.y = BLOCK_SIZE, BLOCK_SIZE #Sets the square size of the snake
        self.xdir = 1 #Resets the snake's x direciton
        self.ydir = 0 #Resets the snake's y direction
        self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE) #Sets the position of the head
        self.body = [pygame.Rect(self.x-BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)] #Sets the position of the body one to the left of the head
        self.dead = False #Makes the snake not dead anymore

    def update(self): #Code that controls what should happen every frame
        global apple

        for square in self.body: #Runs the inside function for each square in the snake's body
            if self.head.x == square.x and self.head.y == square.y: #If the snake's head is in it's body, set the snake to dead
                self.dead = True
            if self.head.x not in range(0, SW) or self.head.y not in range(0, SH): #If the snake's head is outside of the playing area, set the snake to dead
                self.dead = True

        if self.dead: #Specifies what should happen when the snake dies
            self.x, self.y = BLOCK_SIZE, BLOCK_SIZE #Resets the snakes position
            self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE) #Sets the position of the head
            self.body = [pygame.Rect(self.x-BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)] #Sets the position of the body one to the left of the head
            self.xdir = 1 #Resets the snake's x direciton
            self.ydir = 0 #Resets the snake's y direction
            DIRECTION = "right"
            self.dead = False #Makes the snake not dead anymore
            apple = Apple(snake.body) #Makes a new apple

        self.body.append(self.head) #Adds the head to the start of the body
        for i in range(len(self.body)-1): #Runs the following loop for each block in the body
            self.body[i].x, self.body[i].y = self.body[i+1].x, self.body[i+1].y #Moves each block of the body to the block in front of it. This is what makes the body follow the snake head
        self.head.x += self.xdir * BLOCK_SIZE #Moves the head in the x direction
        self.head.y += self.ydir * BLOCK_SIZE #Moves the head in the y direction
        self.body.remove(self.head) #Removes the head from the body

class Apple: #Defines the properties and how to generate an apple so the code doesnt have to be rewritten at a later point
    def __init__(self, snake_body):
        while True:
            self.x = int(random.randint(0, SW - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            self.y = int(random.randint(0, SH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)

            # Check if the apple spawns on the snake's body
            if not any(square.x == self.x and square.y == self.y for square in snake_body):
                break

    def update(self): #Says what should happen every frame
        pygame.draw.rect(screen, "red", self.rect) #Draws the apple


def drawGrid(): #Defines what drawing the grid means so we can easily make the grid at a later point without rewriting all the code
    for x in range(0, SW, BLOCK_SIZE): #Says where in the x direction the grid should be
        for y in range(0, SH, BLOCK_SIZE): #Says where in the y direction the grid should be
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE) #Draws the grid
            pygame.draw.rect(screen, "#3c3c3c", rect, 1) #Draws the grid

#Creates all of the data for the score text
scoretext = FONT.render("Score", True, "white")
scoretext_rect = scoretext.get_rect(center=(950, 100))

#Creates all of the data for the score
score = FONT.render("1", True, "white")
score_rect = score.get_rect(center=(950, 200))

#Creates all of the data for the high score text
highscoretext = FONT.render("High Score", True, "white")
highscoretext_rect = highscoretext.get_rect(center=(950, 500))

#Creates all of the data for where the high score should go
highscore = FONT.render("1", True, "white")
highscore_rect = highscore.get_rect(center=(950, 600))

drawGrid() #Draws the grid that the snake moves along

snake = Snake() #Makes the first snake

apple = Apple(snake.body) #Makes the first apple

while True: #Constantly runs the game code
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #Allows the window to be closed
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN: #Handles changing the snakes direction
            if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and snake.ydir != -1 and snake.xdir != 0: #Check that the down key is pressed and that the snake is not moving up. Then set its direction variable to down
                DIRECTION = "down"
            elif (event.key == pygame.K_UP or event.key == pygame.K_w) and snake.ydir != -1 and snake.xdir != 0: #And these all do the same thing
                 DIRECTION = "up"
            elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and snake.ydir != 0 and snake.xdir != 1:#And these all do the same thing
                DIRECTION = "right"
            elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and snake.ydir != 0 and snake.xdir != 1:#And these all do the same thing
                DIRECTION = "left"

    """
    While it may look redundent to set the varible direction up top and the snakes direction below, the reason we 
        do this is because it prevents the user from changing the direction of the snake multiple times in the game 
        update. If, for example, the user is moving right and then pressed the up key and the left key in the same 
        game update, the snake will end up moving left directly after moving right. This leads the snake to move into 
        its own body and kill itself.

    In the future the goal is to stack inputs so if the user is moving right and quickly presses up and then left, 
        instead of just moving up, it will move up on one game update and then left on the next game update.
    """

    if DIRECTION == "down":
        snake.ydir = 1
        snake.xdir = 0
    elif DIRECTION == "up":
        snake.ydir = -1
        snake.xdir = 0
    elif DIRECTION == "right":
        snake.ydir = 0
        snake.xdir = 1
    elif DIRECTION == "left":
        snake.ydir = 0
        snake.xdir = -1
    DIRECTION = 0 #The direction is set to 0 here so if the snake dies it doesnt keep the direction it had before it died

    snake.update() #This updates the snake so it can move to the diffirent spot. Also checks if it is dead, on an apple, etc

    screen.fill('black') #This removes the snake and apples from their last position so you only see the most recent update of the snake
    drawGrid() #This draws the square grid that the snake is moving along so the user knows where they can go

    apple.update() #Updates the apple so it can check if it has been eaten

    score = FONT.render(f"{len(snake.body) -1}", True, "white") #Renders the score

    if len(snake.body) > maxscore: #Checks the recorded maxscore against the current score and sets the higher one as maxscore
        maxscore = len(snake.body)

    highscore = FONT.render(f"{maxscore -1}", True, "white") #Renders the high score


    pygame.draw.rect(screen, "green", snake.head) #Draws the snake head. This is seperate because it has different properties than the body

    for square in snake.body: #Draws each square that is contained in snake.body
        pygame.draw.rect(screen, "green", square)

    screen.blit(score, score_rect) #Actually displays the current score
    screen.blit(highscore, highscore_rect) #Actually displays the highscore
    screen.blit(scoretext, scoretext_rect) #Actually displays the text saying score
    screen.blit(highscoretext, highscoretext_rect) #Actually displays the text saying highscore

    if snake.head.x == apple.x and snake.head.y == apple.y: #Checks if the snake's head is on an apple
        snake.body.append(pygame.Rect(square.x, square.y, BLOCK_SIZE, BLOCK_SIZE)) #If the head is on an apple it makes the body one square longer
        apple = Apple(snake.body) #If the head is on an apple it makes a new apple



    pygame.display.update() #Updates the display after all of the backend code had run
    clock.tick(5) #Controls the speed of the game
