from PIL import Image

def rotate_and_crop_image(current_time, image_path="my_clock/kellotaulu.png", output_path=None):
    # Lataa kuva
    img = Image.open(image_path)

    # Laske kulma, jonka mukaan kuva tulee kääntää
    minutes = (current_time.hour % 12) * 60 + current_time.minute
    angle = ( ( minutes + 30 - minutes % 30 ) / 720 * 360 )

    # Käännä kuvaa
    rotated_img = img.rotate(-angle, resample=Image.BICUBIC, center=(img.width / 2, img.height / 2))

    print(f"{rotated_img.width} x {rotated_img.height}")
    # Rajaa kuva haluttuun kokoiseen osaan
    cropped_img = rotated_img.crop((120, rotated_img.height - 186, 384, rotated_img.height - 10 ))

    # Tallenna käännetyt ja rajatut kuva
    if output_path:
        cropped_img.save(output_path)

    return cropped_img

if __name__ == "__main__":
    # Aseta kuvatiedoston ja tulostiedoston polut
    input_image_path = "kellotaulu.png"
    output_image_path = "rotated_and_cropped_kellotaulu.png"
