import pygame, random, json
from time import sleep

# Define classes for different screens (Scoreboard, Ready, Game, Result, Winner)
# =======================
# State 1 - Scoreboard
# State 2 - Ready
# State 4 - Game
# State 5 - Result
# State 6 - Winner
# =======================

class Scoreboard:
    """
    Class for displaying the scoreboard.
    """
    def __init__(self, WIDTH, HEIGHT, BACKGROUND):
        """
        Initializes the scoreboard with labels and texts.
        """
        # Initialize variables
        self.offset = 50
        self.player1_score, self.player2_score = 0, 0
        self.BACKGROUND = BACKGROUND
        self.dimensions = (WIDTH, HEIGHT)

        # Initialize labels and texts
        self.TextLabel = self.render_text("Scoreboard", 100, (WIDTH // 2, 50 + self.offset))
        self.playerOneTextLabel = self.render_text("Player 1", 60, (150, 150 + self.offset))
        self.playerOneScoreText = self.render_text(str(self.player1_score), 60, (150, 300 + self.offset))
        self.dividerTextLabel = self.render_text("|", 100, (WIDTH // 2, HEIGHT // 2))
        self.playerTwoTextLabel = self.render_text("Player 2", 60, (WIDTH - 150, 150 + self.offset))
        self.playerTwoScoreText = self.render_text(str(self.player2_score), 60, (WIDTH - 150, 300 + self.offset))

    def render_text(self, text, size, center):
        """
        Renders text using the specified font size and position.
        """
        font = pygame.font.Font('freesansbold.ttf', size)
        text_surface = font.render(text, True, (0, 0, 0), self.BACKGROUND)
        text_rect = text_surface.get_rect(center=center)
        return text_surface, text_rect

    def render(self):
        """
        Renders the scoreboard on the screen.
        """
        screen.blit(self.TextLabel[0], self.TextLabel[1])
        screen.blit(self.playerOneTextLabel[0], self.playerOneTextLabel[1])
        screen.blit(self.playerOneScoreText[0], self.playerOneScoreText[1])
        screen.blit(self.dividerTextLabel[0], self.dividerTextLabel[1])
        screen.blit(self.playerTwoTextLabel[0], self.playerTwoTextLabel[1])
        screen.blit(self.playerTwoScoreText[0], self.playerTwoScoreText[1])

    def update(self, player1_score, player2_score):
        """
        Updates the scores on the scoreboard.
        """
        self.playerOneScoreText = self.render_text(str(player1_score), 60, (150, 300 + self.offset))
        self.playerTwoScoreText = self.render_text(str(player2_score), 60, (self.dimensions[0] - 150, 300 + self.offset))

class Ready:
    """
    Class for displaying the "Ready" screen.
    """
    def __init__(self, WIDTH, HEIGHT, BACKGROUND, count=3):
        """
        Initializes the "Ready" screen.
        """
        self.offset = 55
        self.original_count = count 
        self.count = count
        self.label = "Ready in"
        self.dimensions = (WIDTH, HEIGHT)
        self.BACKGROUND = BACKGROUND

        self.TextLabel, self.TextRect = self.render_text(self.label, 100, (WIDTH // 2, HEIGHT // 2 - self.offset))
        self.TextLabelScore, self.TextRectScore = self.render_text(str(self.count), 100, (WIDTH // 2, HEIGHT // 2 + self.offset))

    def render_text(self, text, size, center):
        """
        Renders text using the specified font size and position.
        """
        font = pygame.font.Font('freesansbold.ttf', size)
        text_surface = font.render(str(text), True, (0, 0, 0), self.BACKGROUND)
        text_rect = text_surface.get_rect(center=center)
        return text_surface, text_rect

    def render(self):
        """
        Renders the "Ready" screen on the screen.
        """
        self.update()
        screen.blit(self.TextLabel, self.TextRect)
        screen.blit(self.TextLabelScore, self.TextRectScore)

    def update(self):
        """
        Updates the "Ready" screen.
        """
        self.TextLabel, self.TextRect = self.render_text(self.label, 100, (self.dimensions[0] // 2, self.dimensions[1] // 2 - self.offset))
        self.labelscore = self.count
        self.TextLabelScore, self.TextRectScore = self.render_text(str(self.labelscore), 100, (self.dimensions[0] // 2, self.dimensions[1] // 2 + self.offset))
        if self.count >  0:
            self.count -= 1

    def reset(self):
        """
        Reset the count
        """
        self.count = self.original_count

class Game:
    def __init__(self, WIDTH, HEIGHT, BACKGROUND, WINDOW, question_list, count = 1000):
        # Set up the game window
        self.width, self.height = WIDTH, HEIGHT
        self.window = WINDOW

        # Set up colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BACKGROUND = BACKGROUND

        # Timer
        self.original_count = count 
        self.count = count

        # Load game fonts
        self.font = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()
        self.gameover = False

        self.score = 0
        self.user_answer = None

        ## 
        self.question_list = question_list
        self.question_list_original = question_list

        self.question = ''
        self.image = 'image.png' # Image Path
        self.answer = None # Boolean

        self.offset = 55
        self.original_count, self.count = count, count
        self.scale = 0.75
        self.dimensions, self.BACKGROUND = (WIDTH, HEIGHT), BACKGROUND
        self.load_new_question()

    def load_new_question(self):
        if len(self.question_list) == 1:
            self.question_list_original = self.question_list
        temp = random.choice(self.question_list)
        self.question = temp['question']
        self.image = temp['url']
        self.answer = temp['answer']
         
    def render_text(self, text, size, center):
        """
        Renders text using the specified font size and position.
        """
        font = pygame.font.Font('freesansbold.ttf', size)
        text_surface = font.render(str(text), True, (0, 0, 0), self.BACKGROUND)
        text_rect = text_surface.get_rect(center=center)
        return text_surface, text_rect

    def run(self):
        running = True
        while running and not(self.gameover):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.checkAnswer()
                        self.user_text = ''
                    elif event.key == pygame.K_y:
                        self.user_answer = True
                        self.checkAnswer()
                    elif event.key == pygame.K_n:
                        self.user_answer = False
                        self.checkAnswer()
                
            self.render()
            self.clock.tick(60)

    def checkAnswer(self):
        if self.answer == self.user_answer:
            self.score = self.score + 1
            self.load_new_question()
        else:
            self.gameover = True

    def update(self):
        if self.count >= 0: 
            self.count -= 1
            sleep(0.01)
        else:
            self.gameover = True 

    def restart(self):
        self.count = self.original_count
        self.gameover = False 
        self.score = 0
    
    def setImage(self, image_path):
        # Load an image using Pygame
        image = pygame.image.load('Asset/' + image_path)

        w, h = image.get_width(), image.get_height()

        target_w = self.dimensions[0] * 0.7

        # Resize the image
        new_width, new_height = target_w, (target_w * (h/w))
        screen_width, screen_height = self.dimensions[0], self.dimensions[1]

        # Resize the image
        self.resized_image = pygame.transform.scale(image, (new_width, new_height))

        # Calculate the position to blit the image in the center
        self.x_pos, self.y_pos = (screen_width - new_width) // 2, HEIGHT // 3

    def render(self):
        """
        Renders the screen on the screen.
        """
        self.update()
        screen.fill(BACKGROUND)

        # Image
        self.setImage(self.image)
        screen.blit(self.resized_image, (self.x_pos, self.y_pos))
        
        # Text
        self.TextLabelScore, self.TextRectScore = self.render_text(str(self.question), 30, (WIDTH // 2, HEIGHT // 4))
        screen.blit(self.TextLabelScore, self.TextRectScore)

        # Countdown
        self.TextLabelScore, self.TextRectScore = self.render_text(f"Time: {self.count//50 + 1}", 20, (WIDTH - 50 , 30))
        screen.blit(self.TextLabelScore, self.TextRectScore)

        # Score
        self.TextLabelScore, self.TextRectScore = self.render_text(f"Score: {self.score}", 20, (50 , 30))
        screen.blit(self.TextLabelScore, self.TextRectScore)

        # Update the display
        pygame.display.update()

class Result:
    """
    Class for displaying the result screen.
    """
    def __init__(self, WIDTH, HEIGHT, BACKGROUND):
        """
        Initializes the result screen.
        """
        self.font = pygame.font.Font('freesansbold.ttf', 80)
        self.dimensions = (WIDTH, HEIGHT)
        self.BACKGROUND = BACKGROUND
        self.TextLabel, self.TextRect = self.render_text(f"You scored X", 100, (self.dimensions[0] // 2, self.dimensions[1] // 2))

    def render_text(self, text, size, center):
        """
        Renders text using the specified font size and position.
        """
        font = pygame.font.Font('freesansbold.ttf', size)
        text_surface = font.render(str(text), True, (0, 0, 0), self.BACKGROUND)
        text_rect = text_surface.get_rect(center=center)
        return text_surface, text_rect

    def update_result(self, score):
        """
        Update the result label based on scores.
        """
        self.TextLabel, self.TextRect = self.render_text(f"You scored {score}", 100, (self.dimensions[0] // 2, self.dimensions[1] // 2))

    def render(self):
        """
        Renders the winner screen on the screen.
        """
        screen.blit(self.TextLabel, self.TextRect)

class Winner:
    """
    Class for displaying the winner screen.
    """
    def __init__(self, WIDTH, HEIGHT, BACKGROUND):
        """
        Initializes the winner screen.
        """
        self.font = pygame.font.Font('freesansbold.ttf', 80)
        self.label = "Player X wins!"
        self.dimensions = (WIDTH, HEIGHT)
        self.BACKGROUND = BACKGROUND
        self.TextLabel, self.TextRect = self.render_text(self.label, 100, (self.dimensions[0] // 2, self.dimensions[1] // 2))

    def render_text(self, text, size, center):
        """
        Renders text using the specified font size and position.
        """
        font = pygame.font.Font('freesansbold.ttf', size)
        text_surface = font.render(str(text), True, (0, 0, 0), self.BACKGROUND)
        text_rect = text_surface.get_rect(center=center)
        return text_surface, text_rect

    def determine_winner_label(self, player1_score, player2_score):
        """
        Determines the winner label based on scores.
        """
        if player1_score > player2_score:
            self.label =  "Player 1 wins!"
        elif player1_score < player2_score:
            self.label =  "Player 2 wins!"
        else:
            self.label =  "Draw"

    def render(self):
        """
        Renders the winner screen on the screen.
        """
        self.TextLabel, self.TextRect = self.render_text(self.label, 100, (self.dimensions[0] // 2, self.dimensions[1] // 2))
        screen.blit(self.TextLabel, self.TextRect)
        
def handle_events():
    global Run, state, player_turn, user_text, score, player1_score, player2_score, question, question_bank
    for event in pygame.event.get():
        if state == 1:  # SCOREBOARD
            # Handle events for state 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    Run = False
                else:
                    state = 2
                    score = 0
        elif state == 2:  # READY
            # Handle events for state 2
            pass
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    Run = False
        elif state == 3:
            pass   
        elif state == 4:  # GAME
            # Handle events for state 4
            pass
        elif state == 5:  # RESULT
            # Handle events for state 5
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    Run = False
                else:
                    if player_turn == 1:
                        state = 1
                        player_turn = 2
                        user_text = ""
                    else:
                        state = 6
            question = ''
        elif state == 6:  # WINNER
            # Handle events for state 6
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    Run = False

def buffer(screen, state, wait_time=1):
    if screen.count <= 0:
        if state == 2:
            state = 4
        else:
            state += 1
        screen.count = 3        
    else:
        screen.render()
        sleep(wait_time)
    return screen, state
    
def update_state():
    global state, BACKGROUND, score, user_text, player1_score, player2_score
    load_player_turn()
    if state == 1:
        scoreboardScreen.update(player1_score, player2_score)
        scoreboardScreen.render()
    elif state == 2:
        _ , state = buffer(readyScreen, state)
    elif state == 4:
        gameScreen.run() # .update(user_text=user_text, question=question['question'])
        if gameScreen.gameover == True:
            state = 5
            score = gameScreen.score
            player1_score, player2_score = update_score(player1_score, player2_score, player_turn, score)
            gameScreen.restart()
    elif state == 5: 
        resultScreen.update_result(score)
        resultScreen.render()
    elif state == 6:
        winnerScreen.determine_winner_label(player1_score, player2_score)
        winnerScreen.render()

def load_player_turn():
    offset = 30
    
    player_color = {
        1:  COLOR["RED"],
        2:  COLOR["GREEN"],
        3:  COLOR["BLUE"]
    }
    TextLabel = font_list[20].render(str(f"P{player_turn}"), True, player_color[player_turn], BACKGROUND)
    TextRect = TextLabel.get_rect(center=(WIDTH-offset, offset))
    screen.blit(TextLabel, TextRect)

def load_contants():
    # Constants
    global WIDTH, HEIGHT, COLOR, BACKGROUND, MAX_LENGTH, font_list
    WIDTH = 800
    HEIGHT = 600
    COLOR = {
        "WHITE": (255, 255, 255),
        "RED":  (255, 0 , 0),
        "GREEN": (0, 255, 0),
        "BLUE": (0, 0, 255)
    }
    BACKGROUND = COLOR["WHITE"] # WHITE
    MAX_LENGTH = 10
    # Load fonts
    font_list = {}
    for i in range(20,101):
        font_list[i] = pygame.font.Font('freesansbold.ttf', i)
    
def load_config(file_path):
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config

def load_question(file_path):
    with open(file_path, 'r') as file:
        question = json.load(file)
    return question

def update_score(player1_score, player2_score, player_turn, score=0):
    if player_turn == 1:
        return player1_score + score, player2_score
    elif player_turn == 2:
        return player1_score, player2_score + score

def main():
    
    global screen, state, Run, player1_score, player2_score, score, player_turn
    global scoreboardScreen, readyScreen, gameScreen, resultScreen, winnerScreen
    global question_bank, config, question, user_text

    # Initialize Pygame
    pygame.init()

    # Load 
    config = load_contants()
    question_bank = load_question('question.json')
    question, user_text = '', '' 
    
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Initialize game variables
    Run, state = True, 1
    player1_score, player2_score, player_turn = 0, 0, 1

    # Load Screens
    scoreboardScreen, readyScreen = Scoreboard(WIDTH, HEIGHT, BACKGROUND), Ready(WIDTH, HEIGHT, BACKGROUND)
    gameScreen = Game(WIDTH, HEIGHT, BACKGROUND, screen, question_bank)
    resultScreen, winnerScreen = Result(WIDTH, HEIGHT, BACKGROUND), Winner(WIDTH, HEIGHT, BACKGROUND)

    while Run:
        screen.fill(BACKGROUND)

        handle_events()
        update_state()
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()