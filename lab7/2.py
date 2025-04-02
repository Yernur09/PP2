import pygame
import sys

pygame.init()

window = pygame.display.set_mode((600, 300))

Play = pygame.image.load('lab7/images/play.png').convert_alpha()
Stop = pygame.image.load('lab7/images/stop.png').convert_alpha()
Next = pygame.image.load('lab7/images/next.png').convert_alpha()
Last = pygame.image.load('lab7/images/prev.png').convert_alpha()

# Create button surface
Button = pygame.Surface((173, 173), pygame.SRCALPHA)

play_button_rect = pygame.Rect(300, 50, 173, 173)
next_button_rect = pygame.Rect(500, 50, 173, 173)
prev_button_rect = pygame.Rect(100, 50, 173, 173)

# Music event
SONG_END = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(SONG_END)


songs = ['C:/Users/ernur/OneDrive/Desktop/PP Labs/lab7/music/505.mp3', 'C:/Users/ernur/OneDrive/Desktop/PP Labs/lab7/music/for the first time.mp3']
currently_playing_song = 0  # Index of current song

# Load and play the first song
pygame.mixer.music.load(songs[currently_playing_song])
pygame.mixer.music.play()

playing = True  # Play state

def play_next_song():
    global currently_playing_song
    currently_playing_song = (currently_playing_song + 1) % len(songs)
    pygame.mixer.music.load(songs[currently_playing_song])
    pygame.mixer.music.play()

def play_last_song():
    global currently_playing_song
    currently_playing_song = (currently_playing_song - 1) % len(songs)
    pygame.mixer.music.load(songs[currently_playing_song])
    pygame.mixer.music.play()

while True:
    pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_button_rect.collidepoint(pos):  # Toggle play/pause
                playing = not playing
                if playing:
                    pygame.mixer.music.unpause()
                else:
                    pygame.mixer.music.pause()
            elif next_button_rect.collidepoint(pos):  # Play next song
                play_next_song()
                playing = True
            elif prev_button_rect.collidepoint(pos):  # Play previous song
                play_last_song()
                playing = True

        if event.type == SONG_END:  # Auto play next song when one finishes
            play_next_song()

    window.fill((255, 255, 255))  
    window.blit(Last, prev_button_rect.topleft)  # Previous button
    window.blit(Next, next_button_rect.topleft)  # Next button
    
    #Pause button
    Button.fill((0, 0, 0, 0))  # Clear the button surface
    if playing:
        Button.blit(Stop, (0, 0))
    else:
        Button.blit(Play, (0, 0))
    window.blit(Button, play_button_rect.topleft)
    pygame.display.flip()