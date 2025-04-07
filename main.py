#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
التطبيق الرئيسي لنظام إدارة المدرسة
"""

import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt6.QtCore import Qt

# إضافة مسار المشروع إلى مسار البحث
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from views.main_window import MainWindow
from views.student_management import StudentManagementWidget
from views.teacher_management import TeacherManagementWidget
from views.medical_certificate import MedicalCertificateWidget
from views.behavior_report import BehaviorReportWidget
from views.parent_summon import ParentSummonWidget
from models.database import init_db

class SchoolManagementApp(QMainWindow):
    """التطبيق الرئيسي لنظام إدارة المدرسة"""
    
    def __init__(self):
        super().__init__()
        
        # إعداد النافذة الرئيسية
        self.setWindowTitle("نظام إدارة المدرسة")
        self.setMinimumSize(1200, 800)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        # إنشاء ويدجت متعدد الصفحات
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # إنشاء الواجهات
        self.main_window = MainWindow()
        self.student_management = StudentManagementWidget()
        self.teacher_management = TeacherManagementWidget()
        self.medical_certificate = MedicalCertificateWidget()
        self.behavior_report = BehaviorReportWidget()
        self.parent_summon = ParentSummonWidget()
        
        # إضافة الواجهات إلى الويدجت متعدد الصفحات
        self.stacked_widget.addWidget(self.main_window)
        self.stacked_widget.addWidget(self.student_management)
        self.stacked_widget.addWidget(self.teacher_management)
        self.stacked_widget.addWidget(self.medical_certificate)
        self.stacked_widget.addWidget(self.behavior_report)
        self.stacked_widget.addWidget(self.parent_summon)
        
        # ربط أزرار الواجهة الرئيسية بالواجهات الفرعية
        self.main_window.open_students_management = lambda: self.stacked_widget.setCurrentWidget(self.student_management)
        self.main_window.open_teachers_management = lambda: self.stacked_widget.setCurrentWidget(self.teacher_management)
        self.main_window.open_medical_certificates = lambda: self.stacked_widget.setCurrentWidget(self.medical_certificate)
        self.main_window.open_behavior_reports = lambda: self.stacked_widget.setCurrentWidget(self.behavior_report)
        self.main_window.open_parent_summons = lambda: self.stacked_widget.setCurrentWidget(self.parent_summon)
        
        # ربط أزرار العودة في الواجهات الفرعية بالواجهة الرئيسية
        self.student_management.go_back = lambda: self.stacked_widget.setCurrentWidget(self.main_window)
        self.teacher_management.go_back = lambda: self.stacked_widget.setCurrentWidget(self.main_window)
        self.medical_certificate.go_back = lambda: self.stacked_widget.setCurrentWidget(self.main_window)
        self.behavior_report.go_back = lambda: self.stacked_widget.setCurrentWidget(self.main_window)
        self.parent_summon.go_back = lambda: self.stacked_widget.setCurrentWidget(self.main_window)

def main():
    """الدالة الرئيسية للتطبيق"""
    # تهيئة قاعدة البيانات
    init_db()
    
    # إنشاء التطبيق
    app = QApplication(sys.argv)
    
    # تعيين اتجاه التطبيق من اليمين إلى اليسار
    app.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
    
    # إنشاء النافذة الرئيسية
    window = SchoolManagementApp()
    window.show()
    
    # تشغيل التطبيق
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
