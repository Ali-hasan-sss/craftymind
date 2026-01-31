# نشر CraftyMind على Render

**لا تحتاج إلى Docker.** Render يدعم تطبيقات Flask مباشرة.

## ما تم إعداده في المشروع

- دعم متغيرات البيئة: `DATABASE_URL`, `SECRET_KEY`, `PORT`
- إضافة **gunicorn** كخادم إنتاج
- ملف **render.yaml** للإعداد التلقائي (اختياري)

---

## الطريقة 1: النشر من لوحة Render (مُوصى بها)

1. **ادفع المشروع إلى GitHub**
   - أنشئ مستودعاً (repository) وادفع المشروع إليه.

2. **سجّل الدخول إلى Render**
   - ادخل إلى [render.com](https://render.com) وسجّل الدخول (أو أنشئ حساباً).

3. **إنشاء Web Service**
   - من لوحة التحكم: **New** → **Web Service**
   - اختر المستودع (مثلاً `craftymind`) وربط الفرع (مثلاً `main`).

4. **إعدادات الخدمة**
   - **Name:** `craftymind` (أو أي اسم تريده)
   - **Region:** اختر الأقرب لك (مثل Frankfurt أو Oregon)
   - **Runtime:** Python 3
   - **Build Command:**  
     `pip install -r requirements.txt`
   - **Start Command:**  
     `gunicorn app:app --bind 0.0.0.0:$PORT`

5. **متغيرات البيئة (Environment Variables)**
   - **SECRET_KEY:** اضغط **Generate** لإنشاء مفتاح عشوائي (مهم للأمان)
   - (اختياري) إذا أضفت قاعدة بيانات PostgreSQL من Render، أضف **DATABASE_URL** واربطها بقاعدة البيانات.

6. **Create Web Service**
   - اضغط **Create Web Service** وانتظر انتهاء البناء والتشغيل.
   - بعد النجاح، الرابط سيكون مثل: `https://craftymind.onrender.com`

---

## الطريقة 2: استخدام render.yaml (Blueprint)

إذا أردت نشراً تلقائياً من الملف:

1. تأكد أن **render.yaml** موجود في جذر المشروع ومرفع إلى GitHub.
2. في Render: **New** → **Blueprint**
3. اختر المستودع؛ Render سيقرأ **render.yaml** وينشئ الخدمة حسبه.
4. يمكنك بعد ذلك إضافة **SECRET_KEY** (وإنشاءه من لوحة Render) وإضافة **DATABASE_URL** إذا استخدمت PostgreSQL.

---

## ملاحظات مهمة

### صور المنتجات والتصنيفات
- تأكد أن مجلدات **static/images/categories/** و **static/images/products/** ومحتوياتها **مضافة إلى Git** ومرفوعة إلى المستودع.
- إذا كانت الصور تعيد 404 على Render: التطبيق يخدم الصور عبر `/media/category/<id>` و `/media/product/<id>` (بدون أحرف عربية في الرابط). تأكد أن الملفات موجودة في المستودع وأن أسماء الملفات في قاعدة البيانات تطابق الملفات على القرص (مثلاً: `images/categories/خياطة.jpg`).

### قاعدة البيانات
- **بدون إعداد قاعدة بيانات:** التطبيق يستخدم SQLite. على الخطة المجانية من Render القرص مؤقت (ephemeral)، أي أن أي بيانات يُدخلها المستخدمون قد تُفقد عند إعادة النشر أو إعادة التشغيل. مناسب للتجربة والعرض.
- **لحفظ البيانات بشكل دائم:** أنشئ **PostgreSQL** من Render (خطة مجانية متوفرة)، ثم أضف متغير **DATABASE_URL** في إعدادات الخدمة واربطه بقاعدة البيانات. التطبيق مضبوط لاستخدام `DATABASE_URL` تلقائياً إن وُجد.

### إيقاف الخدمة على الخطة المجانية
- على الخطة المجانية، الخدمة قد “تنام” بعد فترة عدم استخدام؛ الطلب الأول بعد ذلك قد يستغرق وقتاً أطول حتى يعود التشغيل.

---

## هل تحتاج Docker؟

**لا.** نشر Flask على Render يتم عادةً بدون Docker عن طريق:
- **Build:** `pip install -r requirements.txt`
- **Start:** `gunicorn app:app --bind 0.0.0.0:$PORT`

يمكنك استخدام Docker لاحقاً إذا احتجت بيئة أو إعدادات خاصة جداً، لكن للنشر العادي لا يلزم.
