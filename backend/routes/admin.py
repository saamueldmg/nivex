from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash

from backend.extensions import db
from backend.models import Grade, Student, ClassroomRule, StudentChange, XPActivity
from .utils import generate_students_for_grade


admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def recalculate_level(student):
    if student.xp >= 5000:
        student.level = 5
    elif student.xp >= 4000:
        student.level = 4
    elif student.xp >= 3000:
        student.level = 3
    else:
        student.level = 2


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


@admin_bp.route("/dashboard")
def dashboard():
    grades = Grade.query.all()
    ordered = sorted(grades, key=lambda g: _grade_sort_key(g.name))

    grade_cards = []
    for grade in ordered:
        grade_cards.append(
            {
                "id": grade.id,
                "name": grade.name,
                "count": len(grade.students),
                "is_public": grade.is_public,
            }
        )

    return render_template("admin/dashboard.html", grades=grade_cards)


@admin_bp.route("/grades/<int:grade_id>/toggle-public", methods=["POST"])
def toggle_grade_public(grade_id):
    grade = db.get_or_404(Grade, grade_id)

    grade.is_public = not grade.is_public
    db.session.commit()

    if grade.is_public:
        flash(f"El grado {grade.name} ahora es visible en el portal público.", "success")
    else:
        flash(f"El grado {grade.name} ya no es visible en el portal público.", "info")

    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/rules")
def rules():
    rules = ClassroomRule.query.order_by(ClassroomRule.id.desc()).all()
    return render_template("admin/rules.html", rules=rules)


@admin_bp.route("/rules/save", methods=["POST"])
def save_rule():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    life_penalty_raw = request.form.get("life_penalty", "0").strip()

    try:
        life_penalty = int(life_penalty_raw)
    except ValueError:
        life_penalty = 0

    if not title:
        flash("Debes escribir el título de la norma.", "error")
        return redirect(url_for("admin.rules"))

    if life_penalty <= 0:
        flash("La vida que resta debe ser un número mayor a 0.", "error")
        return redirect(url_for("admin.rules"))

    now = datetime.utcnow()

    new_rule = ClassroomRule(
        title=title,
        description=description if description else None,
        life_penalty=life_penalty,
        created_at=now,
        updated_at=now,
    )

    db.session.add(new_rule)
    db.session.commit()

    flash("Norma registrada correctamente.", "success")
    return redirect(url_for("admin.rules"))


@admin_bp.route("/rules/<int:rule_id>/update", methods=["POST"])
def update_rule(rule_id):
    rule = db.get_or_404(ClassroomRule, rule_id)

    title = request.form.get("title", "").strip()
    life_penalty_raw = request.form.get("life_penalty", "0").strip()

    try:
        life_penalty = int(life_penalty_raw)
    except ValueError:
        life_penalty = 0

    if not title:
        flash("El título de la norma no puede estar vacío.", "error")
        return redirect(url_for("admin.rules"))

    if life_penalty <= 0:
        flash("La penalización de vida debe ser mayor a 0.", "error")
        return redirect(url_for("admin.rules"))

    rule.title = title
    rule.life_penalty = life_penalty
    rule.updated_at = datetime.utcnow()

    db.session.commit()

    flash("Norma actualizada correctamente.", "success")
    return redirect(url_for("admin.rules"))


@admin_bp.route("/rules/delete/<int:rule_id>", methods=["POST"])
def delete_rule(rule_id):
    rule = db.get_or_404(ClassroomRule, rule_id)

    db.session.delete(rule)
    db.session.commit()

    flash("Norma eliminada correctamente.", "success")
    return redirect(url_for("admin.rules"))


@admin_bp.route("/grades/create", methods=["POST"])
def create_grade():
    grade_name = request.form.get("grade_name", "").strip()
    count_raw = request.form.get("count", "0").strip()
    initial_level_raw = request.form.get("initial_level", "1").strip()
    initial_xp_raw = request.form.get("initial_xp", "0").strip()
    initial_coins_raw = request.form.get("initial_coins", "0").strip()
    initial_life_raw = request.form.get("initial_life", "100").strip()

    try:
        count = int(count_raw)
    except ValueError:
        count = 0

    try:
        initial_level = int(initial_level_raw)
    except ValueError:
        initial_level = 1

    try:
        initial_xp = int(initial_xp_raw)
    except ValueError:
        initial_xp = 0

    try:
        initial_coins = int(initial_coins_raw)
    except ValueError:
        initial_coins = 0

    try:
        initial_life = int(initial_life_raw)
    except ValueError:
        initial_life = 100

    if not grade_name or count <= 0 or initial_level <= 0 or initial_xp < 0 or initial_coins < 0 or initial_life <= 0:
        flash("Verifica los datos del grado antes de crearlo.", "error")
        return redirect(url_for("admin.dashboard"))

    existing_grade = Grade.query.filter_by(name=grade_name).first()
    if existing_grade:
        flash("Ya existe un grado con ese nombre.", "warning")
        return redirect(url_for("admin.dashboard"))

    new_grade = Grade(
        name=grade_name,
        max_students=count,
        is_public=False
    )
    db.session.add(new_grade)
    db.session.flush()

    generated_students = generate_students_for_grade(grade_name, count)

    for student_data in generated_students:
        student = Student(
            full_name=student_data["name"],
            grade_id=new_grade.id,
            life=initial_life,
            xp=initial_xp,
            coins=initial_coins,
            level=initial_level,
            is_dead=False,
            life_reason=None,
            pc_number=None,
        )
        db.session.add(student)

    db.session.commit()

    flash(f"Grado {grade_name} creado correctamente.", "success")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/grades/delete/<string:grade_name>", methods=["POST"])
