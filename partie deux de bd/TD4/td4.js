db.createCollection("orders");
db.createCollection("inventories");
db.createCollection("products");
db.createCollection("carts");


db.products.insertMany([
{ "_id": 1, "name": "Chaussures JC", "properties": {} },
{ "_id": 2, "name": "T-shirt Nike", "properties": {} },
{ "_id": 3, "name": "Casquette Adidas", "properties": {} }]);

db.inventories.insertMany([
{ "_id": 1, "quantity": 100, "reservations": [] },
{ "_id": 2, "quantity": 50, "reservations": [] },
{ "_id": 3, "quantity": 20, "reservations": [] }]);

db.carts.insertOne({ "_id": 1001, "state": "active", "modifiedOn": ISODate("2024-12-01T10:00:00Z"), "products": [] });


//Partie B : 

//Ex1 :Ajouter 2 paires de Chaussures JC (productId: 1) au panier (cartId: 1001)
db.carts.updateOne({ "_id": 1001 },{$push: {"products": {"productId": 1,"quantity": 2}},$set: { "modifiedOn": ISODate("2024-12-01T10:05:00Z") }});

db.inventories.updateOne({ "_id": 1 },{$inc: { "quantity": -2 },$push: {"reservations": {"cartId": 1001,"quantity": 2,"reservedOn": ISODate("2024-12-01T10:05:00Z")}}});



//Ex2
db.carts.updateOne({ "_id": 1001 },{$inc: { "products.$[elem].quantity": 2 },"$set": { "modifiedOn": ISODate("2024-12-01T10:10:00Z") }},{ arrayFilters: [ { "elem.productId": 1 } ] });

db.inventories.updateOne({ "_id": 1 },{$inc: { "quantity": -4 },$push: {"reservations": {"cartId": 1001,"quantity": 2,"reservedOn": ISODate("2024-12-01T10:05:00Z")}}});


//Ex3
var d = new Date();
d.setMinutes(d.getMinutes() - 30);
var panierExpire = db.carts.find({modifiedOn: {$lte: d, state: "active"}});

panierExpire.forEach(function(panier) {
    panier.products.forEach(function(produit) {
        db.inventories.update(
            { _id: produit.productId },
            {
                $inc: { quantity: produit.quantity },
                $pull: { reservations: { cartId: panier._id } }
            }
        );
    });
    db.carts.updateOne(
        { _id: panier._id },
        { $set: { state: "expired" } }
    );
}
            
        )

