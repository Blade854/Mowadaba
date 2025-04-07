#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
الواجهة الرئيسية لنظام إدارة المدرسة
"""

import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, QGridLayout, 
                            QSpacerItem, QSizePolicy)
from PyQt6.QtGui import QIcon, QFont, QPixmap
from PyQt6.QtCore import Qt, QSize

# إضافة مسار المشروع إلى مسار البحث
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class MainWindow(QMainWindow):
    """الواجهة الرئيسية للتطبيق"""
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("نظام إدارة المدرسة")
        self.setMinimumSize(1000, 700)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        # إنشاء الويدجت المركزي
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # إنشاء التخطيط الرئيسي
        main_layout = QVBoxLayout(central_widget)
        
        # إضافة شعار وعنوان التطبيق
        header_layout = QHBoxLayout()
        
        # إضافة شعار (يمكن استبداله بشعار حقيقي لاحقًا)
        logo_label = QLabel()
        # logo_label.setPixmap(QPixmap("path/to/logo.png").scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))
        header_layout.addWidget(logo_label)
        
        # إضافة عنوان التطبيق
        title_label = QLabel("نظام إدارة المدرسة")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(title_label, 1)
        
        main_layout.addLayout(header_layout)
        
        # إضافة وصف التطبيق
        description_label = QLabel("نظام متكامل لإدارة شؤون المدرسة: التلاميذ، الأساتذة، الشهادات الطبية، التقارير والاستدعاءات")
        description_font = QFont()
        description_font.setPointSize(12)
        description_label.setFont(description_font)
        description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(description_label)
        
        # إضافة خط فاصل
        separator = QWidget()
        separator.setFixedHeight(2)
        separator.setStyleSheet("background-color: #cccccc;")
        main_layout.addWidget(separator)
        
        # إنشاء شبكة الأزرار
        button_grid = QGridLayout()
        button_grid.setSpacing(20)
        
        # تعريف أزرار الوظائف
        buttons_info = [
            {"text": "إدارة التلاميذ", "icon": "students.png", "slot": self.open_students_management},
            {"text": "إدارة الأساتذة", "icon": "teachers.png", "slot": self.open_teachers_management},
            {"text": "إدارة العمال", "icon": "staff.png", "slot": self.open_staff_management},
            {"text": "الشهادات الطبية", "icon": "medical.png", "slot": self.open_medical_certificates},
            {"text": "التقارير السلوكية", "icon": "reports.png", "slot": self.open_behavior_reports},
            {"text": "استدعاءات الأولياء", "icon": "summons.png", "slot": self.open_parent_summons},
            {"text": "الإحصائيات", "icon": "statistics.png", "slot": self.open_statistics},
            {"text": "الإعدادات", "icon": "settings.png", "slot": self.open_settings}
        ]
        
        # إنشاء الأزرار وإضافتها إلى الشبكة
        for i, button_info in enumerate(buttons_info):
            row, col = divmod(i, 4)
            button = self.create_menu_button(button_info["text"], button_info["icon"], button_info["slot"])
            button_grid.addWidget(button, row, col)
        
        # إضافة مساحة مرنة قبل وبعد شبكة الأزرار
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        main_layout.addLayout(button_grid)
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        # إضافة شريط الحالة
        self.statusBar().showMessage("جاهز")
    
    def create_menu_button(self, text, icon_name, slot):
        """إنشاء زر قائمة مع أيقونة ونص"""
        button = QPushButton(text)
        button.setMinimumSize(200, 150)
        
        # تعيين الأيقونة إذا كانت موجودة
        # icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resources", icon_name)
        # if os.path.exists(icon_path):
        #     button.setIcon(QIcon(icon_path))
        #     button.setIconSize(QSize(64, 64))
        
        # تعيين نمط الزر
        button.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                border: 2px solid #cccccc;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
                border-color: #999999;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """)
        
        # ربط الزر بالوظيفة المناسبة
        button.clicked.connect(slot)
        
        return button
    
    # وظائف فتح النوافذ الفرعية
    def open_students_management(self):
        self.statusBar().showMessage("فتح إدارة التلاميذ...")
        # TODO: تنفيذ فتح نافذة إدارة التلاميذ
    
    def open_teachers_management(self):
        self.statusBar().showMessage("فتح إدارة الأساتذة...")
        # TODO: تنفيذ فتح نافذة إدارة الأساتذة
    
    def open_staff_management(self):
        self.statusBar().showMessage("فتح إدارة العمال...")
        # TODO: تنفيذ فتح نافذة إدارة العمال
    
    def open_medical_certificates(self):
        self.statusBar().showMessage("فتح إدارة الشهادات الطبية...")
        # TODO: تنفيذ فتح نافذة إدارة الشهادات الطبية
    
    def open_behavior_reports(self):
        self.statusBar().showMessage("فتح إدارة التقارير السلوكية...")
        # TODO: تنفيذ فتح نافذة إدارة التقارير السلوكية
    
    def open_parent_summons(self):
        self.statusBar().showMessage("فتح إدارة استدعاءات الأولياء...")
        # TODO: تنفيذ فتح نافذة إدارة استدعاءات الأولياء
    
    def open_statistics(self):
        self.statusBar().showMessage("فتح الإحصائيات...")
        # TODO: تنفيذ فتح نافذة الإحصائيات
    
    def open_settings(self):
        self.statusBar().showMessage("فتح الإعدادات...")
        # TODO: تنفيذ فتح نافذة الإعدادات

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
