#!/usr/bin/env python3
"""
Returns all students sorted by average score.
"""

from pymongo import MongoClient

def top_students(mongo_collection):
    """
    Returns all students sorted by average score.

    Args:
        mongo_collection: pymongo collection object.

    Returns:
        List of student documents sorted by average score.
    """
    students = mongo_collection.find()

    # Calculate average score for each student
    for student in students:
        total_score = sum(topic['score'] for topic in student['topics'])
        average_score = total_score / len(student['topics'])
        student['averageScore'] = round(average_score, 2)

    # Sort students by average score
    sorted_students = sorted(students, key=lambda x: x['averageScore'], reverse=True)

    return sorted_students

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    students_collection = client.my_db.students
    top_students = top_students(students_collection)
    for student in top_students:
        print(f"[{student['_id']}] {student['name']} => {student['averageScore']}")
