import pygame

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((400, 200))
pygame.display.set_caption("VS Code Music Player")

playlist = [
    "music/track1.mp3", 
    "music/track2.mp3", 
    "music/track3.mp3", 
    "music/track4.mp3", 
    "music/track5.mp3", 
    "music/track6.mp3", 
    "music/track7.mp3"
]
current_track = 0

pygame.mixer.music.load(playlist[current_track])

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_p: 
                pygame.mixer.music.play() 
                
            elif event.key == pygame.K_s: 
                pygame.mixer.music.stop() 
                
            elif event.key == pygame.K_n: 
               
                current_track = (current_track + 1) % len(playlist)
                pygame.mixer.music.load(playlist[current_track])
                pygame.mixer.music.play()
                
            elif event.key == pygame.K_b:
                current_track = (current_track - 1) % len(playlist)
                pygame.mixer.music.load(playlist[current_track])
                pygame.mixer.music.play()
                
            elif event.key == pygame.K_q: 
                running = False

    
    screen.fill((0, 0, 0))
    pygame.display.flip()

pygame.quit()