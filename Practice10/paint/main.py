import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    
    # This surface will store our permanent drawing
    canvas = pygame.Surface((800, 600))
    canvas.fill((0, 0, 0))
    
    clock = pygame.time.Clock()
    
    # Initial settings
    radius = 15
    color = (0, 0, 255) # Start with Blue
    mode = 'pen' # Modes: 'pen', 'rect', 'circle', 'eraser'
    
    last_pos = None
    start_pos = None
    drawing = False

    print("Controls:")
    print("Colors: R - Red, G - Green, B - Blue, Y - Yellow, W - White")
    print("Tools: P - Pen, S - Square (Rect), C - Circle, E - Eraser")
    print("Radius: Mouse wheel or Left/Right click")

    while True:
        pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
            # Key controls for colors and tools
            if event.type == pygame.KEYDOWN:
                # Color Selection
                if event.key == pygame.K_r: color = (255, 0, 0)
                elif event.key == pygame.K_g: color = (0, 255, 0)
                elif event.key == pygame.K_b: color = (0, 0, 255)
                elif event.key == pygame.K_y: color = (255, 255, 0)
                elif event.key == pygame.K_w: color = (255, 255, 255)
                
                # Tool Selection
                elif event.key == pygame.K_p: mode = 'pen'
                elif event.key == pygame.K_s: mode = 'rect'
                elif event.key == pygame.K_c: mode = 'circle'
                elif event.key == pygame.K_e: mode = 'eraser'
                
                elif event.key == pygame.K_ESCAPE: return

            # Mouse Button Down
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left click
                    drawing = True
                    start_pos = event.pos # Store starting point for shapes
                elif event.button == 3: # Right click: grow radius
                    radius = min(200, radius + 2)
                elif event.button == 2: # Middle click: shrink radius
                    radius = max(1, radius - 2)
            
            # Mouse Button Up
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
                    # Finalize Rectangle or Circle on the canvas
                    if mode == 'rect':
                        draw_rect(canvas, start_pos, event.pos, radius, color)
                    elif mode == 'circle':
                        draw_circle(canvas, start_pos, event.pos, radius, color)
                    start_pos = None
                last_pos = None

        # --- Drawing Logic ---
        if drawing:
            if mode == 'pen':
                # Draw a continuous line for smooth painting
                if last_pos is not None:
                    draw_line(canvas, last_pos, pos, radius, color)
                last_pos = pos
            elif mode == 'eraser':
                if last_pos is not None:
                    draw_line(canvas, last_pos, pos, radius, (0, 0, 0)) # Erase with Black
                last_pos = pos

        # --- Screen Rendering ---
        # 1. Draw the persistent canvas
        screen.blit(canvas, (0, 0))
        
        # 2. Draw temporary preview for shapes while dragging
        if drawing and start_pos is not None:
            if mode == 'rect':
                draw_rect(screen, start_pos, pos, radius, color)
            elif mode == 'circle':
                draw_circle(screen, start_pos, pos, radius, color)

        # 3. Draw a small brush preview around the cursor
        pygame.draw.circle(screen, color if mode != 'eraser' else (255, 255, 255), pos, radius, 1)

        pygame.display.flip()
        clock.tick(60)

def draw_line(surf, start, end, width, color):
    """Draws a smooth line between two points using overlapping circles."""
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    distance = max(abs(dx), abs(dy))
    for i in range(distance):
        x = int(start[0] + float(i) / distance * dx)
        y = int(start[1] + float(i) / distance * dy)
        pygame.draw.circle(surf, color, (x, y), width)

def draw_rect(surf, start, end, width, color):
    """Draws a rectangle based on two corner points."""
    x1, y1 = start
    x2, y2 = end
    rect_x = min(x1, x2)
    rect_y = min(y1, y2)
    rect_w = abs(x1 - x2)
    rect_h = abs(y1 - y2)
    if rect_w > 0 and rect_h > 0:
        pygame.draw.rect(surf, color, (rect_x, rect_y, rect_w, rect_h), width)

def draw_circle(surf, start, end, width, color):
    """Draws a circle where start is center and distance to end is radius."""
    x1, y1 = start
    x2, y2 = end
    # Distance formula for radius
    r = int(((x1 - x2)**2 + (y1 - y2)**2)**0.5)
    if r > 0:
        pygame.draw.circle(surf, color, (x1, y1), r, width)

if __name__ == "__main__":
    main()