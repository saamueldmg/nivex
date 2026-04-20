from datetime import datetime
from extensions import db


class Grade(db.Model):
    __tablename__ = "grades"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    max_students = db.Column(db.Integer, nullable=False, default=0)
    is_public = db.Column(db.Boolean, nullable=False, default=False)

    students = db.relationship(
        "Student",
        backref="grade",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Grade {self.name}>"


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    grade_id = db.Column(db.Integer, db.ForeignKey("grades.id"), nullable=False)

    life = db.Column(db.Integer, nullable=False, default=100)
    xp = db.Column(db.Integer, nullable=False, default=0)
    coins = db.Column(db.Integer, nullable=False, default=0)
    level = db.Column(db.Integer, nullable=False, default=2)

    is_dead = db.Column(db.Boolean, nullable=False, default=False)
    life_reason = db.Column(db.String(255), nullable=True)
    pc_number = db.Column(db.String(50), nullable=True)

    changes = db.relationship(
        "StudentChange",
        backref="student",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Student {self.full_name}>"


class ClassroomRule(db.Model):
    __tablename__ = "classroom_rules"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    life_penalty = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    def __repr__(self):
        return f"<ClassroomRule {self.title}>"


class XPActivity(db.Model):
    __tablename__ = "xp_activities"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False, unique=True)
    xp_amount = db.Column(db.Integer, nullable=False, default=0)
    description = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<XPActivity {self.title} +{self.xp_amount}XP>"


class StudentChange(db.Model):
    __tablename__ = "student_changes"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<StudentChange {self.student_id} {self.type} {self.amount}>"