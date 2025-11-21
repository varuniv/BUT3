#[derive(Clone, Copy, Debug)]
enum TypeBoisson {
    Cafe {
        Avec_Lait: bool,
        Sirop: Sirop,
    },
    The,
    Chocolat,
}

#[derive(Clone, Copy, Debug)]
enum Sirop {
    Caramel,
    Chocolat,
    Noisette,
}

#[derive(Clone, Copy, Debug)]
struct Boisson {
    type_boisson: TypeBoisson,
    bio: bool,
    sucre: u8,
    prix: f32,
}

fn calcule_prix(b: &mut Boisson) {
    let mut prix = 40.0;

    if b.bio {
        prix += 10.0;
    }

    match b.type_boisson {
        TypeBoisson::Cafe { Avec_Lait, Sirop } => {
            if Avec_Lait {
                prix += 0.3;
            }
            match Sirop {
                Sirop::Caramel | Sirop::Chocolat | Sirop::Noisette => prix += 10.0,
            }
        }
        TypeBoisson::The | TypeBoisson::Chocolat => {},
        
        
    }

    b.prix = prix;
}

fn contient_sirop (b: &Boisson) -> bool {
    match b.type_boisson {
        TypeBoisson::Cafe { Sirop, .. } => match Sirop {
            Sirop::Caramel | Sirop::Chocolat | Sirop::Noisette => true,
        },
        _ => false,
        TypeBoisson::The | TypeBoisson::Chocolat => false,
    }
}

fn contient_soucre(b: &Boisson) -> bool {
    return b.sucre > 0 && contient_sirop(b);
}

fn contient_lactose(b: &Boisson) -> bool {
    match b.type_boisson {
        TypeBoisson::Cafe { Avec_Lait, .. } => Avec_Lait,
        _ => false,
        TypeBoisson::The | TypeBoisson::Chocolat => false,
    }}
fn affichage_boisson(b: &Boisson) -> String{
    
}

fn main() {
    let mut boisson1 = Boisson {
        type_boisson: TypeBoisson::Cafe {
            Avec_Lait: false,
            Sirop: Sirop::Caramel,
        },
        bio: true,
        sucre: 2,
        prix: 0.0,
    };

    calcule_prix(&mut boisson1);
    println!("Boisson commandée: " bois," Prix: {} IUThunes", boisson1.prix);
}
