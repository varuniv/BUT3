# Ditherpunk – retour au monochrome

Ce projet a été réalisé dans le cadre du TP *Ditherpunk – retour au monochrome*.  
Il utilise la bibliothèque Rust `image` (version 0.24) pour effectuer différents
traitements sur des images, principalement le passage en noir et blanc.

Le programme charge une image, parcourt ses pixels et applique un traitement
de conversion en monochrome, avec ou sans diffusion d’erreur.

### Interface en ligne de commande (argh)

L’interface en ligne de commande est implémentée à l’aide de la bibliothèque
`argh`.

Le programme accepte :
- un argument positionnel correspondant au fichier image d’entrée
- une option `--output` (ou `-o`) permettant de choisir le nom du fichier de sortie

Exemple d’utilisation :

cargo run -- image.png --output resultat.png

Si l’option `--output` n’est pas fournie, l’image est enregistrée par défaut
dans le fichier `out.png`.
---

## Questions traitées

### Question 1 – Bibliothèque image

Le projet a été créé avec Cargo et utilise la bibliothèque `image` en version 0.24,
comme demandé dans l’énoncé.

---

### Question 2 – Chargement d’une image

L’image est ouverte avec `ImageReader::open(...).decode()`.  
La fonction `decode()` retourne un `Result<DynamicImage, ImageError>` :
- `DynamicImage` représente une image générique dont le format peut varier
- `ImageError` représente une erreur éventuelle lors du chargement ou du décodage

Dans le programme, l’image est ensuite convertie en `RgbImage` afin de pouvoir
manipuler directement les pixels RGB.

---

### Question 3 – Sauvegarde de l’image

L’image traitée est sauvegardée au format PNG à l’aide de la méthode `save("out.png")`.

---

### Question 4 – Accès à un pixel

Le programme affiche dans le terminal la couleur du pixel de coordonnées `(32, 52)`
afin de vérifier l’accès aux pixels de l’image.

---

### Questions 6 & 7 – Passage en monochrome par seuillage

La luminosité d’un pixel est calculée à partir de ses composantes RGB selon la
formule classique de luminance :

0.2126 × R + 0.7152 × G + 0.0722 × B


Cette valeur est normalisée entre 0 et 1.  
Si la luminosité est supérieure à 0.5, le pixel est remplacé par du blanc, sinon
par du noir.

---

### Question 9 – Diffusion d’erreur en noir et blanc

Une diffusion d’erreur simple est implémentée pour améliorer le rendu du
monochrome.

Pour chaque pixel :
- on choisit noir ou blanc selon sa luminosité
- on calcule l’erreur commise
- cette erreur est diffusée vers les pixels voisins non encore traités

La matrice de diffusion utilisée est la suivante :

0.5
0.5 0



50 % de l’erreur est envoyé au pixel de droite, et 50 % au pixel du dessous.
Un buffer de luminosité séparé est utilisé pour stocker les valeurs modifiées
avant le traitement.

---

## Limitations

Les parties suivantes du sujet n’ont pas été implémentées par manque de temps :
- Passage à une palette de couleurs (questions 6 à 8 de la partie 2)
- Diffusion d’erreur pour les palettes de couleurs (questions 10 à 13)

Le projet se concentre donc uniquement sur le passage en noir et blanc avec
diffusion d’erreur simple.

---

## Résultat

L’image de sortie est enregistrée dans le fichier `out.png`.
