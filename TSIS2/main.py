import pygame
from datetime import datetime
import os

def flood_fill(surface, pos, fill_color):
    """
    Standard Stack-based Flood-fill algorithm.
    Uses get_at and set_at to manipulate pixels directly.
    """
    target_color = surface.get_at(pos)
    
    # If the clicked color is the same as the fill color, stop to avoid infinite loop
    if target_color == surface.map_rgb(fill_color):
        return

    stack = [pos]
    width, height = surface.get_size()
    
    # Map color to Pygame internal format for faster comparison
    fill_mapped = surface.map_rgb(fill_color)

    while stack:
        x, y = stack.pop()
        
        # Boundary check and color match check
        if 0 <= x < width and 0 <= y < height:
            if surface.get_at((x, y)) == target_color:
                surface.set_at((x, y), fill_mapped)
                # Add 4-directional neighbors to the stack
                stack.append((x + 1, y))
                stack.append((x - 1, y))
                stack.append((x, y + 1))
                stack.append((x, y - 1))

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    
    # 'canvas' is the persistent drawing surface. 
    # 'screen' is used for temporary previews (UI layer).
    canvas = pygame.Surface((800, 600))
    canvas.fill((0, 0, 0))
    clock = pygame.time.Clock()
    
    # Font setup for the Text Tool
    font = pygame.font.SysFont(None, 36)
    
    radius = 5          # Brush thickness
    color = (0, 0, 255) # Current drawing color
    mode = 'pen'        # Current tool mode
    last_pos, start_pos = None, None
    drawing = False
    
    # Text tool state variables
    typing = False
    text_input = ""
    text_pos = None

    print("=== CONTROLS ===")
    print("Colors: R, G, B, Y, W")
    print("Brush size: 1, 2, 3")
    print("Tools: P(Pen), L(Line), F(Fill), T(Text), E(Eraser)")
    print("Shapes: S(Rect), C(Circle), 4(Square), 5(Right Tri), 6(Eq Tri), 7(Rhombus)")
    print("Save: Ctrl + S")
    print("================")

    while True:
        pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
            # --- KEYBOARD EVENT HANDLING ---
            if event.type == pygame.KEYDOWN:
                # Logic for typing when Text Tool is active
                if typing:
                    if event.key == pygame.K_RETURN:
                        # "Bake" the text onto the canvas surface
                        text_surface = font.render(text_input, True, color)
                        canvas.blit(text_surface, text_pos)
                        typing = False
                        text_input = ""
                    elif event.key == pygame.K_ESCAPE:
                        # Cancel text entry
                        typing = False
                        text_input = ""
                    elif event.key == pygame.K_BACKSPACE:
                        text_input = text_input[:-1]
                    else:
                        text_input += event.unicode
                
                # Logic for Hotkeys and Tool Switching
                else:
                    mods = pygame.key.get_mods()
                    # SAVE functionality with Timestamp (Ctrl+S)
                    if event.key == pygame.K_s and (mods & pygame.KMOD_CTRL):
                        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                        filename = f"canvas_{timestamp}.png"
                        pygame.image.save(canvas, filename)
                        print(f"Canvas saved as: {filename}")
                        continue 

                    # Color Switching
                    if event.key == pygame.K_r: color = (255, 0, 0)
                    elif event.key == pygame.K_g: color = (0, 255, 0)
                    elif event.key == pygame.K_b: color = (0, 0, 255)
                    elif event.key == pygame.K_y: color = (255, 255, 0)
                    elif event.key == pygame.K_w: color = (255, 255, 255)
                    
                    # Brush Size Selection
                    elif event.key == pygame.K_1: radius = 2
                    elif event.key == pygame.K_2: radius = 5
                    elif event.key == pygame.K_3: radius = 10
                    
                    # Mode Selection
                    elif event.key == pygame.K_p: mode = 'pen'
                    elif event.key == pygame.K_l: mode = 'line'
                    elif event.key == pygame.K_f: mode = 'fill'
                    elif event.key == pygame.K_t: mode = 'text'
                    elif event.key == pygame.K_s: mode = 'rect'
                    elif event.key == pygame.K_c: mode = 'circle'
                    elif event.key == pygame.K_e: mode = 'eraser'
                    elif event.key == pygame.K_4: mode = 'square'
                    elif event.key == pygame.K_5: mode = 'right_tri'
                    elif event.key == pygame.K_6: mode = 'eq_tri'
                    elif event.key == pygame.K_7: mode = 'rhombus'

            # --- MOUSE BUTTON PRESS ---
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left Click
                    if mode == 'fill':
                        flood_fill(canvas, event.pos, color)
                    elif mode == 'text':
                        # Finalize previous text if user clicks elsewhere while typing
                        if typing:
                            text_surface = font.render(text_input, True, color)
                            canvas.blit(text_surface, text_pos)
                        typing = True
                        text_pos = event.pos
                        text_input = ""
                    else:
                        # For shapes/lines, mark the starting point
                        drawing = True
                        start_pos = event.pos 
                        
                # Mouse Wheel for dynamic brush resizing
                elif event.button == 4: radius = min(100, radius + 2)
                elif event.button == 5: radius = max(2, radius - 2)
            
            # --- MOUSE BUTTON RELEASE ---
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and drawing:
                    drawing = False
                    # On release, draw the final shape onto the permanent canvas
                    if mode == 'rect': draw_rect(canvas, start_pos, event.pos, radius, color)
                    elif mode == 'circle': draw_circle(canvas, start_pos, event.pos, radius, color)
                    elif mode == 'square': draw_square(canvas, start_pos, event.pos, radius, color)
                    elif mode == 'right_tri': draw_right_triangle(canvas, start_pos, event.pos, radius, color)
                    elif mode == 'eq_tri': draw_equilateral_triangle(canvas, start_pos, event.pos, radius, color)
                    elif mode == 'rhombus': draw_rhombus(canvas, start_pos, event.pos, radius, color)
                    elif mode == 'line': pygame.draw.line(canvas, color, start_pos, event.pos, radius)
                    
                    start_pos = None
                last_pos = None

        # --- CONTINUOUS DRAWING (Pencil / Eraser) ---
        if drawing:
            # Pencil draws directly on the canvas as the mouse moves
            if mode == 'pen' and last_pos is not None:
                draw_line(canvas, last_pos, pos, radius, color)
            elif mode == 'eraser' and last_pos is not None:
                draw_line(canvas, last_pos, pos, radius, (0, 0, 0)) 
            last_pos = pos

        # --- RENDERING PIPELINE ---
        
        # 1. First, show the permanent drawing surface
        screen.blit(canvas, (0, 0))
        
        # 2. Draw the PREVIEW on top (only on 'screen', not 'canvas')
        # This allows the user to see the shape stretch before confirming
        if drawing and start_pos is not None:
            if mode == 'rect': draw_rect(screen, start_pos, pos, radius, color)
            elif mode == 'circle': draw_circle(screen, start_pos, pos, radius, color)
            elif mode == 'square': draw_square(screen, start_pos, pos, radius, color)
            elif mode == 'right_tri': draw_right_triangle(screen, start_pos, pos, radius, color)
            elif mode == 'eq_tri': draw_equilateral_triangle(screen, start_pos, pos, radius, color)
            elif mode == 'rhombus': draw_rhombus(screen, start_pos, pos, radius, color)
            elif mode == 'line': pygame.draw.line(screen, color, start_pos, pos, radius)

        # 3. Render live text input with a blinking cursor
        if typing and text_pos:
            text_surface = font.render(text_input, True, color)
            screen.blit(text_surface, text_pos)
            # Simple cursor blink logic using ticks
            if pygame.time.get_ticks() % 1000 < 500:
                cursor_x = text_pos[0] + text_surface.get_width()
                pygame.draw.line(screen, color, (cursor_x, text_pos[1]), (cursor_x, text_pos[1] + font.get_height()), 2)

        # 4. Draw brush size indicator near the cursor
        if mode not in ['text', 'fill']:
            pygame.draw.circle(screen, color if mode != 'eraser' else (255, 255, 255), pos, radius, 1)

        pygame.display.flip()
        clock.tick(120)

