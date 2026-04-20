from flask import Blueprint, render_template, abort
from models import Grade, Student

public_bp = Blueprint("public", __name__)


def _safe_change_type(change):
    for attr in ("type", "change_type", "category", "kind"):
        value = getattr(change, attr, None)
        if value:
            return str(value)
    return "Movimiento"


def _safe_change_reason(change):
    for attr in ("reason", "description", "detail", "note"):
        value = getattr(change, attr, None)
        if value:
            return str(value)
    return "Sin descripción"


def _safe_change_amount(change):
    for attr in ("amount", "value", "delta", "points"):
        value = getattr(change, attr, None)
        if value is not None:
            return value
    return 0


def _safe_change_date(change):
    for attr in ("created_at", "timestamp", "date"):
        value = getattr(change, attr, None)
        if value is not None:
            return value
    return None


def _format_amount(change_type, raw_amount):
    try:
        amount = int(raw_amount)
    except (TypeError, ValueError):
        return str(raw_amount)

    suffix_map = {
        "vida": "de vida",
        "xp": "de XP",
        "monedas": "de monedas",
    }
    suffix = suffix_map.get(str(change_type).strip().lower(), "")
    return f"{amount:+d} {suffix}".strip()


def _serialize_changes(student):
    raw_changes = list(getattr(student, "changes", []) or [])
    raw_changes.sort(
        key=lambda change: (
            _safe_change_date(change) is None,
            _safe_change_date(change),
            getattr(change, "id", 0),
        )
    )

    serialized = []
    for change in raw_changes:
        change_type = _safe_change_type(change)
        raw_amount = _safe_change_amount(change)

        try:
            amount_value = int(raw_amount)
        except (TypeError, ValueError):
            amount_value = 0

        serialized.append(
            {
                "type": change_type,
                "amount": _format_amount(change_type, amount_value),
                "amount_value": amount_value,
                "reason": _safe_change_reason(change),
                "created_at": _safe_change_date(change),
            }
        )
    return serialized


def _grade_sort_key(grade_name: str):
    txt = grade_name.strip()

    if "-" in txt:
        base, group = txt.split("-", 1)
    else:
        base, group = txt, "0"

    try:
        base_num = int(base)
    except ValueError:
        base_num = 999

    try:
        group_num = int(group)
    except ValueError:
        group_num = 999

    return (base_num, group_num, txt.lower())


@public_bp.route("/")
def home():
    grades = Grade.query.filter_by(is_public=True).all()
    ordered = sorted(grades, key=lambda g: _grade_sort_key(g.name))

    grade_cards = []
    for grade in ordered:
        grade_cards.append(
            {
                "name": grade.name,
                "count": len(grade.students),
            }
        )

    return render_template("public/home.html", grades=grade_cards)


@public_bp.route("/grades/<grade_name>")
def grade_detail(grade_name):
    grade = Grade.query.filter_by(name=grade_name, is_public=True).first()

    if grade is None:
        abort(404)

    students = []
    ordered_students = sorted(grade.students, key=lambda s: s.id)

    for index, student in enumerate(ordered_students, start=1):
        students.append(
            {
                "id": student.id,
                "name": student.full_name,
                "grade": grade.name,
                "avatar": f"avatar_{((index - 1) % 5) + 1:02}.png",
                "level": student.level,
                "xp": student.xp,
                "coins": student.coins,
                "life": student.life,
                "pc_number": student.pc_number,
            }
        )

    return render_template(
        "public/grade_detail.html",
        grade_name=grade.name,
        students=students
    )


@public_bp.route("/grades/<grade_name>/students/<int:student_id>")
def student_detail(grade_name, student_id):
    grade = Grade.query.filter_by(name=grade_name, is_public=True).first()

    if grade is None:
        abort(404)

    student = Student.query.filter_by(id=student_id, grade_id=grade.id).first()

    if student is None:
        abort(404)

    ordered_students = sorted(grade.students, key=lambda s: s.id)
    avatar_name = "avatar_01.png"

    for index, current_student in enumerate(ordered_students, start=1):
        if current_student.id == student.id:
            avatar_name = f"avatar_{((index - 1) % 5) + 1:02}.png"
            break

    student_data = {
        "id": student.id,
        "name": student.full_name,
        "grade": grade.name,
        "avatar": avatar_name,
        "level": student.level,
        "xp": student.xp,
        "coins": student.coins,
        "life": student.life,
        "pc_number": student.pc_number,
        "is_dead": student.is_dead,
        "life_reason": student.life_reason,
        "changes": _serialize_changes(student),
    }

    return render_template(
        "public/student_detail.html",
        grade_name=grade.name,
        student=student_data
    )