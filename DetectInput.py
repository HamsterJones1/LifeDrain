import pygame
from Globals import *
from Text import Text
from Button import Button


def DetectInput(instructionText="enter text:", length=100, position=(50, 125), size=(300, 50),
                allowLetters=True, allowUppercase=False, allowNumbers=True, allowOthers=True):
    textInput = ""
    instructions = Text(instructionText, (position[0], position[1] - (4 * size[1] / 5)), int(2 * size[1] / 3), white)
    display = pygame.Surface(Globs.VIEW_SIZE)
    surface = pygame.display.get_surface()
    displayText = Button(position, size)
    displayText.setColor(lightGrey, black, lightGrey, black)
    displayText.text.canChangeColor = False

    while True:
        event = pygame.event.poll()
        keys = pygame.key.get_pressed()

        if event.type == pygame.QUIT:
            Globs.RUNNING = False
            break
        elif event.type == pygame.KEYDOWN:
            # Escape
            if event.key == pygame.K_ESCAPE:
                textInput = ""
                break
            # Enter
            if event.key == pygame.K_RETURN:
                break
            # Backspace
            elif event.key == pygame.K_BACKSPACE:
                textInput = textInput[:-1]
            # Delete
            elif event.key == pygame.K_DELETE:
                textInput = ""
            if len(textInput) < length:
                # Space
                if event.key == pygame.K_SPACE:
                    textInput += " "
                # Letters
                elif allowLetters and pygame.K_a <= event.key <= pygame.K_z:
                    value = event.key
                    if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and allowUppercase:
                        value -= 32
                    textInput += str(pygame.key.name(value))
                # Numbers
                elif allowNumbers and pygame.K_0 <= event.key <= pygame.K_9:
                    textInput += str(pygame.key.name(event.key))
                # Others
                elif allowOthers:
                    if (33 <= event.key <= 47) or (58 <= event.key <= 64) or\
                            (91 <= event.key <= 96) or (123 <= event.key <= 126):
                        textInput += str(pygame.key.name(event.key))

        # Render
        instructions.render(display)
        displayText.updateText(textInput)
        displayText.render(display)
        setDisplay = pygame.transform.scale(display, Globs.DISPLAY_SIZE)
        surface.blit(setDisplay, Globs.DISPLAY_OFFSET)
        pygame.display.flip()

    # Break
    return textInput
