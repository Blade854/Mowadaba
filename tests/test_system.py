#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
سكريبت اختبار وظائف نظام إدارة المدرسة
"""

import os
import sys
import unittest
from datetime import date, datetime

# إضافة مسار المشروع إلى مسار البحث
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.database import init_db, Student, Teacher, MedicalCertificate, BehaviorReport, ParentSummon, Session as DBSession
from controllers.student_controller import StudentController
from controllers.teacher_controller import TeacherController
from controllers.medical_certificate_controller import MedicalCertificateController
from controllers.behavior_report_controller import BehaviorReportController
from controllers.parent_summon_controller import ParentSummonController

class TestSchoolManagementSystem(unittest.TestCase):
    """اختبار وظائف نظام إدارة المدرسة"""
    
    @classmethod
    def setUpClass(cls):
        """إعداد بيئة الاختبار"""
        # تهيئة قاعدة البيانات
        init_db(test=True)
        
        # إضافة بيانات اختبار
        cls.add_test_data()
    
    @classmethod
    def add_test_data(cls):
        """إضافة بيانات اختبار إلى قاعدة البيانات"""
        # إضافة تلميذ للاختبار
        student_data = {
            "student_id": "TEST001",
            "last_name": "اختبار",
            "first_name": "تلميذ",
            "gender": "ذكر",
            "birth_date": date(2010, 1, 1)
        }
        StudentController.add_student(student_data)
        
        # إضافة أستاذ للاختبار
        teacher_data = {
            "last_name": "اختبار",
            "first_name": "أستاذ",
            "gender": "ذكر",
            "specialization": "رياضيات"
        }
        TeacherController.add_teacher(teacher_data)
    
    def test_student_management(self):
        """اختبار وظائف إدارة التلاميذ"""
        # اختبار إضافة تلميذ
        student_data = {
            "student_id": "TEST002",
            "last_name": "محمد",
            "first_name": "أحمد",
            "gender": "ذكر",
            "birth_date": date(2011, 5, 15)
        }
        success, _ = StudentController.add_student(student_data)
        self.assertTrue(success)
        
        # اختبار الحصول على تلميذ
        student = StudentController.get_student_by_id("TEST002")
        self.assertIsNotNone(student)
        self.assertEqual(student.first_name, "أحمد")
        
        # اختبار تحديث بيانات تلميذ
        update_data = {
            "last_name": "محمد",
            "first_name": "أحمد معدل",
            "gender": "ذكر",
            "birth_date": date(2011, 5, 15)
        }
        success, _ = StudentController.update_student("TEST002", update_data)
        self.assertTrue(success)
        
        # التحقق من التحديث
        student = StudentController.get_student_by_id("TEST002")
        self.assertEqual(student.first_name, "أحمد معدل")
        
        # اختبار البحث عن تلميذ
        students = StudentController.search_students("أحمد")
        self.assertTrue(len(students) > 0)
        
        # اختبار حذف تلميذ
        success, _ = StudentController.delete_student("TEST002")
        self.assertTrue(success)
        
        # التحقق من الحذف
        student = StudentController.get_student_by_id("TEST002")
        self.assertIsNone(student)
    
    def test_teacher_management(self):
        """اختبار وظائف إدارة الأساتذة"""
        # اختبار إضافة أستاذ
        teacher_data = {
            "last_name": "علي",
            "first_name": "سمير",
            "gender": "ذكر",
            "specialization": "فيزياء",
            "phone_number": "0555123456"
        }
        success, _ = TeacherController.add_teacher(teacher_data)
        self.assertTrue(success)
        
        # اختبار البحث عن أستاذ
        teachers = TeacherController.search_teachers("سمير")
        self.assertTrue(len(teachers) > 0)
        teacher_id = teachers[0].teacher_id
        
        # اختبار تحديث بيانات أستاذ
        update_data = {
            "last_name": "علي",
            "first_name": "سمير معدل",
            "gender": "ذكر",
            "specialization": "فيزياء"
        }
        success, _ = TeacherController.update_teacher(teacher_id, update_data)
        self.assertTrue(success)
        
        # التحقق من التحديث
        teachers = TeacherController.search_teachers("سمير معدل")
        self.assertTrue(len(teachers) > 0)
        
        # اختبار حذف أستاذ
        success, _ = TeacherController.delete_teacher(teacher_id)
        self.assertTrue(success)
    
    def test_medical_certificate_management(self):
        """اختبار وظائف إدارة الشهادات الطبية"""
        # اختبار إضافة شهادة طبية
        certificate_data = {
            "student_id": "TEST001",
            "start_date": date(2023, 10, 1),
            "end_date": date(2023, 10, 5),
            "receipt_date": date(2023, 10, 2),
            "school_doctor_verified": True,
            "parent_delivered": True,
            "notes": "شهادة طبية للاختبار"
        }
        success, _ = MedicalCertificateController.add_certificate(certificate_data)
        self.assertTrue(success)
        
        # اختبار الحصول على الشهادات الطبية لتلميذ
        certificates = MedicalCertificateController.get_certificates_by_student("TEST001")
        self.assertTrue(len(certificates) > 0)
        certificate_id = certificates[0].certificate_id
        
        # اختبار تحديث بيانات شهادة طبية
        update_data = {
            "start_date": date(2023, 10, 1),
            "end_date": date(2023, 10, 7),  # تمديد الشهادة
            "receipt_date": date(2023, 10, 2),
            "school_doctor_verified": True,
            "parent_delivered": True
        }
        success, _ = MedicalCertificateController.update_certificate(certificate_id, update_data)
        self.assertTrue(success)
        
        # اختبار الحصول على الشهادات الطبية حسب التاريخ
        certificates = MedicalCertificateController.get_certificates_by_date(date(2023, 10, 6))
        self.assertTrue(len(certificates) > 0)
        
        # اختبار حذف شهادة طبية
        success, _ = MedicalCertificateController.delete_certificate(certificate_id)
        self.assertTrue(success)
    
    def test_behavior_report_management(self):
        """اختبار وظائف إدارة التقارير السلوكية"""
        # اختبار إضافة تقرير سلوكي
        report_data = {
            "student_id": "TEST001",
            "reporter_name": "أحمد محمد",
            "reporter_role": "أستاذ",
            "reporter_specialization": "رياضيات",
            "report_date": date(2023, 11, 1),
            "report_time": datetime.strptime("10:30", "%H:%M").time(),
            "description": "تقرير سلوكي للاختبار"
        }
        actions_list = ["إنذار شفهي", "توبيخ"]
        success, _ = BehaviorReportController.add_report(report_data, actions_list)
        self.assertTrue(success)
        
        # اختبار الحصول على التقارير السلوكية لتلميذ
        reports = BehaviorReportController.get_reports_by_student("TEST001")
        self.assertTrue(len(reports) > 0)
        report_id = reports[0].report_id
        
        # اختبار الحصول على الإجراءات المتخذة للتقرير
        actions = BehaviorReportController.get_report_actions(report_id)
        self.assertEqual(len(actions), 2)
        
        # اختبار تحديث بيانات تقرير سلوكي
        update_data = {
            "student_id": "TEST001",
            "reporter_name": "أحمد محمد معدل",
            "reporter_role": "أستاذ",
            "reporter_specialization": "رياضيات",
            "report_date": date(2023, 11, 1),
            "report_time": datetime.strptime("10:30", "%H:%M").time(),
            "description": "تقرير سلوكي للاختبار معدل"
        }
        updated_actions = ["إنذار شفهي", "إنذار كتابي"]
        success, _ = BehaviorReportController.update_report(report_id, update_data, updated_actions)
        self.assertTrue(success)
        
        # اختبار الحصول على التقرير مع معلومات التلميذ
        report_info = BehaviorReportController.get_report_with_student_info(report_id)
        self.assertIsNotNone(report_info)
        self.assertEqual(report_info["reporter_name"], "أحمد محمد معدل")
        
        # اختبار حذف تقرير سلوكي
        success, _ = BehaviorReportController.delete_report(report_id)
        self.assertTrue(success)
    
    def test_parent_summon_management(self):
        """اختبار وظائف إدارة استدعاءات الأولياء"""
        # اختبار إضافة استدعاء ولي
        summon_data = {
            "student_id": "TEST001",
            "parent_name": "والد التلميذ",
            "summoner_name": "أحمد محمد",
            "summon_date": date(2023, 11, 5),
            "summon_time": datetime.strptime("11:00", "%H:%M").time(),
            "attended": False,
            "notes": "استدعاء ولي للاختبار"
        }
        success, _ = ParentSummonController.add_summon(summon_data)
        self.assertTrue(success)
        
        # اختبار الحصول على استدعاءات الأولياء لتلميذ
        summons = ParentSummonController.get_summons_by_student("TEST001")
        self.assertTrue(len(summons) > 0)
        summon_id = summons[0].summon_id
        
        # اختبار تحديث بيانات استدعاء ولي
        update_data = {
            "parent_name": "والد التلميذ",
            "summoner_name": "أحمد محمد",
            "summon_date": date(2023, 11, 5),
            "summon_time": datetime.strptime("11:00", "%H:%M").time(),
            "attended": True,  # تحديث حالة الحضور
            "notes": "استدعاء ولي للاختبار - تم الحضور"
        }
        success, _ = ParentSummonController.update_summon(summon_id, update_data)
        self.assertTrue(success)
        
        # اختبار الحصول على استدعاءات الأولياء حسب التاريخ
        summons = ParentSummonController.get_summons_by_date(date(2023, 11, 5))
        self.assertTrue(len(summons) > 0)
        
        # اختبار الحصول على الاستدعاء مع معلومات التلميذ
        summon_info = ParentSummonController.get_summon_with_student_info(summon_id)
        self.assertIsNotNone(summon_info)
        self.assertTrue(summon_info["attended"])
        
        # اختبار حذف استدعاء ولي
        success, _ = ParentSummonController.delete_summon(summon_id)
        self.assertTrue(success)
    
    @classmethod
    def tearDownClass(cls):
        """تنظيف بيئة الاختبار"""
        # حذف بيانات الاختبار
        session = DBSession()
        try:
            # حذف التلميذ المستخدم في الاختبار
            student = session.query(Student).filter_by(student_id="TEST001").first()
            if student:
                session.delete(student)
            
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"خطأ في تنظيف بيانات الاختبار: {e}")
        finally:
            session.close()

if __name__ == "__main__":
    unittest.main()
