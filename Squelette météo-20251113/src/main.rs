mod tests;

fn main() {
    let meteo_ajh_orleans = Meteo {
	temperature: 15.0,
	ciel: Ciel::Clair,
    };
    
    println!("Hello, world!");
}


/// L’état du ciel un jour donné
#[derive(Clone, Copy, Debug)]
enum Ciel {
    /// Ciel clair
    Clair,

    /// Ciel nuageux
    Nuageux,

    /// Pluie, avec un entier (non-signé sur 32 bits) indiquant le quantité de pluie prévue (en mm)
    Pluie(f32),

    /// Neige, avec un entier indiquant la hauteur de neige prévue (en cm)
    Neige(f32),

    /// Brouillard
    Brouillard
}


#[derive(Debug, Copy, Clone)]
struct Meteo {
    temperature: f32,
    ciel: Ciel,
}



fn decrit_ciel(c: Ciel) -> &'static str {
    match c {
	Ciel::Clair => "il fait beau, youpi!",
	Ciel::Nuageux => "il y a des nuages :-(",
	Ciel::Brouillard => "Il░y a d░░brouillard, on░░’y v░░t rie░",
	Ciel::Neige(_) | Ciel::Pluie(_) => "risque d’intempéries",
    }
}


fn to_farenheit(t_celsius: f32) -> f32 {
    t_celsius * 5.0 / 9.0
}

fn que_porter(temperature: f32) -> &'static str {
    if temperature < 0.0 {
	return "un bon manteau";
    } else if temperature < 15.0 {
	return "un petit pull";
    } else if temperature < 25.0 {
	return "une chemise";
    } else {
	return "un T-shirt";
    }
}
