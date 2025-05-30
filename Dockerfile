# استخدام صورة بايثون الرسمية
FROM python:3.13.3

# تعيين مجلد العمل
WORKDIR /app

# نسخ الملفات إلى داخل الحاوية
COPY . /app

# تنزيل مكتبات المشروع في الحاوية
RUN pip install -r requirements.txt

# تشغيل الكود
CMD ["python", "main.py"]