# --- SHAPE DRAWING FUNCTIONS ---

def draw_line(surf, start, end, width, color):
    """
    Connects two points using tiny circles to ensure a smooth line (interpolation).
    Essential for 'Pencil' tool to avoid dotted lines when moving fast.
    """
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    distance = max(abs(dx), abs(dy))
    
    if distance == 0:
        pygame.draw.circle(surf, color, start, width)
        return
        
    for i in range(distance):
        x = int(start[0] + float(i) / distance * dx)
        y = int(start[1] + float(i) / distance * dy)
        pygame.draw.circle(surf, color, (x, y), width)

def draw_rect(surf, start, end, width, color):
    """Draws a standard rectangle based on mouse drag."""
    x1, y1 = start
    x2, y2 = end
    pygame.draw.rect(surf, color, (min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2)), width)

def draw_circle(surf, start, end, width, color):
    """Draws a circle where the drag distance defines the radius."""
    r = int(((start[0] - end[0])**2 + (start[1] - end[1])**2)**0.5)
    if r > width: pygame.draw.circle(surf, color, start, r, width)

def draw_square(surf, start, end, width, color):
    """Forces the shape to have equal width and height."""
    side_length = max(abs(start[0] - end[0]), abs(start[1] - end[1]))
    rect_x = start[0] if end[0] > start[0] else start[0] - side_length
    rect_y = start[1] if end[1] > start[1] else start[1] - side_length
    if side_length > 0:
        pygame.draw.rect(surf, color, (rect_x, rect_y, side_length, side_length), width)

def draw_right_triangle(surf, start, end, width, color):
    """Draws a right-angled triangle using polygon."""
    points = [(start[0], start[1]), (start[0], end[1]), (end[0], end[1])]
    if len(set(points)) > 2:
        pygame.draw.polygon(surf, color, points, width)

def draw_equilateral_triangle(surf, start, end, width, color):
    """Draws a triangle with a centered top vertex."""
    mid_x = (start[0] + end[0]) // 2
    points = [(mid_x, start[1]), (start[0], end[1]), (end[0], end[1])]
    if len(set(points)) > 2:
        pygame.draw.polygon(surf, color, points, width)

def draw_rhombus(surf, start, end, width, color):
    """Calculates midpoints to draw a diamond shape."""
    mid_x = (start[0] + end[0]) // 2
    mid_y = (start[1] + end[1]) // 2
    points = [(mid_x, start[1]), (end[0], mid_y), (mid_x, end[1]), (start[0], mid_y)]
    if len(set(points)) > 2:
        pygame.draw.polygon(surf, color, points, width)

if __name__ == "__main__":
    main()