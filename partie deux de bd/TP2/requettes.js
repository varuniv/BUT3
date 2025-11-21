// Exercice 1 

pipeline = [ 
    {$match : { capacite: {$gt: 50}}},
    {$project : { _id: 0, ville: "$adresse.ville", grande : {$gte : ["$capacite",1000]}} }
 ]
db.salles.aggregate(pipeline)
db.salles.aggregate([{$match : { capacite: {$gt: 50}}},
    {$project : { _id: 0, ville: "$adresse.ville", grande : {$gte : ["$capacite",1000]}} }])


// Exercice 2
db.salles.aggregate([
    {$project : {
        apres_extension : {$add : ["$capacite", 100]},
        avant_extension : "$capacite",
        nom : "$nom"
    }}])


// Exercice 3
pipeline = [{$match : { capacite: {$gt: 50}}},
    {$project : {
        num_departement : {$substrBytes : ["$adresse.codePostal",0,2]},
        capacite: 1,
        _id : 0
    }},
    {$group : {
        _id : "$num_departement",
        capacite_totale : {$sum : "$capacite"}
    }},
    {$sort : {_id : 1}}
]

//Exercice 4
pipeline = [
    {$unwind : "$styles"},
    { $group : {
        _id : "$styles",
        nombre_salles : { $sum : 1 }
    }},
    { $sort : { _id : 1 } }
]


// Exercice 6
pipeline = [
    { $project: 
        {   _id : 0,
            nom: 1,
            avis_excellents: { $filter: { input: "$avis", as: "bestavis",cond: { $gte: ["$$bestavis.note", 10] } } } } }
]

// Exercice 7 
pipeline = [
    {$project : {
        _id : 0,
        ville : "$adresse.ville",
    }},
    {$group : {
        _id : "$ville",
        nombre_salles : { $sum : 1 }
    }},
    { $sort : { nombre_salles : -1 } }
]


// Exercice 8
pipeline = [
    {$unwind : "$styles"},
    { $sortByCount : "$styles" }

]