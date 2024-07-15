import sys
import torch
import facer
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats



device = 'cuda' if torch.cuda.is_available() else 'cpu'

def segment_and_extract_hex(image_path):
    ## Facial Segmentation w/ FACER
    image = facer.hwc2bchw(facer.read_hwc(image_path)).to(device=device)  # image: 1 x 3 x h x w

    face_detector = facer.face_detector('retinaface/mobilenet', device=device)
    with torch.inference_mode():
        faces = face_detector(image)

    # facer.show_bchw(facer.draw_bchw(image, faces))

    face_parser = facer.face_parser('farl/celebm/448', device=device) # optional "farl/lapa/448"

    with torch.inference_mode():
        faces = face_parser(image, faces)

    seg_logits = faces['seg']['logits']
    seg_probs = seg_logits.softmax(dim=1)  # nfaces x nclasses x h x w
    n_classes = seg_probs.size(1)
    vis_seg_probs = seg_probs.argmax(dim=1).float()/n_classes*255
    vis_img = vis_seg_probs.sum(0, keepdim=True)
    # facer.show_bhw(vis_img)
    # facer.show_bchw(facer.draw_bchw(image, faces))

    # Convert the original image tensor to a numpy array and then to a PIL image
    original_image = image.squeeze(0).permute(1, 2, 0).cpu().numpy().astype('uint8')
    original_image = Image.fromarray(original_image)

    # Define the list of facial parts corresponding to the class indices
    facial_parts = [
        "Background", "Neck", "Skin", "Cloth", "Right Ear", "Left Ear", "Right Brow", "Left Brow",
        "Right Eye", "Left Eye", "Nose", "Mouth", "Lower Lip", "Upper Lip", "Hair", "Eye Glasses",
        "Hat", "Ear Ring", "Necklace"
    ]

    # if n_classes > len(facial_parts):
    #     facial_parts += [f'Class_{i}' for i in range(len(facial_parts), n_classes)]

    # print('Facial parts list:')
    # for idx, part in enumerate(facial_parts):
    #     print(f'Class {idx}: {part}')

    # Initialize a list to store non-empty segments
    non_empty_segments = []

    for class_idx in range(n_classes):
        # Create a mask for the current class
        class_mask = (seg_probs.argmax(dim=1) == class_idx).float()

        # Check if the segment is non-empty
        if class_mask.sum() > 0:
            # Resize mask to match original image dimensions
            class_mask = class_mask.squeeze(0).cpu().numpy()
            class_mask = np.repeat(class_mask[:, :, np.newaxis], 3, axis=2)  # Repeat mask across the color channels

            # Apply the mask to the original image
            segment_image = np.array(original_image) * class_mask

            # Convert the segment image to PIL format and save it
            segment_image = Image.fromarray(segment_image.astype('uint8'))
            part_name = facial_parts[class_idx] if class_idx < len(facial_parts) else f'Class_{class_idx}'
            segment_image.save(f'segments/segment_{part_name}.png')

            # Add the segment image to the list
            non_empty_segments.append((class_idx, segment_image, part_name))

    # Display non-empty segments
    # n_non_empty_segments = len(non_empty_segments)
    # fig, axs = plt.subplots(1, n_non_empty_segments, figsize=(5 * n_non_empty_segments, 5))  # Adjust figsize as needed

    # for idx, (class_idx, segment_image, part_name) in enumerate(non_empty_segments):
    #     axs[idx].imshow(segment_image)
    #     axs[idx].axis('off')
    #     axs[idx].set_title(f'{part_name}')

    # plt.show()

    ## Color Extraction

    # Define the class indices for skin, eyes, and hair
    skin_class_idx = facial_parts.index("Skin")
    right_eye_class_idx = facial_parts.index("Right Eye")
    left_eye_class_idx = facial_parts.index("Left Eye")
    hair_class_idx = facial_parts.index("Hair")

    # Function to compute the average color of a segment
    def compute_average_color(mask, image):
        mask = mask.squeeze(0).cpu().numpy()
        segment_pixels = np.array(image)[mask.astype(bool)]
        if segment_pixels.size == 0:
            return [0, 0, 0]
        average_color = segment_pixels.mean(axis=0)
        return average_color.astype(int)

    # Function to compute the most common color of a segment
    def compute_mode_color(mask, image):
        mask = mask.squeeze(0).cpu().numpy()
        segment_pixels = np.array(image)[mask.astype(bool)]
        if segment_pixels.size == 0:
            return [0, 0, 0]
        mode_color = stats.mode(segment_pixels, axis=0)[0][0]
        if isinstance(mode_color, np.ndarray):
            return mode_color.astype(int)
        else:
            return np.array([mode_color] * 3).astype(int)

    # Create masks for skin, eyes, and hair
    skin_mask = (seg_probs.argmax(dim=1) == skin_class_idx).float()
    right_eye_mask = (seg_probs.argmax(dim=1) == right_eye_class_idx).float()
    #left_eye_mask = (seg_probs.argmax(dim=1) == left_eye_class_idx).float()
    hair_mask = (seg_probs.argmax(dim=1) == hair_class_idx).float()

    # Compute the average colors for skin and hair, and mode colors for eyes
    skin_color = compute_average_color(skin_mask, original_image)
    right_eye_color = compute_mode_color(right_eye_mask, original_image)
    #left_eye_color = compute_mode_color(left_eye_mask, original_image)
    hair_color = compute_average_color(hair_mask, original_image)

    # Convert RGB to hex
    def rgb_to_hex(rgb):
        return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])

    skin_hex = rgb_to_hex(skin_color)
    right_eye_hex = rgb_to_hex(right_eye_color)
    #left_eye_hex = rgb_to_hex(left_eye_color)
    hair_hex = rgb_to_hex(hair_color)

    # Print the hex colors
    print("Skin color (hex):", skin_hex)
    print("Right eye color (hex):", right_eye_hex)
    #print("Left eye color (hex):", left_eye_hex)
    print("Hair color (hex):", hair_hex)

    return skin_hex, right_eye_hex, hair_hex

# #Example usage:
# image_path = 'uploads/black_actress.jpg'
# colors = segment_and_extract_hex(image_path)
# print(colors)