def delete_grade(grade_name):
    grade = Grade.query.filter_by(name=grade_name).first()

    if not grade:
        flash("El grado no existe.", "error")
        return redirect(url_for("admin.dashboard"))

    students = Student.query.filter_by(grade_id=grade.id).all()
    for student in students:
        db.session.delete(student)

    db.session.delete(grade)
    db.session.commit()

    flash(f"Grado {grade_name} eliminado correctamente.", "success")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/grades/<int:grade_id>/students")
def grade_students(grade_id):
    grade = db.get_or_404(Grade, grade_id)

    students = (
        Student.query
        .filter_by(grade_id=grade.id)
        .order_by(Student.full_name.asc())
        .all()
    )

    rules = ClassroomRule.query.order_by(ClassroomRule.title.asc()).all()
    xp_activities = XPActivity.query.order_by(XPActivity.title.asc()).all()
    xp_modal_open = request.args.get("xp_modal") == "1"

    return render_template(
        "admin/students.html",
        grade=grade,
        students=students,
        rules=rules,
        xp_activities=xp_activities,
        xp_modal_open=xp_modal_open,
    )


@admin_bp.route("/students/<int:student_id>/update", methods=["POST"])
def update_student(student_id):
    student = db.get_or_404(Student, student_id)

    full_name = request.form.get("full_name", "").strip()
    pc_number = request.form.get("pc_number", "").strip()

    if not full_name:
        flash("El nombre del estudiante no puede estar vacío.", "error")
        return redirect(url_for("admin.grade_students", grade_id=student.grade_id))

    student.full_name = full_name
    student.pc_number = pc_number if pc_number else None

    db.session.commit()

    flash(f"Datos actualizados para {student.full_name}.", "success")
    return redirect(url_for("admin.grade_students", grade_id=student.grade_id))


@admin_bp.route("/xp-activities/create", methods=["POST"])
def create_xp_activity():
    title = request.form.get("title", "").strip()
    xp_amount_raw = request.form.get("xp_amount", "0").strip()
    grade_id = request.form.get("grade_id", type=int)

    try:
        xp_amount = int(xp_amount_raw)
    except ValueError:
        xp_amount = 0

    if not grade_id:
        flash("No se pudo identificar el grado.", "error")
        return redirect(url_for("admin.dashboard"))

    if not title or xp_amount <= 0:
        flash("Debes ingresar un título y una cantidad de XP válida.", "error")
        return redirect(url_for("admin.grade_students", grade_id=grade_id, xp_modal=1))

    activity = XPActivity(
        title=title,
        description=None,
        xp_amount=xp_amount,
    )
    db.session.add(activity)
    db.session.commit()

    flash("Actividad XP creada correctamente.", "success")
    return redirect(url_for("admin.grade_students", grade_id=grade_id, xp_modal=1))


@admin_bp.route("/xp-activities/<int:activity_id>/update", methods=["POST"])
def update_xp_activity(activity_id):
    activity = db.get_or_404(XPActivity, activity_id)

    title = request.form.get("title", "").strip()
    xp_amount_raw = request.form.get("xp_amount", "0").strip()
    grade_id = request.form.get("grade_id", type=int)

    try:
        xp_amount = int(xp_amount_raw)
    except ValueError:
        xp_amount = 0

    if not grade_id:
        flash("No se pudo identificar el grado.", "error")
        return redirect(url_for("admin.dashboard"))

    if not title or xp_amount <= 0:
        flash("Debes ingresar datos válidos para actualizar la actividad.", "error")
        return redirect(url_for("admin.grade_students", grade_id=grade_id, xp_modal=1))

    activity.title = title
    activity.xp_amount = xp_amount

    db.session.commit()

    flash("Actividad XP actualizada correctamente.", "success")
    return redirect(url_for("admin.grade_students", grade_id=grade_id, xp_modal=1))


@admin_bp.route("/xp-activities/<int:activity_id>/delete", methods=["POST"])
def delete_xp_activity(activity_id):
    activity = db.get_or_404(XPActivity, activity_id)
    grade_id = request.form.get("grade_id", type=int)

    if not grade_id:
        flash("No se pudo identificar el grado.", "error")
        return redirect(url_for("admin.dashboard"))

    db.session.delete(activity)
    db.session.commit()

    flash("Actividad XP eliminada correctamente.", "success")
    return redirect(url_for("admin.grade_students", grade_id=grade_id, xp_modal=1))


