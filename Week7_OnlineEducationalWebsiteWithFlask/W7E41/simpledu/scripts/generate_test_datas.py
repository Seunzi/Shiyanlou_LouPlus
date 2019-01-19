import os
import json
from random import randint
from faker import Faker
from simpledu.models import db,User,Course,Chapter

# building faker factory
fake = Faker()

# generate a teacher user
def iter_users():
    yield User(
            username='Jack Lee',
            email='jacklee@example.com',
            password='zxcvbnm',
            job='Develop Engineer'
            )

# read courses data from datas,generate courses 
# and set the author be the teacher user
# that you just generate
def iter_courses():
    author = User.query.filter_by(username='Jack Lee').first()
    with open(os.path.join(os.path.dirname(__file__),'..','datas','courses.json')) as f:
        courses = json.load(f)
    for course in courses:
        yield Course(
                name=course['name'],
                descriptions=course['description'],
                image_url=course['image_url'],
                author=author
                )

def iter_chapters():
    for course in Course.query:
        # generate 3-10 chapter for the courses
        for i in range(randint(3,10)):
            yield Chapter(
                # generate a sentence as courses chapter name
                name=fake.sentence(),
                course=course,
                video_url='https://labfile.oss.aliyuncs.com/courses/923/week2_mp4/2-1-1-mac.mp4',
                video_duration='{}:{}'.format(randint(10,30),randint(10,59))
                )

def run():
    for user in iter_users():
        db.session.add(user)

    for course in iter_courses():
        db.session.add(course)

    for chapter in iter_chapters():
        db.session.add(chapter)

    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
