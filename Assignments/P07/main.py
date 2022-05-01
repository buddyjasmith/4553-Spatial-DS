'''
Name:               Buddy Smith
Assignment:         P07
Description:        Create a screen object filled with circular blips,
                    have a rectangle move through the screen and detect
                    collisions, when collisions are detected, blips turn
                    blue and grow larger in size.
Controls:           ASWD:
                    A: left -> 50
                    S: down -> 50
                    D: right -> 50
                    W: up -> 50
                    P: Pause -> press p again to unpause

'''

import pygame, sys, random






def start_game():
    window_size = (500, 500)
    # initialize pygame application.
    pygame.init()
    # create the pygame surface object
    screen = pygame.display.set_mode(window_size)
    # now we need to set a title to display at the top of the screen
    pygame.display.set_caption('Pygame')

    # define points
    rect_x = 0  # x
    rect_y = 0  # y
    # define size of rectangle
    rect_width = 100
    rect_height = 100
    # create rectangle object
    rectangle = pygame.Rect(rect_x, rect_y, rect_height, rect_width)


    list_of_points = []

    points = 300
    for i in range(points):
        temp_x = random.randint(0, 500)
        temp_y = random.randint(0, 500)
        # inset random point in list of points
        list_of_points.append((temp_x, temp_y))
    state = 'RUNNING'
    pause = False
    pause_text = pygame.font.SysFont('Calibre', 32).render('Pause', True,
                                                            pygame.color.Color(
                                                                'White'))
    while True:
        # set background color
        screen.fill(pygame.Color('black'))
        pygame.draw.rect(screen, pygame.Color('green'), rectangle, 2)
        hor_move_point = 1
        ver_move_point = 0
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p and state == 'RUNNING':
                    # pause if p is pressed
                    state = "PAUSED"
                    pause = True
                    print('Pause is being pressed')
                elif event.key == pygame.K_p and state == 'PAUSED':
                    # if game is paused and p is pressed, unpause the game
                    state = 'RUNNING'
                    pause = False
                    print('Continue is being pressed')
                elif event.key == pygame.K_d:
                    # move to right
                    hor_move_point = 50
                elif event.key == pygame.K_a:
                    # move to left
                    hor_move_point = -50
                elif event.key == pygame.K_s:
                    # move down
                    ver_move_point = 50
                elif event.key == pygame.K_w:
                    # move up
                    ver_move_point = -50



            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
        if state == 'RUNNING':
            point_radius = 1
            collision_point_radius=6
            for point in list_of_points:

                if rectangle.collidepoint(point):
                    pygame.draw.circle(screen,
                                       pygame.Color('blue'),
                                       point,
                                       collision_point_radius,
                                       0)
                else:
                    point_color = pygame.Color(random.randint(0, 255),
                                               random.randint(0, 255),
                                               random.randint(0, 255))
                    pygame.draw.circle(screen,
                                       point_color,
                                       point,
                                       point_radius,
                                       0)
            rectangle.move_ip(hor_move_point, ver_move_point)
            if rectangle.right > window_size[0]:
                rectangle.move_ip(-window_size[0], 100)
            if rectangle.bottom > window_size[1]:
                rectangle.move_ip(-window_size[0], -window_size[1])
            # pygame.display.update()
            pygame.display.flip()
            pygame.time.delay(30)


        elif state == 'PAUSE':
            screen.blit(pause_text, (100, 100))

if __name__ == '__main__':
    start_game()