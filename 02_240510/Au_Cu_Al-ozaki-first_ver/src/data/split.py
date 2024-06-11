from PIL import Image
import os

def split_image(image_path, rows, columns, output_dir):
    img = Image.open(image_path)
    w, h = img.size
    w_chunk = w // columns
    h_chunk = h // rows

    for i in range(rows):
        for j in range(columns):
            left = j * w_chunk
            top = i * h_chunk
            right = (j + 1) * w_chunk
            bottom = (i + 1) * h_chunk
            crop_img = img.crop((left, top, right, bottom))
            crop_img.save(os.path.join(output_dir, f"{os.path.splitext(os.path.basename(image_path))[0]}_{i}_{j}.png"))

if __name__ == "__main__":
    # ROWS, COLUMNS = 6, 4
    # IMAGE_PATH = "./data/raw/images/0.png"
    # OUTPUT_DIR = "./outputs/figures/split"

    # os.makedirs(OUTPUT_DIR, exist_ok=True)
    # split_image(IMAGE_PATH, ROWS, COLUMNS, OUTPUT_DIR)

    ROWS, COLUMNS = 6, 8
    INPUT_DIR = "./data/raw"
    OUTPUT_DIR = "./data/interim/split"
    
    for type in ["images", "labels"]:
        input_dir = f"{INPUT_DIR}/{type}"
        output_dir = f"{OUTPUT_DIR}/{type}"
        os.makedirs(output_dir, exist_ok=True)
        for file_name in os.listdir(input_dir):
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(input_dir, file_name)
                split_image(image_path, ROWS, COLUMNS, output_dir)