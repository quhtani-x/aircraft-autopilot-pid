import math
import random
import sys
import pygame

# AIRCRAFT AUTOPILOT with an artificial horizon (attitude indicator).
# the plane gets knocked around by turbulence. a PID autopilot holds the target
# altitude and keeps the wings level, just like a real "altitude hold" mode.
# use UP/DOWN arrows to change the target altitude and watch it correct.

W, H = 880, 600
pygame.init()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("aircraft autopilot - altitude & attitude hold")
font = pygame.font.SysFont("consolas", 18)
clock = pygame.time.Clock()


class PID:
    def __init__(self, kp, ki, kd):
        self.kp, self.ki, self.kd = kp, ki, kd
        self.prev = 0
        self.integral = 0

    def step(self, err):
        self.integral = max(-100, min(100, self.integral + err))
        d = err - self.prev
        self.prev = err
        return self.kp * err + self.ki * self.integral + self.kd * d


# state: pitch (roll of the horizon), altitude, vertical speed
roll = 0.0          # bank angle in radians
altitude = 5000.0
vspeed = 0.0
target_alt = 5000.0

alt_pid = PID(0.02, 0.001, 0.05)
roll_pid = PID(2.0, 0.0, 0.5)

running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        target_alt += 8
    if keys[pygame.K_DOWN]:
        target_alt -= 8

    # turbulence keeps disturbing the plane
    roll += random.uniform(-0.02, 0.02)
    vspeed += random.uniform(-0.3, 0.3)

    # ---- autopilot ----
    # altitude hold: error in altitude -> desired climb/descent -> elevator
    alt_err = target_alt - altitude
    elevator = alt_pid.step(alt_err)
    vspeed += (elevator - vspeed) * 0.05
    altitude += vspeed * 0.1

    # wing leveler: drive roll back to 0
    aileron = roll_pid.step(-roll)
    roll += aileron * 0.01
    roll *= 0.98  # natural damping

    # ---- draw the artificial horizon ----
    screen.fill((10, 10, 16))
    cx, cy = W // 2, H // 2
    horizon = pygame.Surface((W, H))

    # sky and ground, rotated by the bank angle and shifted by pitch
    pitch_offset = max(-150, min(150, vspeed * 20))
    horizon.fill((90, 150, 220))  # sky
    pygame.draw.rect(horizon, (120, 85, 50), (0, H // 2 + int(pitch_offset), W, H))  # ground
    pygame.draw.line(horizon, (255, 255, 255), (0, H // 2 + int(pitch_offset)),
                     (W, H // 2 + int(pitch_offset)), 3)
    rotated = pygame.transform.rotate(horizon, math.degrees(roll))
    rect = rotated.get_rect(center=(cx, cy))
    # clip into a circular instrument
    screen.blit(rotated, rect)

    # fixed aircraft symbol in the middle
    pygame.draw.line(screen, (255, 220, 0), (cx - 60, cy), (cx - 20, cy), 4)
    pygame.draw.line(screen, (255, 220, 0), (cx + 20, cy), (cx + 60, cy), 4)
    pygame.draw.circle(screen, (255, 220, 0), (cx, cy), 4)

    # HUD text
    screen.blit(font.render(f"ALT  {altitude:6.0f} ft   (target {target_alt:.0f})", True, (230, 230, 230)), (16, 16))
    screen.blit(font.render(f"V/S  {vspeed*60:+5.0f} ft/min", True, (230, 230, 230)), (16, 40))
    screen.blit(font.render(f"BANK {math.degrees(roll):+5.1f} deg", True, (230, 230, 230)), (16, 64))
    screen.blit(font.render("UP / DOWN = change target altitude", True, (150, 160, 180)), (16, H - 30))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
