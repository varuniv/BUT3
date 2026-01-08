use argh::FromArgs;
use image::io::Reader as ImageReader;
use image::{ImageError, Rgb};

/// Application de conversion d'images en noir et blanc
#[derive(FromArgs)]
struct Args {
    /// image d'entrée
    #[argh(positional)]
    input: String,

    /// fichier de sortie (par défaut: out.png)
    #[argh(option, short = 'o', default = "String::from(\"out.png\")")]
    output: String,
}

// Calcul de la luminosité d'un pixel RGB (entre 0 et 1)
fn luminosity(p: Rgb<u8>) -> f32 {
    (0.2126 * p[0] as f32
        + 0.7152 * p[1] as f32
        + 0.0722 * p[2] as f32) / 255.0
}

fn main() -> Result<(), ImageError> {
    let args: Args = argh::from_env();

    // Ouverture de l'image
    let mut img = ImageReader::open(&args.input)?
        .decode()?
        .into_rgb8();

    let (w, h) = img.dimensions();

    // Affichage d'un pixel (Q4)
    let pixel = img.get_pixel(32, 52);
    println!("Pixel (32,52) = {:?}", pixel);

    // Buffer de luminosité
    let mut buffer = vec![vec![0.0f32; w as usize]; h as usize];

    // Initialisation du buffer
    for y in 0..h {
        for x in 0..w {
            let p = img.get_pixel(x, y);
            buffer[y as usize][x as usize] = luminosity(*p);
        }
    }

    // Diffusion d'erreur
    for y in 0..h {
        for x in 0..w {
            let old = buffer[y as usize][x as usize];
            let new = if old > 0.5 { 1.0 } else { 0.0 };
            let error = old - new;

            let v = if new > 0.0 { 255 } else { 0 };
            img.put_pixel(x, y, Rgb([v, v, v]));

            if x + 1 < w {
                buffer[y as usize][(x + 1) as usize] += error * 0.5;
            }
            if y + 1 < h {
                buffer[(y + 1) as usize][x as usize] += error * 0.5;
            }
        }
    }

    // Sauvegarde
    img.save(&args.output)?;
    println!("Image sauvegardée dans {}", args.output);

    Ok(())
}
