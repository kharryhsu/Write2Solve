from pathlib import Path
import pygame
import numpy as np
import time
from tensorflow.keras.models import load_model
from . import equation_generation

MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "digit_cnn.keras"

def predict_digit():
    image = pygame.surfarray.array3d(canvas)
    image = np.mean(image, axis=2)
    image = pygame.transform.scale(pygame.surfarray.make_surface(255 - image.T), (28, 28))
    image_array = pygame.surfarray.array3d(image).mean(axis=2) / 255.0
    image_array = image_array.reshape(1, 28, 28, 1)
    prediction = model.predict(image_array)
    
    return np.argmax(prediction)

model = load_model(MODEL_PATH)

WIDTH, HEIGHT = 800, 800

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

CANVAS_SIZE = 400
CANVAS_OFFSET = (WIDTH - CANVAS_SIZE) // 2

BORDER_COLOR = (200, 200, 200)

BUTTON_HEIGHT = 50
BUTTON_COLOR = (220, 220, 220)
BUTTON_HOVER = (180, 180, 180)

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.Font(None, 50)

pygame.display.set_caption("Write2Solve")

canvas = pygame.Surface((CANVAS_SIZE, CANVAS_SIZE))
canvas.fill(WHITE)

num1, num2, operator, solution = equation_generation.generate_equation()
running = True
drawing = False

drawing_result = '?'
result_color = BLACK
feedback_text = ''
showing_result = False
result_timer = 0

def draw_button(rect, text, hover=False):
    color = BUTTON_HOVER if hover else BUTTON_COLOR
    pygame.draw.rect(screen, color, rect)
    button_text = font.render(text, True, BLACK)
    screen.blit(button_text, (rect.x + (rect.width - button_text.get_width()) // 2, rect.y + (rect.height - button_text.get_height()) // 2))

clear_button_rect = pygame.Rect(CANVAS_OFFSET, CANVAS_OFFSET + CANVAS_SIZE + 10, CANVAS_SIZE // 2 - 5, BUTTON_HEIGHT)
submit_button_rect = pygame.Rect(CANVAS_OFFSET + CANVAS_SIZE // 2 + 5, CANVAS_OFFSET + CANVAS_SIZE + 10, CANVAS_SIZE // 2 - 5, BUTTON_HEIGHT)

while running:
    screen.fill(WHITE)
    pygame.draw.rect(screen, BORDER_COLOR, (CANVAS_OFFSET - 2, CANVAS_OFFSET - 2, CANVAS_SIZE + 4, CANVAS_SIZE + 4), 2)
    screen.blit(canvas, (CANVAS_OFFSET, CANVAS_OFFSET))
    
    equation_text = font.render(f'{num1} {operator} {num2} =', True, BLACK)
    screen.blit(equation_text, (WIDTH // 2 - equation_text.get_width() // 2, 20))
    
    result_text_surface = font.render(str(drawing_result), True, result_color)
    screen.blit(result_text_surface, (WIDTH // 2 + equation_text.get_width() // 2 + 5, 20))
    
    mouse_pos = pygame.mouse.get_pos()
    
    draw_button(clear_button_rect, "Clear", clear_button_rect.collidepoint(mouse_pos))
    draw_button(submit_button_rect, "Submit", submit_button_rect.collidepoint(mouse_pos))
    
    feedback_display  = font.render(feedback_text, True, result_color)
    screen.blit(feedback_display , (WIDTH // 2 - feedback_display .get_width() // 2, CANVAS_OFFSET + CANVAS_SIZE + 70))
    
    if showing_result:
        if time.time() - result_timer > 1:
            showing_result = False
            num1, num2, operator, solution = equation_generation.generate_equation()
            drawing_result = '?'
            feedback_text = ""
            result_color = BLACK
            canvas.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if clear_button_rect.collidepoint(event.pos):
                canvas.fill(WHITE)
                drawing_result = '?'
                feedback_text = ""
                result_color = BLACK
            elif submit_button_rect.collidepoint(event.pos):
                if not showing_result:
                    prediction = predict_digit()
                    drawing_result = prediction
                    if prediction == solution:
                        feedback_text = "Correct!"
                        result_color = GREEN
                        showing_result = True
                        result_timer = time.time()
                    else:
                        feedback_text = "Incorrect!"
                        result_color = RED
                    canvas.fill(WHITE)
            else:
                drawing = True
        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False
    
    if drawing:
        x, y = pygame.mouse.get_pos()
        if CANVAS_OFFSET <= x <= CANVAS_OFFSET + CANVAS_SIZE and CANVAS_OFFSET <= y <= CANVAS_OFFSET + CANVAS_SIZE:
            pygame.draw.circle(canvas, BLACK, (x - CANVAS_OFFSET, y - CANVAS_OFFSET), 8)
            
    pygame.display.flip()

pygame.quit()