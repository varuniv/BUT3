main() {
    
}


#[derive(Clone, Copy, Debug)]
enum Type_Boisson {
    Cafe,
    The,
    Chocolat
}

#[derive(Clone, Copy, Debug)]
enum Sirop {
    Caramel,
    Chocolat,
    Noisette
}

#[derive(Clone, Copy, Debug)]
struct Boisson {
    type_boisson: Type_Boisson,
    bio: bool,
    lait: bool ==> false,
    sucre: i32,
    sirop: Sirop,
    prix: f32 ==> 0.0,
}

fn calcule_prix(b: &mut Boisson) {
    let mut prix = 40.0;

    if b.bio {
        prix += 10.0;
    }
    if Type_Boisson::Cafe == b.type_boisson {
        if b.lait {
        prix += 0.3;
    }}

    match b.sirop {
        Sirop::Caramel | Sirop::Chocolat | Sirop::Noisette => prix += 10.0,
    }

    b.prix = prix;
}