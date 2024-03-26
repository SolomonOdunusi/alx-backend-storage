#!/usr/bin/env python3
""" All the students by ave score"""


def top_students(mongo_collection):
    """ Function that returns all students sorted by average score """

    return mongo_collection.aggregate([
        {'$project':
            {'name': '$name', 'averageScore': {'$avg': '$topics.score'}}},
        {'$sort': {'averageScore': -1}}
    ])
