#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
سكريبت اختبار استيراد البيانات من ملفات Excel
"""

import os
import sys
import unittest
import pandas as pd

# إضافة مسار المشروع إلى مسار البحث
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.database import init_db, Student, Session as DBSession
from controllers.student_controller import StudentController
from utils.helpers import read_excel_file

class TestImportData(unittest.TestCase):
    """اختبار وظائف استيراد البيانات"""
    
    @classmethod
    def setUpClass(cls):
        """إعداد بيئة الاختبار"""
        # تهيئة قاعدة البيانات
        init_db(test=True)
    
    def test_import_students_from_excel(self):
        """اختبار استيراد التلاميذ من ملف Excel"""
        # مسار ملف الاختبار
        file_path = "/home/ubuntu/upload/Eleve (19).xls"
        
        # التحقق من وجود الملف
        self.assertTrue(os.path.exists(file_path), "ملف الاختبار غير موجود")
        
        try:
            # قراءة الملف
            df = read_excel_file(file_path)
            
            # التحقق من قراءة البيانات
            self.assertIsNotNone(df)
            self.assertGreater(len(df), 0)
            
            # تعيين الأعمدة
            column_mapping = {
                "student_id": "رقم التسجيل",
                "last_name": "اللقب",
                "first_name": "الاسم",
                "gender": "الجنس",
                "birth_date": "تاريخ الميلاد",
                "birth_place": "مكان الميلاد",
                "registration_year": "سنة التسجيل"
            }
            
            # استيراد البيانات
            success, message = StudentController.import_students_from_file(file_path, column_mapping)
            
            # التحقق من نجاح الاستيراد
            self.assertTrue(success, f"فشل استيراد البيانات: {message}")
            
            # التحقق من وجود البيانات في قاعدة البيانات
            session = DBSession()
            try:
                students_count = session.query(Student).count()
                self.assertGreater(students_count, 0, "لم يتم استيراد أي تلميذ")
            finally:
                session.close()
                
        except Exception as e:
            self.fail(f"حدث خطأ أثناء اختبار استيراد البيانات: {str(e)}")
    
    def test_column_mapping(self):
        """اختبار تعيين الأعمدة"""
        # مسار ملف الاختبار
        file_path = "/home/ubuntu/upload/Eleve (19).xls"
        
        # التحقق من وجود الملف
        self.assertTrue(os.path.exists(file_path), "ملف الاختبار غير موجود")
        
        try:
            # قراءة الملف
            df = read_excel_file(file_path)
            
            # التحقق من قراءة البيانات
            self.assertIsNotNone(df)
            
            # تعيين الأعمدة بشكل غير صحيح (بدون الأعمدة الإلزامية)
            invalid_column_mapping = {
                "birth_place": "مكان الميلاد",
                "registration_year": "سنة التسجيل"
            }
            
            # محاولة استيراد البيانات
            success, _ = StudentController.import_students_from_file(file_path, invalid_column_mapping)
            
            # التحقق من فشل الاستيراد
            self.assertFalse(success, "تم استيراد البيانات رغم عدم وجود الأعمدة الإلزامية")
            
        except Exception as e:
            self.fail(f"حدث خطأ أثناء اختبار تعيين الأعمدة: {str(e)}")
    
    @classmethod
    def tearDownClass(cls):
        """تنظيف بيئة الاختبار"""
        # حذف بيانات الاختبار
        session = DBSession()
        try:
            # حذف جميع التلاميذ
            session.query(Student).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"خطأ في تنظيف بيانات الاختبار: {e}")
        finally:
            session.close()

if __name__ == "__main__":
    unittest.main()
