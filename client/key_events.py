# key_events.py

import pygame


def handle_key_press(event, app):
    """
    Аналог Processing keyPressed()
    """

    if event.key == pygame.K_SPACE:
        app.homography_matrix_calculated = False

    elif event.key == pygame.K_r:
        app.reset_data_objects()

    elif event.key == pygame.K_g:
        app.gesture_debug = not app.gesture_debug

    elif event.key == pygame.K_t:
        app.tag_debug = not app.tag_debug

    elif event.key == pygame.K_d:
        app.data_object_debug = not app.data_object_debug

    elif event.key == pygame.K_s:
        app.serial_debug = not app.serial_debug

    elif event.key == pygame.K_1:
        app.gesture_mode = 1

    elif event.key == pygame.K_2:
        app.gesture_mode = 2

    elif event.key == pygame.K_3:
        app.gesture_mode = 3
        
        