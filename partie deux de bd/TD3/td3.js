db.createCollection("Personne", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["nom", "prenom", "age", "adresse"],
            properties: {
                nom: {
                    bsonType: "string",
                    description: "Le nom de la personne est obligatoire" },
                prenom: {
                    bsonType: "string",
                    description: "Le prénom de la personne est obligatoire" },
                datenaissance: {
                    bsonType: "date",
                    description: "La date de naissance de la personne est obligatoire" },
                habitation: {
                    bsonType: "object",
                    required: ["adresse", "ville"],
                    properties: {
                        adresse: {
                            bsonType: "string",
                            description: "L'adresse est obligatoire" },
                        ville: {
                            bsonType: "string",
                            description: "La ville est obligatoire" } } },
                domaine: {
                    bsonType: "array",
                    items: {
                        bsonType: "string" },
                    description: "Le domaine d'expertise est un tableau de chaînes de caractères" },
                emplois: {
                    bsonType: "array",
                    items: {
                        bsonType: "object",
                        required: ["id_établissement", "qualité", "date"],
                        properties: {
                            id_établissement: {
                                bsonType: "objectId",
                                description: "L'identifiant de l'établissement est obligatoire" },
                            qualité: {
                                bsonType: "string",
                                description: "La qualité est obligatoire" },
                            date: {
                                bsonType: "date",
                                description: "La date est obligatoire" } } },
                    description: "Les emplois sont un tableau d'objets" } } } } });

db.createCollection("Établissement", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["raison_sociale", "adresse", "ville"],
            properties: {
                raison_sociale: {
                    bsonType: "string",
                    description: "La raison sociale de l'établissement est obligatoire" },
                adresse: {
                    bsonType: "string",
                    description: "L'adresse de l'établissement est obligatoire" },
                ville: {
                    bsonType: "string",
                    description: "La ville de l'établissement est obligatoire" } } } } });  



// exercise 2
