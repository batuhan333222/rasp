from picamera2 import Picamera2
import pygame
import numpy as np
import time

# Ekran ve kamera ayarları
SCREEN_WIDTH = 800  # Pygame ekran genişliği
SCREEN_HEIGHT = 480  # Pygame ekran yüksekliği
CAM_WIDTH = 320  # Kamera görüntüsü genişliği
CAM_HEIGHT = 240  # Kamera görüntüsü yüksekliği
CAM_FPS = 30  # Kamera FPS
SPACING = 20  # Görüntüler arasındaki yatay boşluk
MARGIN_TOP = 50  # Üstten boşluk

# Renk tanımları
green = (0, 255, 0)
black = (0, 0, 0)

# Pygame başlatma
pygame.init()
font = pygame.font.Font(None, 24)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.mouse.set_visible(False)
screen.fill(black)
pygame.display.update()

# FPS metni güncelleme (görüntülerin altına ortalanmış şekilde yerleştirme)
def draw_fps_text():
    fps_text = font.render(str(CAM_FPS) + "fps", True, green)

    # Sol kamera görüntüsü için FPS (sağa kaydırılmış)
    left_fps_x = (SCREEN_WIDTH // 2) - CAM_WIDTH - (SPACING // 2) + (CAM_WIDTH // 2) - (fps_text.get_width() // 2) + 60  # Sağa kaydırma
    left_fps_y = MARGIN_TOP + CAM_HEIGHT + 10  # Görüntünün altında biraz boşluk bırak
    screen.blit(fps_text, (left_fps_x, left_fps_y))
    
    # Sağ kamera görüntüsü için FPS (sağa kaydırılmış)
    right_fps_x = (SCREEN_WIDTH // 2) + (SPACING // 2) + (CAM_WIDTH // 2) - (fps_text.get_width() // 2) + 60  # Sağa kaydırma
    right_fps_y = MARGIN_TOP + CAM_HEIGHT + 10  # Görüntünün altında biraz boşluk bırak
    screen.blit(fps_text, (right_fps_x, right_fps_y))

# Picamera2 başlatma
picam2 = Picamera2()
camera_config = picam2.create_preview_configuration(main={"size": (CAM_WIDTH, CAM_HEIGHT)})
picam2.configure(camera_config)
picam2.start()

# Ana döngü
running = True
while running:
    # Kamera görüntüsünü yakala
    frame = picam2.capture_array("main")
    frame = np.rot90(np.flip(frame, axis=2))
    camera_surface = pygame.surfarray.make_surface(frame)

    # Sol görüntü
    left_x = (SCREEN_WIDTH // 2) - CAM_WIDTH - (SPACING // 2)
    left_y = MARGIN_TOP
    screen.blit(camera_surface, (left_x, left_y))

    # Sağ görüntü
    right_x = (SCREEN_WIDTH // 2) + (SPACING // 2)
    right_y = MARGIN_TOP
    screen.blit(camera_surface, (right_x, right_y))

    # FPS metinlerini güncelle
    draw_fps_text()
    pygame.display.update()

    # Çıkış kontrolü
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    time.sleep(1 / CAM_FPS)

pygame.quit()