@admin_bp.route("/grades/<int:grade_id>/xp-activities/apply", methods=["POST"])
def apply_xp_activity_bulk(grade_id):
    grade = db.get_or_404(Grade, grade_id)
    student_ids_raw = request.form.getlist("student_ids")
    xp_activity_id = request.form.get("xp_activity_id", type=int)

    if not student_ids_raw or not xp_activity_id:
        flash("Debes seleccionar al menos un estudiante y una actividad XP.", "warning")
        return redirect(url_for("admin.grade_students", grade_id=grade.id))

    activity = db.session.get(XPActivity, xp_activity_id)
    if not activity:
        flash("La actividad XP seleccionada no existe.", "error")
        return redirect(url_for("admin.grade_students", grade_id=grade.id))

    try:
        student_ids = [int(student_id) for student_id in student_ids_raw]
    except ValueError:
        flash("La selección de estudiantes no es válida.", "error")
        return redirect(url_for("admin.grade_students", grade_id=grade.id))

    students = Student.query.filter(
        Student.grade_id == grade.id,
        Student.id.in_(student_ids),
    ).all()

    if not students:
        flash("No se encontraron estudiantes válidos para aplicar la actividad.", "warning")
        return redirect(url_for("admin.grade_students", grade_id=grade.id))

    for student in students:
        student.xp += activity.xp_amount
        recalculate_level(student)

        db.session.add(
            StudentChange(
                student_id=student.id,
                type="XP",
                amount=activity.xp_amount,
                reason=activity.title,
            )
        )

    db.session.commit()

    flash(f"Actividad {activity.title} aplicada a {len(students)} estudiantes.", "success")
    return redirect(url_for("admin.grade_students", grade_id=grade.id))


@admin_bp.route("/students/<int:student_id>/apply_rule", methods=["POST"])
def apply_rule(student_id):
    student = db.get_or_404(Student, student_id)

    rule_id_raw = request.form.get("rule_id", "").strip()
    coins_delta_raw = request.form.get("coins_delta", "0").strip()

    rule = None
    if rule_id_raw:
        try:
            rule_id = int(rule_id_raw)
            rule = db.session.get(ClassroomRule, rule_id)
        except ValueError:
            rule = None

    try:
        coins_delta = int(coins_delta_raw) if coins_delta_raw else 0
    except ValueError:
        coins_delta = 0

    if not rule and coins_delta == 0:
        flash("No se aplicó ningún cambio al estudiante.", "warning")
        return redirect(url_for("admin.grade_students", grade_id=student.grade_id))

    if rule:
        new_life = student.life - rule.life_penalty

        if new_life <= 0:
            student.life = 0
            student.is_dead = True
            student.life_reason = "Debe revivir"
        else:
            student.life = new_life
            student.is_dead = False
            student.life_reason = rule.title

        db.session.add(
            StudentChange(
                student_id=student.id,
                type="Vida",
                amount=-rule.life_penalty,
                reason=rule.title,
            )
        )

    if coins_delta != 0:
        student.coins = max(0, student.coins + coins_delta)

        db.session.add(
            StudentChange(
                student_id=student.id,
                type="Monedas",
                amount=coins_delta,
                reason="Ajuste manual de monedas",
            )
        )

    recalculate_level(student)
    db.session.commit()

    flash(f"Cambios aplicados a {student.full_name}.", "success")
    return redirect(url_for("admin.grade_students", grade_id=student.grade_id))


@admin_bp.route("/grades/<int:grade_id>/reset-demo", methods=["POST"])
def reset_grade_demo(grade_id):
    grade = db.get_or_404(Grade, grade_id)
    students = Student.query.filter_by(grade_id=grade.id).all()

    if not students:
        flash("No hay estudiantes para reiniciar en este grado.", "warning")
        return redirect(url_for("admin.grade_students", grade_id=grade.id))

    student_ids = [student.id for student in students]

    if student_ids:
        StudentChange.query.filter(
            StudentChange.student_id.in_(student_ids)
        ).delete(synchronize_session=False)

    for student in students:
        student.life = 100
        student.xp = 0
        student.coins = 0
        student.level = 2
        student.is_dead = False
        student.life_reason = None

    db.session.commit()

    flash(
        f"Se reinició completamente el grado {grade.name}: vida 100, XP 0 y monedas 0.",
        "success"
    )
    return redirect(url_for("admin.grade_students", grade_id=grade.id))


@admin_bp.route("/students/<int:student_id>/revive", methods=["POST"])
def revive_student(student_id):
    student = db.get_or_404(Student, student_id)

    student.life = 100
    student.is_dead = False
    student.life_reason = "Revivido por el administrador"

    db.session.add(
        StudentChange(
            student_id=student.id,
            type="Vida",
            amount=100,
            reason="Revivido por el administrador",
        )
    )

    db.session.commit()

    flash(f"{student.full_name} fue revivido correctamente.", "success")
    return redirect(url_for("admin.grade_students", grade_id=student.grade_id))