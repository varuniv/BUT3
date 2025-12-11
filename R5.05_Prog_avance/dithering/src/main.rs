use image::io::Reader as ImageReader;
use image::{ImageError};

fn main() -> Result<(), ImageError> {
    println!("Hello, world!");
    let img = ImageReader::open("iut.jpg")?.decode()?.into_rgb8();
    img.save("out.png")?;

    Ok(())
}