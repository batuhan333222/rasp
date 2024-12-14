from picamera2 import Picamera2
import pygame
import time
import os
import numpy as np

# Konfigürasyon Sabitleri
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480
CAM_FPS_LIST = [10, 30, 60, 90]
CAM_WIDTH = 261  # 300
CAM_HEIGHT = 348  # 400
CAM_ROTATION = 90
CAM_HORIZONTAL_OFFSET = 18
POWER_DOWN_BUTTON_DUR = 5  # saniye

# Başlangıç Değerleri
cam_fps_id = 1
green = (0, 255, 0)
black = (0, 0, 0)
pygame.init()
font = pygame.font.Font(None, 24)
size = width, height = 800, 480
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
pygame.mouse.set_visible(False)
pygame.display.update()

# FPS metnini güncelleyen fonksiyon
def update_fps_text():
    fps_text = font.render(f"{CAM_FPS_LIST[cam_fps_id]} fps", True, green, black)
    fps_text_rect = fps_text.get_rect()
    fps_text_rect.center = (CAM_HORIZONTAL_OFFSET - (CAM_WIDTH / 2), (SCREEN_HEIGHT + CAM_HEIGHT) / 2 + 7)
    screen.blit(fps_text, fps_text_rect)
    fps_text_rect.center = (SCREEN_WIDTH - (CAM_HORIZONTAL_OFFSET + (CAM_WIDTH / 2)), (SCREEN_HEIGHT + CAM_HEIGHT) / 2 + 7)
    screen.blit(fps_text, fps_text_rect)
    pygame.display.flip()

# Picamera2 başlatma
picam2 = Picamera2()
config = picam2.create_preview_configuration()
camera_config = picam2.create_still_configuration(main={"size": (CAM_WIDTH, CAM_HEIGHT)}, display="rgb")
picam2.configure(camera_config)
picam2.start()
picam2.set_controls({'Frame Rate': CAM_FPS_LIST[cam_fps_id]})
picam2.set_controls({'Rotation': CAM_ROTATION})

# Ana döngü
running = True
while running:
    # Kameradan görüntü al
    frame = picam2.capture_array("main")
    frame = np.rot90(np.flip(frame, axis=2))  # Rotasyon ve flip
    camera_surface = pygame.surfarray.make_surface(frame)
    
    # Görüntüyü ekrana iki kere yerleştir (sol ve sağ taraf)
    screen.blit(camera_surface, (CAM_HORIZONTAL_OFFSET, (SCREEN_HEIGHT - CAM_HEIGHT) // 2))
    screen.blit(camera_surface, (SCREEN_WIDTH - CAM_HORIZONTAL_OFFSET - CAM_WIDTH, (SCREEN_HEIGHT - CAM_HEIGHT) // 2))

    # FPS metnini güncelle
    update_fps_text()

    pygame.display.update()

    # Çıkış olaylarını kontrol et
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # FPS'yi kontrol et
    time.sleep(1 / CAM_FPS_LIST[cam_fps_id])  # FPS'ye göre bekleme süresi

pygame.quit()
