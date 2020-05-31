from PIL import Image, ImageDraw, ImageFilter


def crop_max_square(pil_img):
    return crop_center(pil_img, min(pil_img.size), min(pil_img.size))


def crop_center(pil_img, crop_width, crop_height):
    img_width, image_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (image_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (image_height + crop_height) // 2))


def mask_circle_transparent(pil_img, blur_radius, offset=0):
    offset = blur_radius * 2 + offset
    mask = Image.new("L", pil_img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((offset, offset, pil_img.size[0] - offset, pil_img.size[1] - offset), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(blur_radius))

    result = pil_img.copy()
    result.putalpha(mask)
    return result


def circle_image(temp_in_path, image_file):
    mark_img = Image.open(image_file)
    thumb_width = 150

    im_square = crop_max_square(mark_img).resize((thumb_width, thumb_width), Image.LANCZOS)
    im_thumb = mask_circle_transparent(im_square, 0)
    out_image = image_file.split('/')[-1]
    out_image_name = out_image.split('.')[0] + '.png'
    out_image = temp_in_path + '\\' + out_image_name
    im_thumb.save(out_image)
    return out_image_name
