use image::io::Reader as ImageReader;
use image::{ImageError, RgbImage};

const WHITE: image::Rgb<u8> = image::Rgb([255, 255, 255]);

fn main() -> Result<(), ImageError> {
    println!("Hello, world!");
    let mut img = ImageReader::open("iut.jpg")?.decode()?.into_rgb8();
    un_pixel_sur_deux(&mut img);
    img.save("out.png")?;

    Ok(())
}

fn un_pixel_sur_deux(img: &mut RgbImage) {
    for (x, y, pixel) in img.enumerate_pixels_mut() {
        if (x + y) % 2 == 0 {
            *pixel = WHITE;
        }
    }
}