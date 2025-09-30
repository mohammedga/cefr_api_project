# backend/routes.py
from flask import Blueprint, request, jsonify
from sqlalchemy import select
from .database import get_db
from .models import Story

bp = Blueprint("api", __name__, url_prefix="/api")

@bp.get("/health")
def health():
    return {"status": "ok"}

@bp.get("/stories")
def list_stories():
    db = next(get_db())
    rows = db.execute(select(Story)).scalars().all()
    res = []
    for s in rows:
        res.append({
            "id": s.id,
            "title": s.title,
            "level": s.level,
            "minutes": s.minutes,
            "text": s.text,
            "ar": s.ar or [],
            "vocab": s.vocab or [],
            "quiz": s.quiz or []
        })
    return jsonify(res)

@bp.get("/stories/<int:story_id>")
def get_story(story_id):
    db = next(get_db())
    st = db.get(Story, story_id)
    if not st:
        return jsonify({"error":"not found"}), 404
    return jsonify({
        "id": st.id,
        "title": st.title,
        "level": st.level,
        "minutes": st.minutes,
        "text": st.text,
        "ar": st.ar or [],
        "vocab": st.vocab or [],
        "quiz": st.quiz or []
    })

@bp.post("/stories")
def create_story():
    data = request.get_json() or {}
    if not data.get("title") or not data.get("text"):
        return jsonify({"error":"title and text required"}), 400
    db = next(get_db())
    st = Story(
        title=data.get("title"),
        level=data.get("level"),
        minutes=data.get("minutes") or 3,
        text=data.get("text"),
        ar=data.get("ar") or [],
        vocab=data.get("vocab") or [],
        quiz=data.get("quiz") or []
    )
    db.add(st)
    db.commit()
    db.refresh(st)
    return jsonify({"id": st.id}), 201

@bp.put("/stories/<int:story_id>")
def update_story(story_id):
    data = request.get_json() or {}
    db = next(get_db())
    st = db.get(Story, story_id)
    if not st: return jsonify({"error":"not found"}), 404
    st.title = data.get("title", st.title)
    st.level = data.get("level", st.level)
    st.minutes = data.get("minutes", st.minutes)
    st.text = data.get("text", st.text)
    st.ar = data.get("ar", st.ar)
    st.vocab = data.get("vocab", st.vocab)
    st.quiz = data.get("quiz", st.quiz)
    db.commit()
    return jsonify({"status":"ok"})

@bp.delete("/stories/<int:story_id>")
def delete_story(story_id):
    db = next(get_db())
    st = db.get(Story, story_id)
    if not st: return jsonify({"error":"not found"}), 404
    db.delete(st)
    db.commit()
    return jsonify({"status":"deleted"})
