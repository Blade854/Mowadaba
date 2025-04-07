#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
وحدة التحكم في التلاميذ لنظام إدارة المدرسة
"""

import os
import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import or_

from models.database import Student, Session as DBSession

class StudentController:
    """وحدة التحكم في التلاميذ"""
    
    @staticmethod
    def get_all_students():
        """الحصول على جميع التلاميذ"""
        session = DBSession()
        try:
            students = session.query(Student).all()
            return students
        except Exception as e:
            print(f"خطأ في الحصول على التلاميذ: {e}")
            return []
        finally:
            session.close()
    
    @staticmethod
    def get_student_by_id(student_id):
        """الحصول على تلميذ حسب الرقم التعريفي"""
        session = DBSession()
        try:
            student = session.query(Student).filter_by(student_id=student_id).first()
            return student
        except Exception as e:
            print(f"خطأ في الحصول على التلميذ: {e}")
            return None
        finally:
            session.close()
    
    @staticmethod
    def search_students(search_text):
        """البحث عن التلاميذ"""
        session = DBSession()
        try:
            students = session.query(Student).filter(
                or_(
                    Student.student_id.like(f"%{search_text}%"),
                    Student.first_name.like(f"%{search_text}%"),
                    Student.last_name.like(f"%{search_text}%")
                )
            ).all()
            return students
        except Exception as e:
            print(f"خطأ في البحث عن التلاميذ: {e}")
            return []
        finally:
            session.close()
    
    @staticmethod
    def add_student(student_data):
        """إضافة تلميذ جديد"""
        session = DBSession()
        try:
            # التحقق من وجود التلميذ
            existing_student = session.query(Student).filter_by(student_id=student_data["student_id"]).first()
            if existing_student:
                return False, "التلميذ موجود بالفعل"
            
            # إنشاء كائن التلميذ
            student = Student(
                student_id=student_data["student_id"],
                last_name=student_data["last_name"],
                first_name=student_data["first_name"],
                gender=student_data["gender"],
                birth_date=student_data["birth_date"],
                birth_judgment=student_data.get("birth_judgment"),
                birth_certificate_type=student_data.get("birth_certificate_type"),
                registration_year=student_data.get("registration_year"),
                birth_certificate_number=student_data.get("birth_certificate_number"),
                birth_place=student_data.get("birth_place"),
                academic_year=student_data.get("academic_year"),
                section=student_data.get("section"),
                class_number=student_data.get("class_number"),
                study_system=student_data.get("study_system"),
                registration_number=student_data.get("registration_number"),
                registration_date=student_data.get("registration_date")
            )
            
            # إضافة التلميذ إلى قاعدة البيانات
            session.add(student)
            session.commit()
            return True, "تم إضافة التلميذ بنجاح"
        except Exception as e:
            session.rollback()
            print(f"خطأ في إضافة التلميذ: {e}")
            return False, f"خطأ في إضافة التلميذ: {str(e)}"
        finally:
            session.close()
    
    @staticmethod
    def update_student(student_id, student_data):
        """تحديث بيانات تلميذ"""
        session = DBSession()
        try:
            # الحصول على التلميذ
            student = session.query(Student).filter_by(student_id=student_id).first()
            if not student:
                return False, "التلميذ غير موجود"
            
            # تحديث بيانات التلميذ
            student.last_name = student_data["last_name"]
            student.first_name = student_data["first_name"]
            student.gender = student_data["gender"]
            student.birth_date = student_data["birth_date"]
            
            if "birth_judgment" in student_data:
                student.birth_judgment = student_data["birth_judgment"]
            if "birth_certificate_type" in student_data:
                student.birth_certificate_type = student_data["birth_certificate_type"]
            if "registration_year" in student_data:
                student.registration_year = student_data["registration_year"]
            if "birth_certificate_number" in student_data:
                student.birth_certificate_number = student_data["birth_certificate_number"]
            if "birth_place" in student_data:
                student.birth_place = student_data["birth_place"]
            if "academic_year" in student_data:
                student.academic_year = student_data["academic_year"]
            if "section" in student_data:
                student.section = student_data["section"]
            if "class_number" in student_data:
                student.class_number = student_data["class_number"]
            if "study_system" in student_data:
                student.study_system = student_data["study_system"]
            if "registration_number" in student_data:
                student.registration_number = student_data["registration_number"]
            if "registration_date" in student_data:
                student.registration_date = student_data["registration_date"]
            
            # حفظ التغييرات
            session.commit()
            return True, "تم تحديث بيانات التلميذ بنجاح"
        except Exception as e:
            session.rollback()
            print(f"خطأ في تحديث بيانات التلميذ: {e}")
            return False, f"خطأ في تحديث بيانات التلميذ: {str(e)}"
        finally:
            session.close()
    
    @staticmethod
    def delete_student(student_id):
        """حذف تلميذ"""
        session = DBSession()
        try:
            # الحصول على التلميذ
            student = session.query(Student).filter_by(student_id=student_id).first()
            if not student:
                return False, "التلميذ غير موجود"
            
            # حذف التلميذ
            session.delete(student)
            session.commit()
            return True, "تم حذف التلميذ بنجاح"
        except Exception as e:
            session.rollback()
            print(f"خطأ في حذف التلميذ: {e}")
            return False, f"خطأ في حذف التلميذ: {str(e)}"
        finally:
            session.close()
    
    @staticmethod
    def import_students_from_file(file_path, column_mapping):
        """استيراد التلاميذ من ملف"""
        try:
            # قراءة الملف
            if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
                df = pd.read_excel(file_path)
            elif file_path.endswith('.html') or file_path.endswith('.htm'):
                df = pd.read_html(file_path)[0]
            else:
                return False, "نوع الملف غير مدعوم"
            
            # تعيين الأعمدة
            mapped_df = pd.DataFrame()
            for db_col, file_col in column_mapping.items():
                if file_col in df.columns:
                    mapped_df[db_col] = df[file_col]
            
            # التحقق من وجود الأعمدة الإلزامية
            required_columns = ["student_id", "last_name", "first_name", "gender", "birth_date"]
            for col in required_columns:
                if col not in mapped_df.columns:
                    return False, f"العمود الإلزامي {col} غير موجود في الملف"
            
            # إضافة التلاميذ إلى قاعدة البيانات
            session = DBSession()
            try:
                success_count = 0
                error_count = 0
                
                for _, row in mapped_df.iterrows():
                    # التحقق من وجود التلميذ
                    student_id = str(row["student_id"])
                    existing_student = session.query(Student).filter_by(student_id=student_id).first()
                    
                    if existing_student:
                        # تحديث بيانات التلميذ
                        for col in mapped_df.columns:
                            if col != "student_id" and not pd.isna(row[col]):
                                setattr(existing_student, col, row[col])
                        success_count += 1
                    else:
                        # إنشاء تلميذ جديد
                        student_data = {}
                        for col in mapped_df.columns:
                            if not pd.isna(row[col]):
                                student_data[col] = row[col]
                        
                        # التحقق من وجود البيانات الإلزامية
                        if all(col in student_data for col in required_columns):
                            student = Student(**student_data)
                            session.add(student)
                            success_count += 1
                        else:
                            error_count += 1
                
                session.commit()
                return True, f"تم استيراد {success_count} تلميذ بنجاح، {error_count} تلميذ لم يتم استيراده"
            except Exception as e:
                session.rollback()
                print(f"خطأ في استيراد التلاميذ: {e}")
                return False, f"خطأ في استيراد التلاميذ: {str(e)}"
            finally:
                session.close()
        except Exception as e:
            print(f"خطأ في قراءة الملف: {e}")
            return False, f"خطأ في قراءة الملف: {str(e)}"
