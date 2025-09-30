# backend/app.py
from flask import Flask
from flask_cors import CORS
from .database import engine, Base
from .routes import bp as api_bp

# backend/app.py
import os
from flask import Flask, send_from_directory

from database import Base, engine  # موجودة عندك أصلاً
from routes import register_routes  # حسب تنظيمك الحالي

def create_app() -> Flask:
    app = Flask(__name__)

    # إنشاء الجداول
    Base.metadata.create_all(bind=engine)

    # تسجيل الراوتس
    register_routes(app)

    # (اختياري) تقديم واجهة frontend من نفس السيرفر
    STATIC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))

    @app.route("/")
    def root():
        index_path = os.path.join(STATIC_DIR, "index.html")
        if os.path.exists(index_path):
            return send_from_directory(STATIC_DIR, "index.html")
        return {"ok": True, "message": "Backend running."}, 200

    @app.route("/<path:path>")
    def static_files(path):
        full = os.path.join(STATIC_DIR, path)
        if os.path.exists(full):
            return send_from_directory(STATIC_DIR, path)
        # لو الملف غير موجود، رجّع الصفحة الرئيسية (تنفع للواجهات أحادية الصفحة)
        return root()

    return app


# أنشئ التطبيق مرة واحدة على مستوى الموديول
app = create_app()

# شغّل السيرفر بالطريقة الصحيحة لـ Fly.io
if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)

