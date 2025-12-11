use image::io::Reader as ImageReader;
use image::{ImageError, RgbImage,Rgb,Pixel};
use rand::Rng;

const WHITE: image::Rgb<u8> = image::Rgb([255, 255, 255]);
const BLACK: image::Rgb<u8> = image::Rgb([0, 0, 0]);

fn main() -> Result<(), ImageError> {
    println!("Hello, world!");
    let mut img = ImageReader::open("iut.jpg")?.decode()?.into_rgb8();
    dithering(&mut img);
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

fn seuillage(img : &mut RgbImage) {
    for (_x, _y, pixel) in img.enumerate_pixels_mut() {
        let luminosite = pixel.to_luma_alpha();
        let seuil:u8 = 127;
        *pixel = if luminosite[0] > seuil { WHITE } else { BLACK };
    }
}

fn dithering(img : &mut RgbImage) {
    for (_x, _y, pixel) in img.enumerate_pixels_mut() {
        let luminosite = pixel.to_luma_alpha();
        let num = rand::thread_rng().gen_range(0..255);
        let seuil:u8 = num;
        *pixel = if luminosite[0] > seuil { WHITE } else { BLACK };
    }
}