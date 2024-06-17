from sqlalchemy import func, desc, select, and_

from conf.models import Grade, Teacher, Student, Subject, Group
from conf.db import session


def select_01():
    """
    -- Знайти 5 студентів із найбільшим середнім балом з усіх предметів
    SELECT s.id, s.fullname, ROUND(AVG(g.grade), 2) AS average_grade
    FROM students s
    JOIN grades g ON s.id = g.student_id
    GROUP BY s.id
    ORDER BY average_grade DESC
    LIMIT 5;
    """
    stmt = select(Student.id, Student.fullname, func.round(func.avg(Grade.grade), 2).label('avarage_grade'))\
                  .join(Grade).group_by(Student.id).order_by(desc('avarage_grade')).limit(5)
    result = session.execute(stmt).all()
    return result

def select_02():
    """
    -- Знайти студента із найвищим середнім балом з предмета з id=2
    SELECT s.id, s.fullname, ROUND(AVG(g.grade), 2) AS average_grade
    FROM students s
    JOIN grades g ON s.id = g.student_id
    WHERE g.subject_id = 2
    GROUP BY s.id
    ORDER BY average_grade DESC
    LIMIT 1;
    """
    stmt = select(Student.id, Student.fullname, func.round(func.avg(Grade.grade), 2).label('avarage_grade'))\
                  .join(Grade).where(Grade.subject_id==2).group_by(Student.id).order_by(desc('avarage_grade')).limit(1)
    result = session.execute(stmt).one()
    return result

def select_03():
    """
    -- Знайти середній бал у групах з предмета з id=4
    SELECT gr.id, gr.name, ROUND(AVG(g.grade), 2) AS average_grade
    FROM groups gr
    JOIN students s ON gr.id = s.group_id
    JOIN grades g ON s.id = g.student_id
    WHERE g.subject_id = 4
    GROUP BY gr.id;
    """
    stmt = select(Group.id, Group.name, func.round(func.avg(Grade.grade), 2).label('avarage_grade')).select_from(Group)\
                  .join(Student).join(Grade).where(Grade.subject_id == 4).group_by(Group.id)
    result = session.execute(stmt).all()
    return result

def select_04():
    """
    -- Знайти середній бал на потоці (по всій таблиці оцінок)
    SELECT ROUND(AVG(grade), 2) AS average_grade
    FROM grades;
    """
    stmt = select(func.round(func.avg(Grade.grade), 2).label('avarage_grade'))
    result = session.execute(stmt).one()
    return result

def select_05():
    """
    -- Знайти які курси читає викладач з id=4
    SELECT s.id, s.name
    FROM subjects s
    WHERE s.teacher_id = 4;
    """
    stmt = select(Subject.id, Subject.name).where(Subject.teacher_id == 4)
    result = session.execute(stmt).all()
    return result

def select_06():
    """
    -- Знайти список студентів у групі з id=1
    SELECT s.id, s.fullname
    FROM students s
    WHERE s.group_id = 1
    order by s.fullname;
    """
    stmt = select(Student.id, Student.fullname).where(Student.group_id == 1).order_by(Student.fullname)
    result = session.execute(stmt).all()
    return result

def select_07():
    """
    -- Знайти оцінки студентів у групі з id=1 з предмета з id=4
    SELECT s.id, s.fullname, g.grade
    FROM students s
    JOIN grades g ON s.id = g.student_id
    WHERE s.group_id = 1 AND g.subject_id = 4;
    """
    stmt = select(Student.id, Student.fullname, Grade.grade).join(Grade)\
                  .where(and_(Student.group_id == 1, Grade.subject_id == 4))
    result = session.execute(stmt).all()
    return result

def select_08():
    """
    -- Знайти середній бал, який ставить викладач з id=1 зі своїх предметів
    SELECT ROUND(AVG(g.grade), 2) AS average_grade
    FROM grades g
    JOIN subjects s ON g.subject_id = s.id
    WHERE s.teacher_id = 1;
    """
    stmt = select(func.round(func.avg(Grade.grade), 2).label('avarage_grade'))\
                  .join(Subject).where(Subject.teacher_id == 1)
    result = session.execute(stmt).one()
    return result

def select_09():
    """
    -- Знайти список курсів, які відвідує студент з id=1
    SELECT distinct s.id, s.name
    FROM subjects s
    JOIN grades g ON s.id = g.subject_id
    WHERE g.student_id = 1
    order by s.id;
    """
    stmt = select(Subject.id, Subject.name).distinct().join(Grade).where(Grade.student_id == 1).order_by(Subject.id)
    result = session.execute(stmt).all()
    return result

def select_10():
    """
    -- Список курсів, які студенту з id=10 читає викладач з id=1
    SELECT sub.id, sub.name
    FROM subjects sub
    JOIN grades g ON sub.id = g.subject_id
    WHERE g.student_id = 10 AND sub.teacher_id = 1
    GROUP BY sub.id;
    """
    stmt = select(Subject.id, Subject.name).join(Grade)\
                  .where(and_(Grade.student_id == 10, Subject.teacher_id == 1)).group_by(Subject.id)
    result = session.execute(stmt).all()
    return result

# print(select_10())
