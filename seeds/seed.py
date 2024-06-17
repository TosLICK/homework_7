from random import randint
from faker import Faker
from sqlalchemy.exc import SQLAlchemyError

from conf.db import session
from conf.models import Teacher, Student, Subject, Grade, Group


fake = Faker('uk-UA')


def insert_teachers():
    for i in range(5):
        teacher = Teacher(
            id=i+1,
            fullname=fake.name()
        )
        session.add(teacher)

def insert_groups():
    for i in range(3):
        group = Group(
            id=i+1,
            name=fake.word()
        )
        session.add(group)

def insert_subjects():
    for i in range(7):
        subject = Subject(
            id=i+1,
            name=fake.word(),
            teacher_id=randint(1, 5)
        )
        session.add(subject)

def insert_students():
    for i in range(30):
        student = Student(
            id=i+1,
            fullname=fake.name(),
            group_id=randint(1, 3)
        )
        session.add(student)

def insert_grades():
    for student_i in range(1, 31):
        subject_i = 1
        for _ in range(randint(7, 20)):
            grade = Grade(
                grade=randint(0, 100),
                grade_date=fake.date_this_decade(),
                student_id=student_i,
                subject_id=subject_i
            )
            session.add(grade)
            if subject_i == 7:
                subject_i = 1
                continue
            subject_i += 1


# def insert_rel():
#     # students = session.query(Student).all()
#     # teachers = session.query(Teacher).all()
#     students = list(session.execute(select(Student)).scalars())
#     teachers = list(session.execute(select(Teacher)).scalars())

#     for student in students:
#         rel = TeacherStudent(teacher_id=choice(teachers).id, student_id=student.id)
#         session.add(rel)


if __name__ == '__main__':
    try:
        insert_teachers()
        insert_groups()
        session.commit()
        insert_students()
        insert_subjects()
        session.commit()
        insert_grades()
        session.commit()
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
    finally:
        session.close()
