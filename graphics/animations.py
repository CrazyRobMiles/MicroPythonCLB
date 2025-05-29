from graphics.sprite import Sprite
import random

def anim_wandering_sprites(frame, no_of_sprites=30):

    frame.background_manager.start_transitions(((255,0,0),(0,255,0),(0,0,255),(0,0,0),(255,255,255)),100)

    frame.clear_sprites()

    for i in range (no_of_sprites):
        sprite = Sprite(frame)
        sprite.x = random.randint(0, frame.width)
        sprite.y = random.randint(0, frame.height)
        sprite.setColour((random.randint(0,255),random.randint(0,255),random.randint(0,255)))
        sprite.brightness = 0.3
        sprite.opacity = 0.1
        sprite.enabled = True
        sprite.startWrap(random.uniform(-0.2,0.2), random.uniform(-0.2,0.2))
        frame.add_sprite(sprite)
