from bson import ObjectId
from flask import jsonify
from datetime import datetime

from database.connect import accidents, db
from datetime import datetime
#
#
# #1
def get_sum_accidents_by_region(region):
     sum_accidents = accidents.count_documents({'beat_of_occurrence': region})
     return sum_accidents
#






def get_accidents_by_region_and_date(region, start_date_str, end_date_str):
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    return list(db.accidents.find({
        'beat_of_occurrence': region,
        'crash_date': {
            '$gte': start_date,
            '$lte': end_date
        }
    }))
















def get_accidents_grouped_by_cause(region):
    pipeline = [
        {
            "$match": {
                "beat_of_occurrence": region
            }
        },
        {
            "$group": {
                "_id": "$prim_contributory_cause",
                "total_accidents": { "$sum": 1 },
                "accidents": {
                    "$push": {
                        "accident_id": "$accident_id",
                        "crash_date": "$crash_date",
                        "injuries_id": "$injuries_id"
                    }
                }
            }
        },
        {
            "$sort": {
                "total_accidents": -1
            }
        }
    ]


    result = list(db.accidents.aggregate(pipeline))

    return jsonify(result)

