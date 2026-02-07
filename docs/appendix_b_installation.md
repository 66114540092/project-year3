ภาคผนวก ข 
คู่มือการติดตั้งระบบ

ข.1 การติดตั้งแบบ Docker (แนะนำ)

ข.1.1 Clone โปรเจกต์
git clone https://github.com/username/battlehub.git
cd battlehub

ข.1.2 สร้างไฟล์ Environment
สร้างไฟล์ .env ที่ root ของโปรเจกต์
DEBUG=False
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgres://postgres:password@db:5432/battlehub
ALLOWED_HOSTS=localhost,127.0.0.1,c271a6310f28.ngrok-free.app

ข.1.3 Build และ Run
docker-compose build
docker-compose up -d

ข.1.4 สร้าง Superuser
docker-compose exec web python manage.py createsuperuser

ข.1.5 ตรวจสอบการติดตั้ง
เปิด browser ไปที่ https://c271a6310f28.ngrok-free.app
เข้า Admin ที่ https://c271a6310f28.ngrok-free.app/admin

ข.2 การติดตั้งแบบ Manual (Development)

ข.2.1 สร้าง Virtual Environment
python -m venv venv
venv\Scripts\activate    # Windows
source venv/bin/activate # Linux/Mac

ข.2.2 ติดตั้ง Dependencies
pip install -r requirements.txt

ข.2.3 ตั้งค่า Database
python manage.py migrate
python manage.py createsuperuser

ข.2.4 รัน Development Server
python manage.py runserver

ข.3 การ Migrate Database
หากมีการเปลี่ยนแปลง Models
python manage.py makemigrations
python manage.py migrate

ข.4 การ Collect Static Files (Production)
python manage.py collectstatic --noinput
