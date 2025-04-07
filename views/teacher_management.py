#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
واجهة إدارة الأساتذة لنظام إدارة المدرسة
"""

import sys
import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
                            QTableWidget, QTableWidgetItem, QLineEdit, QComboBox,
                            QFormLayout, QDateEdit, QDialog, QFileDialog, QHeaderView,
                            QMessageBox, QTabWidget, QGroupBox)
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt, QDate

# إضافة مسار المشروع إلى مسار البحث
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import reshape_arabic, date_to_qdate, qdate_to_date, show_error, show_info, read_excel_file, map_columns

class TeacherManagementWidget(QWidget):
    """واجهة إدارة الأساتذة"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.setup_ui()
    
    def setup_ui(self):
        """إعداد واجهة المستخدم"""
        main_layout = QVBoxLayout(self)
        
        # إضافة عنوان الصفحة
        title_label = QLabel("إدارة الأساتذة")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # إضافة شريط البحث
        search_layout = QHBoxLayout()
        search_label = QLabel("بحث:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("أدخل اسم الأستاذ أو التخصص...")
        self.search_input.textChanged.connect(self.filter_teachers)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        main_layout.addLayout(search_layout)
        
        # إضافة أزرار العمليات
        buttons_layout = QHBoxLayout()
        
        self.add_button = QPushButton("إضافة أستاذ")
        self.add_button.clicked.connect(self.add_teacher)
        buttons_layout.addWidget(self.add_button)
        
        self.edit_button = QPushButton("تعديل أستاذ")
        self.edit_button.clicked.connect(self.edit_teacher)
        buttons_layout.addWidget(self.edit_button)
        
        self.delete_button = QPushButton("حذف أستاذ")
        self.delete_button.clicked.connect(self.delete_teacher)
        buttons_layout.addWidget(self.delete_button)
        
        self.import_button = QPushButton("استيراد من ملف")
        self.import_button.clicked.connect(self.import_teachers)
        buttons_layout.addWidget(self.import_button)
        
        self.refresh_button = QPushButton("تحديث")
        self.refresh_button.clicked.connect(self.load_teachers)
        buttons_layout.addWidget(self.refresh_button)
        
        main_layout.addLayout(buttons_layout)
        
        # إضافة جدول الأساتذة
        self.teachers_table = QTableWidget()
        self.teachers_table.setColumnCount(7)
        self.teachers_table.setHorizontalHeaderLabels([
            "الرقم", "اللقب", "الاسم", "الجنس", 
            "تاريخ الميلاد", "التخصص", "رقم الهاتف"
        ])
        self.teachers_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.teachers_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.teachers_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.teachers_table.itemDoubleClicked.connect(self.edit_teacher)
        main_layout.addWidget(self.teachers_table)
        
        # إضافة زر العودة
        back_layout = QHBoxLayout()
        self.back_button = QPushButton("العودة إلى الصفحة الرئيسية")
        self.back_button.clicked.connect(self.go_back)
        back_layout.addWidget(self.back_button)
        main_layout.addLayout(back_layout)
        
        # تحميل بيانات الأساتذة
        self.load_teachers()
    
    def load_teachers(self):
        """تحميل بيانات الأساتذة من قاعدة البيانات"""
        # TODO: تنفيذ تحميل بيانات الأساتذة من قاعدة البيانات
        # هذه بيانات تجريبية للعرض فقط
        self.teachers_table.setRowCount(0)
        
        sample_data = [
            {"id": 1, "last_name": "محمد", "first_name": "أحمد", "gender": "ذكر", 
             "birth_date": "1980-05-15", "specialization": "رياضيات", "phone": "0555123456"},
            {"id": 2, "last_name": "علي", "first_name": "سمير", "gender": "ذكر", 
             "birth_date": "1975-08-20", "specialization": "فيزياء", "phone": "0555789012"},
            {"id": 3, "last_name": "أحمد", "first_name": "فاطمة", "gender": "أنثى", 
             "birth_date": "1985-03-10", "specialization": "لغة عربية", "phone": "0555345678"}
        ]
        
        for row, teacher in enumerate(sample_data):
            self.teachers_table.insertRow(row)
            self.teachers_table.setItem(row, 0, QTableWidgetItem(str(teacher["id"])))
            self.teachers_table.setItem(row, 1, QTableWidgetItem(teacher["last_name"]))
            self.teachers_table.setItem(row, 2, QTableWidgetItem(teacher["first_name"]))
            self.teachers_table.setItem(row, 3, QTableWidgetItem(teacher["gender"]))
            self.teachers_table.setItem(row, 4, QTableWidgetItem(teacher["birth_date"]))
            self.teachers_table.setItem(row, 5, QTableWidgetItem(teacher["specialization"]))
            self.teachers_table.setItem(row, 6, QTableWidgetItem(teacher["phone"]))
    
    def filter_teachers(self):
        """تصفية الأساتذة حسب نص البحث"""
        search_text = self.search_input.text().lower()
        for row in range(self.teachers_table.rowCount()):
            match = False
            for col in range(self.teachers_table.columnCount()):
                item = self.teachers_table.item(row, col)
                if item and search_text in item.text().lower():
                    match = True
                    break
            self.teachers_table.setRowHidden(row, not match)
    
    def add_teacher(self):
        """إضافة أستاذ جديد"""
        dialog = TeacherDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # TODO: تنفيذ إضافة الأستاذ إلى قاعدة البيانات
            show_info(self, "إضافة أستاذ", "تم إضافة الأستاذ بنجاح")
            self.load_teachers()
    
    def edit_teacher(self):
        """تعديل بيانات أستاذ"""
        selected_rows = self.teachers_table.selectedItems()
        if not selected_rows:
            show_error(self, "خطأ", "الرجاء اختيار أستاذ للتعديل")
            return
        
        row = selected_rows[0].row()
        teacher_id = int(self.teachers_table.item(row, 0).text())
        
        # TODO: تحميل بيانات الأستاذ من قاعدة البيانات
        teacher_data = {
            "id": teacher_id,
            "last_name": self.teachers_table.item(row, 1).text(),
            "first_name": self.teachers_table.item(row, 2).text(),
            "gender": self.teachers_table.item(row, 3).text(),
            "birth_date": self.teachers_table.item(row, 4).text(),
            "specialization": self.teachers_table.item(row, 5).text(),
            "phone": self.teachers_table.item(row, 6).text()
        }
        
        dialog = TeacherDialog(self, teacher_data)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # TODO: تنفيذ تحديث بيانات الأستاذ في قاعدة البيانات
            show_info(self, "تعديل أستاذ", "تم تعديل بيانات الأستاذ بنجاح")
            self.load_teachers()
    
    def delete_teacher(self):
        """حذف أستاذ"""
        selected_rows = self.teachers_table.selectedItems()
        if not selected_rows:
            show_error(self, "خطأ", "الرجاء اختيار أستاذ للحذف")
            return
        
        row = selected_rows[0].row()
        teacher_id = int(self.teachers_table.item(row, 0).text())
        teacher_name = f"{self.teachers_table.item(row, 2).text()} {self.teachers_table.item(row, 1).text()}"
        
        confirm = QMessageBox.question(
            self, "تأكيد الحذف", 
            f"هل أنت متأكد من حذف الأستاذ {teacher_name}؟",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if confirm == QMessageBox.StandardButton.Yes:
            # TODO: تنفيذ حذف الأستاذ من قاعدة البيانات
            show_info(self, "حذف أستاذ", "تم حذف الأستاذ بنجاح")
            self.load_teachers()
    
    def import_teachers(self):
        """استيراد الأساتذة من ملف"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "اختر ملف الأساتذة", "", "ملفات Excel (*.xlsx *.xls);;ملفات HTML (*.html *.htm);;جميع الملفات (*)"
        )
        
        if not file_path:
            return
        
        try:
            # قراءة الملف
            df = read_excel_file(file_path)
            
            # فتح نافذة تعيين الأعمدة
            dialog = ColumnMappingDialog(self, df.columns.tolist())
            if dialog.exec() == QDialog.DialogCode.Accepted:
                column_mapping = dialog.get_column_mapping()
                
                # TODO: تنفيذ استيراد الأساتذة إلى قاعدة البيانات
                show_info(self, "استيراد الأساتذة", f"تم استيراد {len(df)} أستاذ بنجاح")
                self.load_teachers()
                
        except Exception as e:
            show_error(self, "خطأ في الاستيراد", str(e))
    
    def go_back(self):
        """العودة إلى الصفحة الرئيسية"""
        # TODO: تنفيذ العودة إلى الصفحة الرئيسية
        self.parent().setCurrentIndex(0)  # افتراض أن هذه الواجهة في QStackedWidget


class TeacherDialog(QDialog):
    """نافذة إضافة/تعديل أستاذ"""
    
    def __init__(self, parent=None, teacher_data=None):
        super().__init__(parent)
        self.teacher_data = teacher_data
        self.setWindowTitle("إضافة أستاذ" if not teacher_data else "تعديل أستاذ")
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.setMinimumWidth(500)
        self.setup_ui()
    
    def setup_ui(self):
        """إعداد واجهة المستخدم"""
        main_layout = QVBoxLayout(self)
        
        # إنشاء علامات التبويب
        tab_widget = QTabWidget()
        
        # علامة تبويب البيانات الأساسية
        basic_tab = QWidget()
        basic_layout = QFormLayout(basic_tab)
        
        # حقول البيانات الأساسية
        self.last_name_input = QLineEdit()
        if self.teacher_data:
            self.last_name_input.setText(self.teacher_data["last_name"])
        basic_layout.addRow("اللقب:", self.last_name_input)
        
        self.first_name_input = QLineEdit()
        if self.teacher_data:
            self.first_name_input.setText(self.teacher_data["first_name"])
        basic_layout.addRow("الاسم:", self.first_name_input)
        
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["ذكر", "أنثى"])
        if self.teacher_data:
            self.gender_combo.setCurrentText(self.teacher_data["gender"])
        basic_layout.addRow("الجنس:", self.gender_combo)
        
        self.birth_date_edit = QDateEdit()
        self.birth_date_edit.setCalendarPopup(True)
        self.birth_date_edit.setDisplayFormat("yyyy-MM-dd")
        if self.teacher_data and self.teacher_data["birth_date"]:
            self.birth_date_edit.setDate(QDate.fromString(self.teacher_data["birth_date"], "yyyy-MM-dd"))
        else:
            self.birth_date_edit.setDate(QDate.currentDate().addYears(-30))  # افتراضيًا 30 سنة قبل اليوم
        basic_layout.addRow("تاريخ الميلاد:", self.birth_date_edit)
        
        # إضافة علامة التبويب الأساسية
        tab_widget.addTab(basic_tab, "البيانات الأساسية")
        
        # علامة تبويب البيانات المهنية
        professional_tab = QWidget()
        professional_layout = QFormLayout(professional_tab)
        
        self.specialization_input = QLineEdit()
        if self.teacher_data and "specialization" in self.teacher_data:
            self.specialization_input.setText(self.teacher_data["specialization"])
        professional_layout.addRow("التخصص:", self.specialization_input)
        
        self.phone_input = QLineEdit()
        if self.teacher_data and "phone" in self.teacher_data:
            self.phone_input.setText(self.teacher_data["phone"])
        professional_layout.addRow("رقم الهاتف:", self.phone_input)
        
        self.email_input = QLineEdit()
        if self.teacher_data and "email" in self.teacher_data:
            self.email_input.setText(self.teacher_data["email"])
        professional_layout.addRow("البريد الإلكتروني:", self.email_input)
        
        self.address_input = QLineEdit()
        if self.teacher_data and "address" in self.teacher_data:
            self.address_input.setText(self.teacher_data["address"])
        professional_layout.addRow("العنوان:", self.address_input)
        
        self.hire_date_edit = QDateEdit()
        self.hire_date_edit.setCalendarPopup(True)
        self.hire_date_edit.setDisplayFormat("yyyy-MM-dd")
        if self.teacher_data and "hire_date" in self.teacher_data:
            self.hire_date_edit.setDate(QDate.fromString(self.teacher_data["hire_date"], "yyyy-MM-dd"))
        else:
            self.hire_date_edit.setDate(QDate.currentDate())
        professional_layout.addRow("تاريخ التوظيف:", self.hire_date_edit)
        
        # إضافة علامة التبويب المهنية
        tab_widget.addTab(professional_tab, "البيانات المهنية")
        
        # إضافة علامات التبويب إلى التخطيط الرئيسي
        main_layout.addWidget(tab_widget)
        
        # أزرار الحفظ والإلغاء
        buttons_layout = QHBoxLayout()
        
        self.cancel_button = QPushButton("إلغاء")
        self.cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(self.cancel_button)
        
        self.save_button = QPushButton("حفظ")
        self.save_button.clicked.connect(self.accept)
        buttons_layout.addWidget(self.save_button)
        
        main_layout.addLayout(buttons_layout)
    
    def accept(self):
        """التحقق من البيانات وحفظها"""
        # التحقق من إدخال البيانات الإلزامية
        if not self.last_name_input.text():
            show_error(self, "خطأ", "الرجاء إدخال اللقب")
            return
        
        if not self.first_name_input.text():
            show_error(self, "خطأ", "الرجاء إدخال الاسم")
            return
        
        if not self.specialization_input.text():
            show_error(self, "خطأ", "الرجاء إدخال التخصص")
            return
        
        # TODO: جمع البيانات وإرسالها إلى الكنترولر
        
        super().accept()


class ColumnMappingDialog(QDialog):
    """نافذة تعيين الأعمدة عند استيراد البيانات"""
    
    def __init__(self, parent=None, file_columns=None):
        super().__init__(parent)
        self.file_columns = file_columns or []
        self.setWindowTitle("تعيين الأعمدة")
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.setMinimumWidth(600)
        self.setup_ui()
    
    def setup_ui(self):
        """إعداد واجهة المستخدم"""
        main_layout = QVBoxLayout(self)
        
        # إضافة تعليمات
        instructions = QLabel("قم بتعيين أعمدة الملف إلى حقول قاعدة البيانات المناسبة:")
        main_layout.addWidget(instructions)
        
        # إنشاء نموذج التعيين
        form_layout = QFormLayout()
        
        # قائمة حقول قاعدة البيانات
        db_fields = [
            ("last_name", "اللقب"),
            ("first_name", "الاسم"),
            ("gender", "الجنس"),
            ("birth_date", "تاريخ الميلاد"),
            ("specialization", "التخصص"),
            ("phone_number", "رقم الهاتف"),
            ("email", "البريد الإلكتروني"),
            ("address", "العنوان"),
            ("hire_date", "تاريخ التوظيف")
        ]
        
        # إنشاء قوائم منسدلة لكل حقل
        self.mapping_combos = {}
        for field_key, field_label in db_fields:
            combo = QComboBox()
            combo.addItem("-- لا يوجد --")
            combo.addItems(self.file_columns)
            
            # محاولة تعيين تلقائي للأعمدة المتطابقة
            for i, col in enumerate(self.file_columns):
                if field_label in col or field_key in col.lower():
                    combo.setCurrentIndex(i + 1)  # +1 لتجاوز "-- لا يوجد --"
                    break
            
            form_layout.addRow(field_label + ":", combo)
            self.mapping_combos[field_key] = combo
        
        main_layout.addLayout(form_layout)
        
        # أزرار الحفظ والإلغاء
        buttons_layout = QHBoxLayout()
        
        self.cancel_button = QPushButton("إلغاء")
        self.cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(self.cancel_button)
        
        self.save_button = QPushButton("استيراد")
        self.save_button.clicked.connect(self.accept)
        buttons_layout.addWidget(self.save_button)
        
        main_layout.addLayout(buttons_layout)
    
    def get_column_mapping(self):
        """الحصول على تعيين الأعمدة"""
        mapping = {}
        for field_key, combo in self.mapping_combos.items():
            if combo.currentIndex() > 0:  # تجاوز "-- لا يوجد --"
                mapping[field_key] = combo.currentText()
        return mapping
