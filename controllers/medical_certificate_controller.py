#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
وحدة التحكم في الشهادات الطبية لنظام إدارة المدرسة
"""

import os
from datetime import datetime, date
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, between

from models.database import MedicalCertificate, Student, Session as DBSession

class MedicalCertificateController:
    """وحدة التحكم في الشهادات الطبية"""
    
    @staticmethod
    def get_all_certificates():
        """الحصول على جميع الشهادات الطبية"""
        session = DBSession()
        try:
            certificates = session.query(MedicalCertificate).all()
            return certificates
        except Exception as e:
            print(f"خطأ في الحصول على الشهادات الطبية: {e}")
            return []
        finally:
            session.close()
    
    @staticmethod
    def get_certificate_by_id(certificate_id):
        """الحصول على شهادة طبية حسب الرقم التعريفي"""
        session = DBSession()
        try:
            certificate = session.query(MedicalCertificate).filter_by(certificate_id=certificate_id).first()
            return certificate
        except Exception as e:
            print(f"خطأ في الحصول على الشهادة الطبية: {e}")
            return None
        finally:
            session.close()
    
    @staticmethod
    def get_certificates_by_student(student_id):
        """الحصول على الشهادات الطبية لتلميذ معين"""
        session = DBSession()
        try:
            certificates = session.query(MedicalCertificate).filter_by(student_id=student_id).all()
            return certificates
        except Exception as e:
            print(f"خطأ في الحصول على الشهادات الطبية للتلميذ: {e}")
            return []
        finally:
            session.close()
    
    @staticmethod
    def search_certificates_by_student_name(student_name):
        """البحث عن الشهادات الطبية حسب اسم التلميذ"""
        session = DBSession()
        try:
            # البحث عن التلاميذ الذين يطابق اسمهم نص البحث
            students = session.query(Student).filter(
                or_(
                    Student.first_name.like(f"%{student_name}%"),
                    Student.last_name.like(f"%{student_name}%")
                )
            ).all()
            
            # جمع الشهادات الطبية لهؤلاء التلاميذ
            certificates = []
            for student in students:
                student_certificates = session.query(MedicalCertificate).filter_by(student_id=student.student_id).all()
                certificates.extend(student_certificates)
            
            return certificates
        except Exception as e:
            print(f"خطأ في البحث عن الشهادات الطبية: {e}")
            return []
        finally:
            session.close()
    
    @staticmethod
    def get_certificates_by_date(specific_date):
        """الحصول على الشهادات الطبية التي تشمل تاريخًا معينًا"""
        session = DBSession()
        try:
            # البحث عن الشهادات الطبية التي تشمل التاريخ المحدد
            certificates = session.query(MedicalCertificate).filter(
                and_(
                    MedicalCertificate.start_date <= specific_date,
                    MedicalCertificate.end_date >= specific_date
                )
            ).all()
            
            return certificates
        except Exception as e:
            print(f"خطأ في الحصول على الشهادات الطبية حسب التاريخ: {e}")
            return []
        finally:
            session.close()
    
    @staticmethod
    def add_certificate(certificate_data):
        """إضافة شهادة طبية جديدة"""
        session = DBSession()
        try:
            # التحقق من وجود التلميذ
            student_id = certificate_data["student_id"]
            student = session.query(Student).filter_by(student_id=student_id).first()
            if not student:
                return False, "التلميذ غير موجود"
            
            # إنشاء كائن الشهادة الطبية
            certificate = MedicalCertificate(
                student_id=student_id,
                start_date=certificate_data["start_date"],
                end_date=certificate_data["end_date"],
                receipt_date=certificate_data["receipt_date"],
                school_doctor_verified=certificate_data.get("school_doctor_verified", False),
                parent_delivered=certificate_data.get("parent_delivered", False),
                notes=certificate_data.get("notes")
            )
            
            # إضافة الشهادة الطبية إلى قاعدة البيانات
            session.add(certificate)
            session.commit()
            return True, "تم إضافة الشهادة الطبية بنجاح"
        except Exception as e:
            session.rollback()
            print(f"خطأ في إضافة الشهادة الطبية: {e}")
            return False, f"خطأ في إضافة الشهادة الطبية: {str(e)}"
        finally:
            session.close()
    
    @staticmethod
    def update_certificate(certificate_id, certificate_data):
        """تحديث بيانات شهادة طبية"""
        session = DBSession()
        try:
            # الحصول على الشهادة الطبية
            certificate = session.query(MedicalCertificate).filter_by(certificate_id=certificate_id).first()
            if not certificate:
                return False, "الشهادة الطبية غير موجودة"
            
            # تحديث بيانات الشهادة الطبية
            certificate.start_date = certificate_data["start_date"]
            certificate.end_date = certificate_data["end_date"]
            certificate.receipt_date = certificate_data["receipt_date"]
            
            if "school_doctor_verified" in certificate_data:
                certificate.school_doctor_verified = certificate_data["school_doctor_verified"]
            if "parent_delivered" in certificate_data:
                certificate.parent_delivered = certificate_data["parent_delivered"]
            if "notes" in certificate_data:
                certificate.notes = certificate_data["notes"]
            
            # حفظ التغييرات
            session.commit()
            return True, "تم تحديث بيانات الشهادة الطبية بنجاح"
        except Exception as e:
            session.rollback()
            print(f"خطأ في تحديث بيانات الشهادة الطبية: {e}")
            return False, f"خطأ في تحديث بيانات الشهادة الطبية: {str(e)}"
        finally:
            session.close()
    
    @staticmethod
    def delete_certificate(certificate_id):
        """حذف شهادة طبية"""
        session = DBSession()
        try:
            # الحصول على الشهادة الطبية
            certificate = session.query(MedicalCertificate).filter_by(certificate_id=certificate_id).first()
            if not certificate:
                return False, "الشهادة الطبية غير موجودة"
            
            # حذف الشهادة الطبية
            session.delete(certificate)
            session.commit()
            return True, "تم حذف الشهادة الطبية بنجاح"
        except Exception as e:
            session.rollback()
            print(f"خطأ في حذف الشهادة الطبية: {e}")
            return False, f"خطأ في حذف الشهادة الطبية: {str(e)}"
        finally:
            session.close()
    
    @staticmethod
    def get_certificate_with_student_info(certificate_id):
        """الحصول على الشهادة الطبية مع معلومات التلميذ"""
        session = DBSession()
        try:
            # الحصول على الشهادة الطبية مع معلومات التلميذ
            certificate = session.query(MedicalCertificate).filter_by(certificate_id=certificate_id).first()
            if not certificate:
                return None
            
            # الحصول على معلومات التلميذ
            student = session.query(Student).filter_by(student_id=certificate.student_id).first()
            if not student:
                return None
            
            # إنشاء قاموس يحتوي على معلومات الشهادة الطبية والتلميذ
            certificate_info = {
                "certificate_id": certificate.certificate_id,
                "student_id": certificate.student_id,
                "student_name": f"{student.first_name} {student.last_name}",
                "start_date": certificate.start_date,
                "end_date": certificate.end_date,
                "receipt_date": certificate.receipt_date,
                "school_doctor_verified": certificate.school_doctor_verified,
                "parent_delivered": certificate.parent_delivered,
                "notes": certificate.notes
            }
            
            return certificate_info
        except Exception as e:
            print(f"خطأ في الحصول على الشهادة الطبية مع معلومات التلميذ: {e}")
            return None
        finally:
            session.close()
    
    @staticmethod
    def get_all_certificates_with_student_info():
        """الحصول على جميع الشهادات الطبية مع معلومات التلاميذ"""
        session = DBSession()
        try:
            # الحصول على جميع الشهادات الطبية
            certificates = session.query(MedicalCertificate).all()
            
            # إنشاء قائمة تحتوي على معلومات الشهادات الطبية والتلاميذ
            certificates_info = []
            for certificate in certificates:
                # الحصول على معلومات التلميذ
                student = session.query(Student).filter_by(student_id=certificate.student_id).first()
                if not student:
                    continue
                
                # إنشاء قاموس يحتوي على معلومات الشهادة الطبية والتلميذ
                certificate_info = {
                    "certificate_id": certificate.certificate_id,
                    "student_id": certificate.student_id,
                    "student_name": f"{student.first_name} {student.last_name}",
                    "start_date": certificate.start_date,
                    "end_date": certificate.end_date,
                    "receipt_date": certificate.receipt_date,
                    "school_doctor_verified": certificate.school_doctor_verified,
                    "parent_delivered": certificate.parent_delivered,
                    "notes": certificate.notes
                }
                
                certificates_info.append(certificate_info)
            
            return certificates_info
        except Exception as e:
            print(f"خطأ في الحصول على الشهادات الطبية مع معلومات التلاميذ: {e}")
            return []
        finally:
            session.close()
