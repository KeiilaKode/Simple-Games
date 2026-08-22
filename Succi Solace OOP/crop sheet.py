import pygame

pygame.init()
# Initialize a hidden dummy display so pygame image operations work
pygame.display.set_mode((1, 1), pygame.NOFRAME)

input_path = "spritsheets/enemies/lvl_3_enemies/demented_attack_ss.png"

# Load the original sheet without convert_alpha
raw_sheet = pygame.image.load(input_path)
num_frames = 10
frame_w = raw_sheet.get_width() // num_frames  # 1920
frame_h = raw_sheet.get_height()                # 1080

target_frame_w = 810
target_sheet = pygame.Surface((target_frame_w * num_frames, frame_h), pygame.SRCALPHA)

for i in range(num_frames):
    # Slice frame
    sub = raw_sheet.subsurface((i * frame_w, 0, frame_w, frame_h))
    # Crop center 810px
    crop_x = (frame_w - target_frame_w) // 2
    cropped_frame = sub.subsurface((crop_x, 0, target_frame_w, frame_h))
    # Blit into target sheet
    target_sheet.blit(cropped_frame, (i * target_frame_w, 0))

pygame.image.save(target_sheet, input_path)
print("Done! Resized sheet to 8100x1080.")
pygame.quit()