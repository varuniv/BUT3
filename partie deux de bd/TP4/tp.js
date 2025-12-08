
db.sessions.insert[{
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