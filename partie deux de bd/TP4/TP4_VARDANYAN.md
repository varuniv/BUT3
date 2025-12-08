Sargis VARDANYAN TP4

# Exercice 1
    
## Question 1
        
### a 
Le chemps seats represents les places, sièges dans le théâtre

### b 
Le chemps seatsAvailable évite de faire des calculs et donne une informations direct. C'est un gagne de temps.

## Question 2

### a 

Le lien entre la collection theaters et la collection sessions est theaterId, qui présente théâtre dans la quelle la session aura lieux.


### b
Le chemps reservations represante les réservations des sièges dans le théâtre.


# Exercice 2 

## 1 
```js
db.sessions.insertOne[{
        "_id": { "$oid": "5500632d2dc02be024ba5c73" },
        "theaterId": 1,
        "name": "Concert de jazz",
        "start": { "$date": "2025-01-20T20:00:00Z" },
        "end": { "$date": "2025-01-20T22:00:00Z" },
        "price": 20,
        "seatsAvailable": 30,
        "seats": [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ],
        "reservations": []
    }]
```

## 2
```js 
db.sessions.find({theaterId : 1})
```

# Exercice 3

## 1 
```js 
db.sessions.updateOne(
    {"name": "Concert de jazz"},
    
    {$set: {"seats.1.0": 1,"seats.1.1": 1},
    $push: {
      reservations: {
        seats: [
          { row: 1, col: 0 },
          { row: 1, col: 1 }
        ],date: new Date()}},
    $inc: {seatsAvailable: -2}}
)

```

## 2 
```js
db.sessions.find({name : "Concert de jazz"})
[
  {
    _id: ObjectId('5500632d2dc02be024ba5c73'),
    theaterId: 1,
    name: 'Concert de jazz',
    start: ISODate('2025-01-20T20:00:00.000Z'),
    end: ISODate('2025-01-20T22:00:00.000Z'),
    price: 20,
    seatsAvailable: 28,
    seats: [
      [ 0, 0, 0, 0, 0 ],
      [ 1, 1, 0, 0, 0 ],
      [ 0, 0, 0, 0, 0 ],
      [ 0, 0, 0, 0, 0 ],
      [ 0, 0, 0, 0, 0 ],
      [ 0, 0, 0, 0, 0 ]
    ],
    reservations: [
      {
        seats: [ { row: 1, col: 0 }, { row: 1, col: 1 } ],
        date: ISODate('2025-12-08T09:30:05.198Z')
      }
    ]
  }
]
```
## 3 
```js 
db.sessions.updateOne(
    {"name": "Concert de jazz"},
    {$set: {"seats.1.0": 0,"seats.1.1": 0},
    $pull: {
      reservations: {
        seats: [
          { row: 1, col: 0 },
          { row: 1, col: 1 }
        ]
      }
    },
    $inc: {seatsAvailable: 2}}
)

```


# Exercice 4


```js
db.carts.insertOne({
    "_id": 1,
    "state": "active",
    "total": 0,
    "reservations": [],
    "createdOn": ISODate("2025-01-01T12:00:00Z"),
    "modifiedOn": ISODate("2025-01-01T12:00:00Z")
})


db.cart.updateOne(
    { _id: 1 },
    {$push: {
            reservations: {
                sessionName: "Concert de jazz",
                seats: [
                    { row: 1, col: 0 },
                    { row: 1, col: 1 }
                ],
                pricePerSeat: 20,
                quantity: 2,
                date: new Date()
            }
        },
        $inc: { total: 40 },
        $set: { modifiedOn: new Date() }
    })

```


# Ex 5 

```js 
db.sessions.updateOne(
    {"name": "Concert de jazz"},
    
    {$set: {"seats.2.0": 1,"seats.2.1": 1,"seats.2.2": 1,},
    $push: {
      reservations: {
        seats: [
          { row: 2, col: 0 },
          { row: 2, col: 1 },
          { row: 2, col: 2 }

        ],date: new Date()}},
    $inc: {seatsAvailable: -3}}
)

db.carts.insertOne({
    "_id": 2,
    "state": "active",
    "total": 0,
    "reservations": [],
    "createdOn": ISODate("2025-11-01T12:00:00Z"),
    "modifiedOn": ISODate("2025-11-01T12:00:00Z")
})


db.cart.updateOne(
    { _id: 2 },
    {$push: {
            reservations: {
                sessionName: "Concert de jazz",
                seats: [
                    { row: 2, col: 0 },
                    { row: 2, col: 1 },
                    { row: 2, col: 2 }
                ],
                pricePerSeat: 20,
                quantity: 3,
                date: new Date()
            }
        },
        $inc: { total: 60 },
        $set: { modifiedOn: new Date() }
    })

db.cart.updateOne
```

