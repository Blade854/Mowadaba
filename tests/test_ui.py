#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
سكريبت اختبار واجهات المستخدم لنظام إدارة المدرسة
"""

import os
import sys
import unittest
from PyQt6.QtWidgets import QApplication
from PyQt6.QtTest import QTest
from PyQt6.QtCore import Qt

# إضافة مسار المشروع إلى مسار البحث
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.database import init_db
from views.main_window import MainWindow
from views.student_management import StudentManagementWidget
from views.teacher_management import TeacherManagementWidget
from views.medical_certificate import MedicalCertificateWidget
from views.behavior_report import BehaviorReportWidget
from views.parent_summon import ParentSummonWidget

class TestUserInterface(unittest.TestCase):
    """اختبار واجهات المستخدم"""
    
    @classmethod
    def setUpClass(cls):
        """إعداد بيئة الاختبار"""
        # تهيئة قاعدة البيانات
        init_db(test=True)
        
        # إنشاء تطبيق PyQt
        cls.app = QApplication.instance()
        if not cls.app:
            cls.app = QApplication(sys.argv)
    
    def test_main_window(self):
        """اختبار الواجهة الرئيسية"""
        # إنشاء الواجهة الرئيسية
        main_window = MainWindow()
        
        # التحقق من وجود الأزرار الرئيسية
        self.assertIsNotNone(main_window.students_button)
        self.assertIsNotNone(main_window.teachers_button)
        self.assertIsNotNone(main_window.medical_certificates_button)
        self.assertIsNotNone(main_window.behavior_reports_button)
        self.assertIsNotNone(main_window.parent_summons_button)
    
    def test_student_management_widget(self):
        """اختبار واجهة إدارة التلاميذ"""
        # إنشاء واجهة إدارة التلاميذ
        student_widget = StudentManagementWidget()
        
        # التحقق من وجود العناصر الرئيسية
        self.assertIsNotNone(student_widget.students_table)
        self.assertIsNotNone(student_widget.search_input)
        self.assertIsNotNone(student_widget.add_button)
        self.assertIsNotNone(student_widget.edit_button)
        self.assertIsNotNone(student_widget.delete_button)
        self.assertIsNotNone(student_widget.import_button)
    
    def test_teacher_management_widget(self):
        """اختبار واجهة إدارة الأساتذة"""
        # إنشاء واجهة إدارة الأساتذة
        teacher_widget = TeacherManagementWidget()
        
        # التحقق من وجود العناصر الرئيسية
        self.assertIsNotNone(teacher_widget.teachers_table)
        self.assertIsNotNone(teacher_widget.search_input)
        self.assertIsNotNone(teacher_widget.add_button)
        self.assertIsNotNone(teacher_widget.edit_button)
        self.assertIsNotNone(teacher_widget.delete_button)
        self.assertIsNotNone(teacher_widget.import_button)
    
    def test_medical_certificate_widget(self):
        """اختبار واجهة إدارة الشهادات الطبية"""
        # إنشاء واجهة إدارة الشهادات الطبية
        certificate_widget = MedicalCertificateWidget()
        
        # التحقق من وجود العناصر الرئيسية
        self.assertIsNotNone(certificate_widget.certificates_table)
        self.assertIsNotNone(certificate_widget.student_radio)
        self.assertIsNotNone(certificate_widget.date_radio)
        self.assertIsNotNone(certificate_widget.add_button)
        self.assertIsNotNone(certificate_widget.edit_button)
        self.assertIsNotNone(certificate_widget.delete_button)
    
    def test_behavior_report_widget(self):
        """اختبار واجهة إدارة التقارير السلوكية"""
        # إنشاء واجهة إدارة التقارير السلوكية
        report_widget = BehaviorReportWidget()
        
        # التحقق من وجود العناصر الرئيسية
        self.assertIsNotNone(report_widget.reports_table)
        self.assertIsNotNone(report_widget.search_input)
        self.assertIsNotNone(report_widget.add_button)
        self.assertIsNotNone(report_widget.edit_button)
        self.assertIsNotNone(report_widget.delete_button)
    
    def test_parent_summon_widget(self):
        """اختبار واجهة إدارة استدعاءات الأولياء"""
        # إنشاء واجهة إدارة استدعاءات الأولياء
        summon_widget = ParentSummonWidget()
        
        # التحقق من وجود العناصر الرئيسية
        self.assertIsNotNone(summon_widget.summons_table)
        self.assertIsNotNone(summon_widget.student_radio)
        self.assertIsNotNone(summon_widget.date_radio)
        self.assertIsNotNone(summon_widget.pending_radio)
        self.assertIsNotNone(summon_widget.add_button)
        self.assertIsNotNone(summon_widget.edit_button)
        self.assertIsNotNone(summon_widget.delete_button)

if __name__ == "__main__":
    unittest.main()
