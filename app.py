from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

# =======================
# App Config
# =======================
app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# دعم Render: استخدام DATABASE_URL إن وُجد (PostgreSQL)، وإلا SQLite
database_url = os.environ.get('DATABASE_URL')
if database_url:
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'database.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'craftymind-secret-key')

db = SQLAlchemy(app)

# =======================
# Models
# =======================

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    image = db.Column(db.String(200))
    products = db.relationship('Product', backref='category', lazy=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    orders = db.relationship('Order', back_populates='user', lazy=True)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    materials = db.Column(db.String(200))
    image = db.Column(db.String(200))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    orders = db.relationship('Order', back_populates='product', lazy=True)


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)

    # ربط الطلب بالمنتج
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product_name = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Float, nullable=False)

    quantity = db.Column(db.Integer, nullable=False, default=1)
    total_price = db.Column(db.Float, nullable=False)

    order_date = db.Column(db.DateTime, default=datetime.utcnow)

    # ربط الطلب بالمستخدم
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # إضافة عمود الحالة
    status = db.Column(db.String(50), nullable=False, default="في السلة")  

    # علاقات ORM
    product = db.relationship('Product', back_populates='orders')
    user = db.relationship('User', back_populates='orders')

    def __repr__(self):
        return f"<Order {self.id} | {self.product_name} x{self.quantity} | User {self.user_id} | Status {self.status}>"



# =======================
# Default Data
# =======================
def add_default_data():
    if Category.query.first():
        return

    categories = [
        ("خياطة", "/static/images/categories/خياطة.jpg"),
            ("خشب", "/static/images/categories/خشب.jpg"),
            ("خرز", "/static/images/categories/خرز.jpg"),
            ("رسم", "/static/images/categories/رسم.jpg"),
            ("طلاء", "/static/images/categories/طلاء.jpg"),
            ("صابون يدوي", "/static/images/categories/صابون.jpg"),
            ("شموع", "/static/images/categories/شموع.jpg"),
            ("أشغال ورقية", "/static/images/categories/ورق.jpg"),
            ("مجوهرات", "/static/images/categories/مجوهرات.jpg"),
            ("نسيج", "/static/images/categories/نسيج.jpg"),
            ("فخار", "/static/images/categories/فخار.jpg"),
            ("سيراميك", "/static/images/categories/سيراميك.jpg"),
            ("حقائب", "/static/images/categories/حقائب.jpg"),
            ("ملابس", "/static/images/categories/ملابس.jpg"),
            ("إكسسوارات", "/static/images/categories/إكسسوارات.jpg")
    ]

    for c in categories:
        db.session.add(Category(name=c[0], image=c[1]))
    db.session.commit()

    cat = Category.query.all()

    products = [
        ("وسادة مزخرفة", "وسادة قماشية مزخرفة بخيوط متعددة الألوان.", 50, "خيوط، قماش", "/static/images/products/وسادة.jpg", cat[0].id),
            ("حقيبة خشبية صغيرة", "حقيبة خشبية صغيرة للزينة أو التخزين.", 120, "خشب، دهان", "/static/images/products/حقيبة.jpg", cat[1].id),
            ("قلادة خرز ملونة", "قلادة مصنوعة من خرز ملون متنوع.", 30, "خرز، سلك معدني", "/static/images/products/قلادة.jpg", cat[2].id),
            ("لوحة زيتية صغيرة", "لوحة زيتية رائعة للتزيين.", 200, "ألوان زيتية، قماش", "/static/images/products/لوحة.jpg", cat[3].id),
            ("صابون معطر", "صابون طبيعي برائحة الزهور.", 25, "زيوت طبيعية، صودا كاوية", "/static/images/products/صابون.jpg", cat[5].id),
            ("شمعة معطرة", "شمعة يدوية معطرة بألوان متنوعة.", 40, "شمع، عطور", "/static/images/products/شمعة.jpg", cat[6].id),
            ("دفتر أشغال ورقية", "دفتر لتدوين وتصميم أشغال ورقية.", 15, "ورق، غلاف كرتوني", "/static/images/products/دفتر.jpg", cat[7].id),
            ("خاتم فضي", "خاتم فضي أنيق للزينة.", 75, "فضة", "/static/images/products/خاتم.jpg", cat[8].id)
    ]

    for p in products:
        db.session.add(Product(
            name=p[0], description=p[1], price=p[2],
            materials=p[3], image=p[4], category_id=p[5]
        ))

    db.session.commit()

# =======================
# Authentication
# =======================
@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/about')
def about():
    return render_template('about.html')

# =======================
# Add Default Users
# =======================
def add_default_users():
    if User.query.first():  # إذا كان هناك مستخدم موجود بالفعل، لا تضيف
        return

    users = [
        User(username="admin", email="admin@craftymind.com", 
             password=generate_password_hash("123456")),
        User(username="user1", email="user1@example.com", 
             password=generate_password_hash("password")),
        User(username="user2", email="user2@example.com", 
             password=generate_password_hash("password123"))
    ]

    for u in users:
        db.session.add(u)

    db.session.commit()
    print("تم إضافة المستخدمين الافتراضيين")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        # البحث عن المستخدم حسب اسم المستخدم فقط
        user = User.query.filter_by(username=username).first()

        # التحقق من كلمة المرور المشفرة
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('index'))
        else:
            flash("بيانات الدخول غير صحيحة")

    return render_template('login.html')


from werkzeug.security import generate_password_hash

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password'].strip()

        # تشفير كلمة المرور
        hashed_password = generate_password_hash(password)

        user = User(
            username=username,
            email=email,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        flash("تم إنشاء الحساب بنجاح! يمكنك تسجيل الدخول الآن")
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# =======================
# Routes
# =======================
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('welcome'))
    categories = Category.query.all()
    return render_template('categories.html', categories=categories)
