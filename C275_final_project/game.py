import sys, pygame, time
import collision
from pygame.locals import *
from gui import GUI
from utilities import Timer

BG_IMG = pygame.image.load('assets/farback.gif')
RESOLUTION = BG_IMG.get_rect()
CLOCK = pygame.time.Clock()

main_gui = GUI(RESOLUTION, BG_IMG)

SPACE_STATION = main_gui.space_station
ENDGAME_TOKEN = None

ASTEROID_PERIOD = 0.75
ASTEROID_SPAWN_TIMER = Timer(ASTEROID_PERIOD, main_gui.asteroid_spawn)

ALIEN_SPAWN_PERIOD = 2.5
ALIEN_SPAWN_TIMER = Timer(ALIEN_SPAWN_PERIOD, main_gui.alien_spawn)

ALIEN_HOP_PERIOD = 0.8
ALIEN_HOP_TIMER = Timer(ALIEN_HOP_PERIOD, main_gui.alien_hop)

def get_user_input():
    '''
    Checks for user keyboard input.
    Allows for acceleration, braking, turning of ship and exit from game.
    '''
    # Get user input
    for event in pygame.event.get(): 
        if not hasattr(event, 'key'):continue 
        down = event.type == KEYDOWN
        key = event.key
        #key down or up?
        if (key == K_RIGHT or key == K_LEFT or  key == K_UP or\
                key == K_DOWN or key == K_SPACE or key == K_TAB):
            # Found a valid key input, pass to gui
            main_gui.p1_button(key, down)
        elif event.key == K_ESCAPE: sys.exit(0)

def check_for_endgame():
    '''
    When the space station is destroyed, particles are generated.
    The last of these particles is used as a token; when it is deactivated
    the game is finished and exits.
    '''
    global ENDGAME_TOKEN
    if not SPACE_STATION.alive():
        # Create particles when spacestation dies
        if ENDGAME_TOKEN is None:
            ENDGAME_TOKEN =\
                collision.generate_particles(
                main_gui.screen,
                SPACE_STATION,
                100,
                3,
                (124,55,0),
                health = 100)
    
    # The very last particle has finished its animation, exit game.
    if not ENDGAME_TOKEN is None and not ENDGAME_TOKEN.alive():
        sys.exit(0)

# Main game loop
while 1:

    check_for_endgame()
    get_user_input()

    # Periodically(timer preset) add aliens, asteroids, make aliens to move.
    ALIEN_SPAWN_TIMER.update(2) # Arg: how many possible aliens to add
    ASTEROID_SPAWN_TIMER.update()
    ALIEN_HOP_TIMER.update()
    
    # Update, delete offscreen and draw objects every frame
    main_gui.update()
    main_gui.offscreen()
    main_gui.draw()

    # Handles framerate. Note: game is framerate dependent
    current_tick = CLOCK.tick(40)


