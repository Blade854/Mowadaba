#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
وحدة التحكم في استدعاءات الأولياء لنظام إدارة المدرسة
"""

import os
from datetime import datetime, date
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from models.database import ParentSummon, Student, Session as DBSession

class ParentSummonController:
    """وحدة التحكم في استدعاءات الأولياء"""
    
    @staticmethod
    def get_all_summons():
        """الحصول على جميع استدعاءات الأولياء"""
        session = DBSession()
        try:
            summons = session.query(ParentSummon).all()
            return summons
        except Exception as e:
            print(f"خطأ في الحصول على استدعاءات الأولياء: {e}")
            return []
        finally:
            session.close()
    
    @staticmethod
    def get_summon_by_id(summon_id):
        """الحصول على استدعاء ولي حسب الرقم التعريفي"""
        session = DBSession()
        try:
            summon = session.query(ParentSummon).filter_by(summon_id=summon_id).first()
            return summon
        except Exception as e:
            print(f"خطأ في الحصول على استدعاء الولي: {e}")
            return None
        finally:
            session.close()
    
    @staticmethod
    def get_summon_by_report_id(report_id):
        """الحصول على استدعاء ولي حسب رقم التقرير"""
        session = DBSession()
        try:
            summon = session.query(ParentSummon).filter_by(report_id=report_id).first()
            return summon
        except Exception as e:
            print(f"خطأ في الحصول على استدعاء الولي حسب رقم التقرير: {e}")
            return None
        finally:
            session.close()
    
    @staticmethod
    def get_summons_by_student(student_id):
        """الحصول على استدعاءات الأولياء لتلميذ معين"""
        session = DBSession()
        try:
            summons = session.query(ParentSummon).filter_by(student_id=student_id).all()
            return summons
        except Exception as e:
            print(f"خطأ في الحصول على استدعاءات الأولياء للتلميذ: {e}")
            return []
        finally:
            session.close()
    
    @staticmethod
    def search_summons_by_student_name(student_name):
        """البحث عن استدعاءات الأولياء حسب اسم التلميذ"""
        session = DBSession()
        try:
            # البحث عن التلاميذ الذين يطابق اسمهم نص البحث
            students = session.query(Student).filter(
                or_(
                    Student.first_name.like(f"%{student_name}%"),
                    Student.last_name.like(f"%{student_name}%")
                )
            ).all()
            
            # جمع استدعاءات الأولياء لهؤلاء التلاميذ
            summons = []
            for student in students:
                student_summons = session.query(ParentSummon).filter_by(student_id=student.student_id).all()
                summons.extend(student_summons)
            
            return summons
        except Exception as e:
            print(f"خطأ في البحث عن استدعاءات الأولياء: {e}")
            return []
        finally:
            session.close()
    
    @staticmethod
    def get_summons_by_date(specific_date):
        """الحصول على استدعاءات الأولياء لتاريخ معين"""
        session = DBSession()
        try:
            # البحث عن استدعاءات الأولياء للتاريخ المحدد
            summons = session.query(ParentSummon).filter(
                ParentSummon.summon_date == specific_date
            ).all()
            
            return summons
        except Exception as e:
            print(f"خطأ في الحصول على استدعاءات الأولياء حسب التاريخ: {e}")
            return []
        finally:
            session.close()
    
    @staticmethod
    def get_pending_summons():
        """الحصول على استدعاءات الأولياء المعلقة (التي لم يحضر فيها الأولياء)"""
        session = DBSession()
        try:
            # البحث عن استدعاءات الأولياء المعلقة
            summons = session.query(ParentSummon).filter_by(attended=False).all()
            
            return summons
        except Exception as e:
            print(f"خطأ في الحصول على استدعاءات الأولياء المعلقة: {e}")
            return []
        finally:
            session.close()
    
    @staticmethod
    def add_summon(summon_data):
        """إضافة استدعاء ولي جديد"""
        session = DBSession()
        try:
            # التحقق من وجود التلميذ
            student_id = summon_data["student_id"]
            student = session.query(Student).filter_by(student_id=student_id).first()
            if not student:
                return False, "التلميذ غير موجود"
            
            # إنشاء كائن استدعاء الولي
            summon = ParentSummon(
                student_id=student_id,
                parent_name=summon_data["parent_name"],
                summoner_name=summon_data["summoner_name"],
                summon_date=summon_data["summon_date"],
                summon_time=summon_data["summon_time"],
                attended=summon_data.get("attended", False),
                notes=summon_data.get("notes"),
                report_id=summon_data.get("report_id")
            )
            
            # إضافة استدعاء الولي إلى قاعدة البيانات
            session.add(summon)
            session.commit()
            return True, "تم إضافة استدعاء الولي بنجاح"
        except Exception as e:
            session.rollback()
            print(f"خطأ في إضافة استدعاء الولي: {e}")
            return False, f"خطأ في إضافة استدعاء الولي: {str(e)}"
        finally:
            session.close()
    
    @staticmethod
    def update_summon(summon_id, summon_data):
        """تحديث بيانات استدعاء ولي"""
        session = DBSession()
        try:
            # الحصول على استدعاء الولي
            summon = session.query(ParentSummon).filter_by(summon_id=summon_id).first()
            if not summon:
                return False, "استدعاء الولي غير موجود"
            
            # تحديث بيانات استدعاء الولي
            summon.parent_name = summon_data["parent_name"]
            summon.summoner_name = summon_data["summoner_name"]
            summon.summon_date = summon_data["summon_date"]
            summon.summon_time = summon_data["summon_time"]
            
            if "attended" in summon_data:
                summon.attended = summon_data["attended"]
            if "notes" in summon_data:
                summon.notes = summon_data["notes"]
            if "report_id" in summon_data:
                summon.report_id = summon_data["report_id"]
            
            # حفظ التغييرات
            session.commit()
            return True, "تم تحديث بيانات استدعاء الولي بنجاح"
        except Exception as e:
            session.rollback()
            print(f"خطأ في تحديث بيانات استدعاء الولي: {e}")
            return False, f"خطأ في تحديث بيانات استدعاء الولي: {str(e)}"
        finally:
            session.close()
    
    @staticmethod
    def delete_summon(summon_id):
        """حذف استدعاء ولي"""
        session = DBSession()
        try:
            # الحصول على استدعاء الولي
            summon = session.query(ParentSummon).filter_by(summon_id=summon_id).first()
            if not summon:
                return False, "استدعاء الولي غير موجود"
            
            # حذف استدعاء الولي
            session.delete(summon)
            session.commit()
            return True, "تم حذف استدعاء الولي بنجاح"
        except Exception as e:
            session.rollback()
            print(f"خطأ في حذف استدعاء الولي: {e}")
            return False, f"خطأ في حذف استدعاء الولي: {str(e)}"
        finally:
            session.close()
    
    @staticmethod
    def delete_summons_by_report_id(report_id):
        """حذف استدعاءات الأولياء حسب رقم التقرير"""
        session = DBSession()
        try:
            # حذف استدعاءات الأولياء المرتبطة بالتقرير
            session.query(ParentSummon).filter_by(report_id=report_id).delete()
            session.commit()
            return True, "تم حذف استدعاءات الأولياء المرتبطة بالتقرير بنجاح"
        except Exception as e:
            session.rollback()
            print(f"خطأ في حذف استدعاءات الأولياء المرتبطة بالتقرير: {e}")
            return False, f"خطأ في حذف استدعاءات الأولياء المرتبطة بالتقرير: {str(e)}"
        finally:
            session.close()
    
    @staticmethod
    def get_summon_with_student_info(summon_id):
        """الحصول على استدعاء الولي مع معلومات التلميذ"""
        session = DBSession()
        try:
            # الحصول على استدعاء الولي
            summon = session.query(ParentSummon).filter_by(summon_id=summon_id).first()
            if not summon:
                return None
            
            # الحصول على معلومات التلميذ
            student = session.query(Student).filter_by(student_id=summon.student_id).first()
            if not student:
                return None
            
            # إنشاء قاموس يحتوي على معلومات استدعاء الولي والتلميذ
            summon_info = {
                "summon_id": summon.summon_id,
                "student_id": summon.student_id,
                "student_name": f"{student.first_name} {student.last_name}",
                "parent_name": summon.parent_name,
                "summoner_name": summon.summoner_name,
                "summon_date": summon.summon_date,
                "summon_time": summon.summon_time,
                "attended": summon.attended,
                "notes": summon.notes,
                "report_id": summon.report_id
            }
            
            return summon_info
        except Exception as e:
            print(f"خطأ في الحصول على استدعاء الولي مع معلومات التلميذ: {e}")
            return None
        finally:
            session.close()
    
    @staticmethod
    def get_all_summons_with_student_info():
        """الحصول على جميع استدعاءات الأولياء مع معلومات التلاميذ"""
        session = DBSession()
        try:
            # الحصول على جميع استدعاءات الأولياء
            summons = session.query(ParentSummon).all()
            
            # إنشاء قائمة تحتوي على معلومات استدعاءات الأولياء والتلاميذ
            summons_info = []
            for summon in summons:
                # الحصول على معلومات التلميذ
                student = session.query(Student).filter_by(student_id=summon.student_id).first()
                if not student:
                    continue
                
                # إنشاء قاموس يحتوي على معلومات استدعاء الولي والتلميذ
                summon_info = {
                    "summon_id": summon.summon_id,
                    "student_id": summon.student_id,
                    "student_name": f"{student.first_name} {student.last_name}",
                    "parent_name": summon.parent_name,
                    "summoner_name": summon.summoner_name,
                    "summon_date": summon.summon_date,
                    "summon_time": summon.summon_time,
                    "attended": summon.attended,
                    "notes": summon.notes,
                    "report_id": summon.report_id
                }
                
                summons_info.append(summon_info)
            
            return summons_info
        except Exception as e:
            print(f"خطأ في الحصول على استدعاءات الأولياء مع معلومات التلاميذ: {e}")
            return []
        finally:
            session.close()