@app.route('/add-product', methods=['GET', 'POST'])
def add_product():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    categories = Category.query.all()

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        materials = request.form['materials']
        image = request.form['image']  # رابط الصورة من static
        category_id = int(request.form['category_id'])

        new_product = Product(
            name=name,
            description=description,
            price=price,
            materials=materials,
            image=image,
            category_id=category_id
        )
        db.session.add(new_product)
        db.session.commit()
        flash("تم إضافة العمل بنجاح!")
        return redirect(url_for('index'))

    return render_template('add_product.html', categories=categories)
# =======================
# إضافة منتج إلى السلة
# =======================
@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    product = Product.query.get_or_404(product_id)
    quantity = int(request.form.get('quantity', 1))
    total = product.price * quantity

    # إضافة الطلب إلى جدول Order مع حالة "في السلة"
    order = Order(
        product_id=product.id,
        product_name=product.name,
        price=product.price,
        quantity=quantity,
        total_price=total,
        user_id=session['user_id'],
        status="في السلة"
    )
    db.session.add(order)
    db.session.commit()

    flash(f"تم إضافة {product.name} إلى السلة!")
    return redirect(url_for('my_cart'))


# =======================
# عرض محتويات السلة
# =======================
@app.route('/cart')
def my_cart():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # جميع الطلبات في السلة للمستخدم الحالي
    cart_items = Order.query.filter_by(user_id=session['user_id'], status="في السلة").all()
    total_price = sum(item.total_price for item in cart_items)

    return render_template('cart.html', cart_items=cart_items, total_price=total_price)


# =======================
# تحديث كمية طلب في السلة
# =======================
@app.route('/update_cart/<int:order_id>', methods=['POST'])
def update_cart(order_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    order = Order.query.get_or_404(order_id)

    # التحقق أن الطلب تابع للمستخدم الحالي
    if order.user_id != session['user_id']:
        flash("ليس لديك صلاحية تعديل هذا الطلب!")
        return redirect(url_for('my_cart'))

    quantity = int(request.form.get('quantity', 1))
    order.quantity = quantity
    order.total_price = order.price * quantity

    db.session.commit()
    flash(f"تم تحديث كمية {order.product_name} إلى {quantity}")
    return redirect(url_for('my_cart'))


# =======================
# حذف طلب من السلة
# =======================
@app.route('/remove_from_cart/<int:order_id>', methods=['POST'])
def remove_from_cart(order_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    order = Order.query.get_or_404(order_id)

    if order.user_id != session['user_id']:
        flash("ليس لديك صلاحية حذف هذا الطلب!")
        return redirect(url_for('my_cart'))

    db.session.delete(order)
    db.session.commit()
    flash(f"تم حذف {order.product_name} من السلة")
    return redirect(url_for('my_cart'))


# =======================
# الطلب المباشر (شراء منتج واحد)
# =======================
@app.route('/order/<int:product_id>', methods=['GET', 'POST'])
def order(product_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    product = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        quantity = int(request.form['quantity'])
        total = product.price * quantity

        order = Order(
            product_id=product.id,
            product_name=product.name,
            price=product.price,
            quantity=quantity,
            total_price=total,
            user_id=session['user_id'],
            status="تم الطلب"
        )
        db.session.add(order)
        db.session.commit()

        flash(f"تم طلب {product.name} بنجاح!")
        return redirect(url_for('my_orders'))

    return render_template('order.html', product=product)


# =======================
# عرض جميع الطلبات للمستخدم
# =======================
@app.route('/orders')
def my_orders():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # جميع الطلبات، سواء في السلة أو تم طلبها
    orders = Order.query.filter_by(user_id=session['user_id']).all()
    return render_template('orders.html', orders=orders)


# =======================
# عرض منتجات تصنيف محدد
# =======================
@app.route('/category/<int:id>')
def category_products(id):
    products = Product.query.filter_by(category_id=id).all()
    return render_template('products.html', products=products)
@app.route('/checkout')
def checkout():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # جميع الطلبات في السلة للمستخدم
    cart_items = Order.query.filter_by(user_id=session['user_id'], status="في السلة").all()

    if not cart_items:
        flash("سلة التسوق فارغة!")
        return redirect(url_for('my_cart'))

    # تحويل جميع العناصر في السلة إلى "تم الطلب"
    for item in cart_items:
        item.status = "تم الطلب"
    db.session.commit()

    flash("تم إتمام الطلب بنجاح!")
    return redirect(url_for('my_orders'))


# =======================
# AI Pages
# =======================
@app.route('/ideas', methods=['GET', 'POST'])
def ideas():
    suggestions = []
    if request.method == 'POST':
        from ai_rules import generate_ideas
        materials = request.form['materials'].split(',')
        suggestions = generate_ideas(materials)
    return render_template('ideas.html', suggestions=suggestions)

@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    if request.method == 'POST':
        from ai_rules import chatbot_response
        user_message = request.form.get('message', '')
        bot_reply = chatbot_response(user_message)

        # ✅ إرسال نص فقط بدون HTML كامل
        return bot_reply, 200, {'Content-Type': 'text/plain; charset=utf-8'}

    # GET request يعرض صفحة الدردشة
    return render_template('chatbot.html')



# =======================
# تهيئة DB عند التحميل (يعمل مع gunicorn على Render أيضاً)
# =======================
with app.app_context():
    db.create_all()
    add_default_data()
    add_default_users()

# =======================
# Run App
# =======================
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', debug=True, port=port)

