import pygame

pygame.mixer.init()  # Initialize the mixer
pygame.mixer.music.load(r'C:\Users\ASUS GAMING\Music\Slack - Yoink.mp3')  # Replace with your actual audio file path
pygame.mixer.music.play()  # Play the audio
pygame.time.wait(5000)  # Wait for 5 seconds
pygame.mixer.music.stop()  # Stop the audio