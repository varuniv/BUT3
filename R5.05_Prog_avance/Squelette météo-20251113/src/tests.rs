use crate::{Ciel, decrit_ciel, to_farenheit, que_porter, alerte};

#[test]
fn test_decrit_ciel() {
    let b = decrit_ciel(Ciel::Brouillard);
    assert!(b.contains("░"));
    let n = decrit_ciel(Ciel::Nuageux);
    assert!(!n.contains("░"));
}


#[test]
fn test_conversion_farenheit() {
    let c = 0.0;
    let f = to_farenheit(c);
    assert!(f < 32.001, "{} trop grand", f);
    assert!(f > 31.999, "{} trop petit", f);
}

#[test]
fn test_que_porter() {
    let mut t = 30.0;
    assert_eq!(que_porter(t), "un T-shirt");
    t = 20.0;
    assert_eq!(que_porter(t), "une chemise");    
    t = -15.0;
    assert_eq!(que_porter(t), "un anorak");
}

#[test]
fn test_alerte() {
    assert!(alerte(Ciel::Nuageux) == false);
    assert!(alerte(Ciel::Pluie(20.0)) == true);
    assert!(alerte(Ciel::Pluie(2.0)) == false);
    assert!(alerte(Ciel::Neige(10.0)) == true);
}