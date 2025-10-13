"This program takes in text from a GUI and classifies it as positive, neutral or negative"
import os
import sys
import pygame
import google.generativeai as genai

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel(
    'gemini-2.5-flash',
    system_instruction=
    """
    You are a bot that classifies text based on it's sentiment, return only
    positive, negative or neutral.

    e.g. 
    >That movie was so bad
    Return: Negative

    >I love ice-cream
    Return: Positive

    >The movie was about movies
    Return: Neutral
    """
)

# --- Initialization ---
pygame.init()

# --- Constants ---
SCALE_FACTOR = 4
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 700
SCREEN_WIDTH = WINDOW_WIDTH * SCALE_FACTOR
SCREEN_HEIGHT = WINDOW_HEIGHT * SCALE_FACTOR

BG_COLOR = (240, 240, 240)
INPUT_BOX_COLOR_INACTIVE = (200, 200, 200)
INPUT_BOX_COLOR_ACTIVE = (150, 150, 150)
TEXT_COLOR = (0, 0, 0)
BUTTON_COLOR = (100, 180, 100)
BUTTON_TEXT_COLOR = (255, 255, 255)

# --- Screen and Font Setup ---
# The actual window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
# The surface we draw everything to at 4x resolution
display_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Pygame Text Submitter")
font = pygame.font.Font(None, 32 * SCALE_FACTOR)
small_font = pygame.font.Font(None, 28 * SCALE_FACTOR)

# --- State Variables ---
input_text = ""
submitted_text = ""
input_box = pygame.Rect(50 * SCALE_FACTOR, 80 * SCALE_FACTOR, (WINDOW_WIDTH - 100) * SCALE_FACTOR, 40 * SCALE_FACTOR)
submit_button = pygame.Rect(50 * SCALE_FACTOR, 140 * SCALE_FACTOR, 140 * SCALE_FACTOR, 40 * SCALE_FACTOR)
input_active = False

def process_text(text_to_process):
    prompt = text_to_process
    response = model.generate_content(prompt)

    return response.text

def handle_submit():
    """Handles the text submission logic."""
    global input_text, submitted_text
    if input_text:
        processed = process_text(input_text)
        submitted_text = processed
        input_text = ""

# --- Main Game Loop ---
running = True
while running:
    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # Mouse click handling
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Scale mouse position to match the larger surface
            scaled_mouse_pos = (event.pos[0] * SCALE_FACTOR, event.pos[1] * SCALE_FACTOR)

            # Check if user clicked on the input box
            if input_box.collidepoint(scaled_mouse_pos):
                input_active = not input_active
            else:
                input_active = False
            
            # Check if user clicked on the submit button
            if submit_button.collidepoint(scaled_mouse_pos):
                handle_submit()

        # Keyboard input handling
        if event.type == pygame.KEYDOWN:
            if input_active:
                if event.key == pygame.K_RETURN: # Enter key submits
                    handle_submit()
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    # Append typed character to the input text
                    input_text += event.unicode

    # --- Drawing and Rendering ---
    # Draw everything on the high-resolution surface first
    display_surface.fill(BG_COLOR)
    
    # Draw a title for the input box
    title_surface = small_font.render("Enter Text Below:", True, TEXT_COLOR)
    display_surface.blit(title_surface, (50 * SCALE_FACTOR, 40 * SCALE_FACTOR))

    # Draw the input box
    box_color = INPUT_BOX_COLOR_ACTIVE if input_active else INPUT_BOX_COLOR_INACTIVE
    pygame.draw.rect(display_surface, box_color, input_box, 2 * SCALE_FACTOR, border_radius=5 * SCALE_FACTOR)
    
    # Render and blit the input text
    text_surface = font.render(input_text, True, TEXT_COLOR)
    display_surface.blit(text_surface, (input_box.x + 10 * SCALE_FACTOR, input_box.y + 10 * SCALE_FACTOR))
    # Keep the input box width from changing
    input_box.w = max((WINDOW_WIDTH - 100) * SCALE_FACTOR, text_surface.get_width() + 20 * SCALE_FACTOR)

    # Draw the submit button
    pygame.draw.rect(display_surface, BUTTON_COLOR, submit_button, border_radius=5 * SCALE_FACTOR)
    submit_text_surface = font.render("Submit", True, BUTTON_TEXT_COLOR)
    # Center text on the button, ensuring integer coordinates
    display_surface.blit(submit_text_surface, 
                (submit_button.x + (submit_button.w - submit_text_surface.get_width()) // 2,
                 submit_button.y + (submit_button.h - submit_text_surface.get_height()) // 2))

    # Draw the submitted texts
    y_offset = 210 * SCALE_FACTOR
    submitted_surface = small_font.render(submitted_text, True, TEXT_COLOR)
    display_surface.blit(submitted_surface, (50 * SCALE_FACTOR, y_offset))

    # --- Scale down and update the display ---
    # Scale the high-res surface down to the window size. 'smoothscale' provides anti-aliasing.
    scaled_surface = pygame.transform.smoothscale(display_surface, (WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(scaled_surface, (0, 0))
    pygame.display.flip()

# --- Clean Up ---
pygame.quit()
sys.exit()


