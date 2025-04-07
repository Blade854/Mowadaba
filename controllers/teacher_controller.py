#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
وحدة التحكم في الأساتذة لنظام إدارة المدرسة
"""

import os
import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import or_

from models.database import Teacher, Session as DBSession

class TeacherController:
    """وحدة التحكم في الأساتذة"""
    
    @staticmethod
    def get_all_teachers():
        """الحصول على جميع الأساتذة"""
        session = DBSession()
        try:
            teachers = session.query(Teacher).all()
            return teachers
        except Exception as e:
            print(f"خطأ في الحصول على الأساتذة: {e}")
            return []
        finally:
            session.close()
    
    @staticmethod
    def get_teacher_by_id(teacher_id):
        """الحصول على أستاذ حسب الرقم التعريفي"""
        session = DBSession()
        try:
            teacher = session.query(Teacher).filter_by(teacher_id=teacher_id).first()
            return teacher
        except Exception as e:
            print(f"خطأ في الحصول على الأستاذ: {e}")
            return None
        finally:
            session.close()
    
    @staticmethod
    def search_teachers(search_text):
        """البحث عن الأساتذة"""
        session = DBSession()
        try:
            teachers = session.query(Teacher).filter(
                or_(
                    Teacher.first_name.like(f"%{search_text}%"),
                    Teacher.last_name.like(f"%{search_text}%"),
                    Teacher.specialization.like(f"%{search_text}%")
                )
            ).all()
            return teachers
        except Exception as e:
            print(f"خطأ في البحث عن الأساتذة: {e}")
            return []
        finally:
            session.close()
    
    @staticmethod
    def add_teacher(teacher_data):
        """إضافة أستاذ جديد"""
        session = DBSession()
        try:
            # إنشاء كائن الأستاذ
            teacher = Teacher(
                last_name=teacher_data["last_name"],
                first_name=teacher_data["first_name"],
                gender=teacher_data["gender"],
                birth_date=teacher_data.get("birth_date"),
                specialization=teacher_data.get("specialization"),
                phone_number=teacher_data.get("phone_number"),
                email=teacher_data.get("email"),
                address=teacher_data.get("address"),
                hire_date=teacher_data.get("hire_date")
            )
            
            # إضافة الأستاذ إلى قاعدة البيانات
            session.add(teacher)
            session.commit()
            return True, "تم إضافة الأستاذ بنجاح"
        except Exception as e:
            session.rollback()
            print(f"خطأ في إضافة الأستاذ: {e}")
            return False, f"خطأ في إضافة الأستاذ: {str(e)}"
        finally:
            session.close()
    
    @staticmethod
    def update_teacher(teacher_id, teacher_data):
        """تحديث بيانات أستاذ"""
        session = DBSession()
        try:
            # الحصول على الأستاذ
            teacher = session.query(Teacher).filter_by(teacher_id=teacher_id).first()
            if not teacher:
                return False, "الأستاذ غير موجود"
            
            # تحديث بيانات الأستاذ
            teacher.last_name = teacher_data["last_name"]
            teacher.first_name = teacher_data["first_name"]
            teacher.gender = teacher_data["gender"]
            
            if "birth_date" in teacher_data:
                teacher.birth_date = teacher_data["birth_date"]
            if "specialization" in teacher_data:
                teacher.specialization = teacher_data["specialization"]
            if "phone_number" in teacher_data:
                teacher.phone_number = teacher_data["phone_number"]
            if "email" in teacher_data:
                teacher.email = teacher_data["email"]
            if "address" in teacher_data:
                teacher.address = teacher_data["address"]
            if "hire_date" in teacher_data:
                teacher.hire_date = teacher_data["hire_date"]
            
            # حفظ التغييرات
            session.commit()
            return True, "تم تحديث بيانات الأستاذ بنجاح"
        except Exception as e:
            session.rollback()
            print(f"خطأ في تحديث بيانات الأستاذ: {e}")
            return False, f"خطأ في تحديث بيانات الأستاذ: {str(e)}"
        finally:
            session.close()
    
    @staticmethod
    def delete_teacher(teacher_id):
        """حذف أستاذ"""
        session = DBSession()
        try:
            # الحصول على الأستاذ
            teacher = session.query(Teacher).filter_by(teacher_id=teacher_id).first()
            if not teacher:
                return False, "الأستاذ غير موجود"
            
            # حذف الأستاذ
            session.delete(teacher)
            session.commit()
            return True, "تم حذف الأستاذ بنجاح"
        except Exception as e:
            session.rollback()
            print(f"خطأ في حذف الأستاذ: {e}")
            return False, f"خطأ في حذف الأستاذ: {str(e)}"
        finally:
            session.close()
    
    @staticmethod
    def import_teachers_from_file(file_path, column_mapping):
        """استيراد الأساتذة من ملف"""
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
            required_columns = ["last_name", "first_name", "gender"]
            for col in required_columns:
                if col not in mapped_df.columns:
                    return False, f"العمود الإلزامي {col} غير موجود في الملف"
            
            # إضافة الأساتذة إلى قاعدة البيانات
            session = DBSession()
            try:
                success_count = 0
                error_count = 0
                
                for _, row in mapped_df.iterrows():
                    # إنشاء أستاذ جديد
                    teacher_data = {}
                    for col in mapped_df.columns:
                        if not pd.isna(row[col]):
                            teacher_data[col] = row[col]
                    
                    # التحقق من وجود البيانات الإلزامية
                    if all(col in teacher_data for col in required_columns):
                        teacher = Teacher(**teacher_data)
                        session.add(teacher)
                        success_count += 1
                    else:
                        error_count += 1
                
                session.commit()
                return True, f"تم استيراد {success_count} أستاذ بنجاح، {error_count} أستاذ لم يتم استيراده"
            except Exception as e:
                session.rollback()
                print(f"خطأ في استيراد الأساتذة: {e}")
                return False, f"خطأ في استيراد الأساتذة: {str(e)}"
            finally:
                session.close()
        except Exception as e:
            print(f"خطأ في قراءة الملف: {e}")
            return False, f"خطأ في قراءة الملف: {str(e)}"
