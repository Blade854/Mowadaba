#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
واجهة إدارة التلاميذ لنظام إدارة المدرسة
"""

import sys
import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
                            QTableWidget, QTableWidgetItem, QLineEdit, QComboBox,
                            QFormLayout, QDateEdit, QDialog, QFileDialog, QHeaderView,
                            QMessageBox, QTabWidget, QGroupBox, QCheckBox, QSpinBox)
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt, QDate

# إضافة مسار المشروع إلى مسار البحث
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import reshape_arabic, date_to_qdate, qdate_to_date, show_error, show_info, read_excel_file, map_columns

class StudentManagementWidget(QWidget):
    """واجهة إدارة التلاميذ"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.setup_ui()
    
    def setup_ui(self):
        """إعداد واجهة المستخدم"""
        main_layout = QVBoxLayout(self)
        
        # إضافة عنوان الصفحة
        title_label = QLabel("إدارة التلاميذ")
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
        self.search_input.setPlaceholderText("أدخل اسم التلميذ أو الرقم التعريفي...")
        self.search_input.textChanged.connect(self.filter_students)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        main_layout.addLayout(search_layout)
        
        # إضافة أزرار العمليات
        buttons_layout = QHBoxLayout()
        
        self.add_button = QPushButton("إضافة تلميذ")
        self.add_button.clicked.connect(self.add_student)
        buttons_layout.addWidget(self.add_button)
        
        self.edit_button = QPushButton("تعديل تلميذ")
        self.edit_button.clicked.connect(self.edit_student)
        buttons_layout.addWidget(self.edit_button)
        
        self.delete_button = QPushButton("حذف تلميذ")
        self.delete_button.clicked.connect(self.delete_student)
        buttons_layout.addWidget(self.delete_button)
        
        self.import_button = QPushButton("استيراد من ملف")
        self.import_button.clicked.connect(self.import_students)
        buttons_layout.addWidget(self.import_button)
        
        self.refresh_button = QPushButton("تحديث")
        self.refresh_button.clicked.connect(self.load_students)
        buttons_layout.addWidget(self.refresh_button)
        
        main_layout.addLayout(buttons_layout)
        
        # إضافة جدول التلاميذ
        self.students_table = QTableWidget()
        self.students_table.setColumnCount(8)
        self.students_table.setHorizontalHeaderLabels([
            "الرقم التعريفي", "اللقب", "الاسم", "الجنس", 
            "تاريخ الميلاد", "السنة", "الشعبة", "القسم"
        ])
        self.students_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.students_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.students_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.students_table.itemDoubleClicked.connect(self.edit_student)
        main_layout.addWidget(self.students_table)
        
        # إضافة زر العودة
        back_layout = QHBoxLayout()
        self.back_button = QPushButton("العودة إلى الصفحة الرئيسية")
        self.back_button.clicked.connect(self.go_back)
        back_layout.addWidget(self.back_button)
        main_layout.addLayout(back_layout)
        
        # تحميل بيانات التلاميذ
        self.load_students()
    
    def load_students(self):
        """تحميل بيانات التلاميذ من قاعدة البيانات"""
        # TODO: تنفيذ تحميل بيانات التلاميذ من قاعدة البيانات
        # هذه بيانات تجريبية للعرض فقط
        self.students_table.setRowCount(0)
        
        sample_data = [
            {"id": "1100912010068100", "last_name": "مشري", "first_name": "رهام هبة الله", "gender": "أنثى", 
             "birth_date": "2009-02-04", "year": "أولى", "section": "جدع مشترك آداب", "class": "1"},
            {"id": "1000812030242600", "last_name": "حميدة", "first_name": "داوود", "gender": "ذكر", 
             "birth_date": "2008-05-16", "year": "أولى", "section": "جدع مشترك آداب", "class": "1"},
            {"id": "1100912150000300", "last_name": "رحال", "first_name": "نورالإيمان", "gender": "أنثى", 
             "birth_date": "2009-02-17", "year": "أولى", "section": "جدع مشترك آداب", "class": "1"}
        ]
        
        for row, student in enumerate(sample_data):
            self.students_table.insertRow(row)
            self.students_table.setItem(row, 0, QTableWidgetItem(student["id"]))
            self.students_table.setItem(row, 1, QTableWidgetItem(student["last_name"]))
            self.students_table.setItem(row, 2, QTableWidgetItem(student["first_name"]))
            self.students_table.setItem(row, 3, QTableWidgetItem(student["gender"]))
            self.students_table.setItem(row, 4, QTableWidgetItem(student["birth_date"]))
            self.students_table.setItem(row, 5, QTableWidgetItem(student["year"]))
            self.students_table.setItem(row, 6, QTableWidgetItem(student["section"]))
            self.students_table.setItem(row, 7, QTableWidgetItem(student["class"]))
    
    def filter_students(self):
        """تصفية التلاميذ حسب نص البحث"""
        search_text = self.search_input.text().lower()
        for row in range(self.students_table.rowCount()):
            match = False
            for col in range(self.students_table.columnCount()):
                item = self.students_table.item(row, col)
                if item and search_text in item.text().lower():
                    match = True
                    break
            self.students_table.setRowHidden(row, not match)
    
    def add_student(self):
        """إضافة تلميذ جديد"""
        dialog = StudentDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # TODO: تنفيذ إضافة التلميذ إلى قاعدة البيانات
            show_info(self, "إضافة تلميذ", "تم إضافة التلميذ بنجاح")
            self.load_students()
    
    def edit_student(self):
        """تعديل بيانات تلميذ"""
        selected_rows = self.students_table.selectedItems()
        if not selected_rows:
            show_error(self, "خطأ", "الرجاء اختيار تلميذ للتعديل")
            return
        
        row = selected_rows[0].row()
        student_id = self.students_table.item(row, 0).text()
        
        # TODO: تحميل بيانات التلميذ من قاعدة البيانات
        student_data = {
            "id": student_id,
            "last_name": self.students_table.item(row, 1).text(),
            "first_name": self.students_table.item(row, 2).text(),
            "gender": self.students_table.item(row, 3).text(),
            "birth_date": self.students_table.item(row, 4).text(),
            "year": self.students_table.item(row, 5).text(),
            "section": self.students_table.item(row, 6).text(),
            "class": self.students_table.item(row, 7).text()
        }
        
        dialog = StudentDialog(self, student_data)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # TODO: تنفيذ تحديث بيانات التلميذ في قاعدة البيانات
            show_info(self, "تعديل تلميذ", "تم تعديل بيانات التلميذ بنجاح")
            self.load_students()
    
    def delete_student(self):
        """حذف تلميذ"""
        selected_rows = self.students_table.selectedItems()
        if not selected_rows:
            show_error(self, "خطأ", "الرجاء اختيار تلميذ للحذف")
            return
        
        row = selected_rows[0].row()
        student_id = self.students_table.item(row, 0).text()
        student_name = f"{self.students_table.item(row, 2).text()} {self.students_table.item(row, 1).text()}"
        
        confirm = QMessageBox.question(
            self, "تأكيد الحذف", 
            f"هل أنت متأكد من حذف التلميذ {student_name}؟\n"
            "سيتم حذف جميع البيانات المرتبطة بهذا التلميذ (الشهادات الطبية، التقارير، الاستدعاءات).",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if confirm == QMessageBox.StandardButton.Yes:
            # TODO: تنفيذ حذف التلميذ من قاعدة البيانات
            show_info(self, "حذف تلميذ", "تم حذف التلميذ بنجاح")
            self.load_students()
    
    def import_students(self):
        """استيراد التلاميذ من ملف"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "اختر ملف التلاميذ", "", "ملفات Excel (*.xlsx *.xls);;ملفات HTML (*.html *.htm);;جميع الملفات (*)"
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
                
                # TODO: تنفيذ استيراد التلاميذ إلى قاعدة البيانات
                show_info(self, "استيراد التلاميذ", f"تم استيراد {len(df)} تلميذ بنجاح")
                self.load_students()
                
        except Exception as e:
            show_error(self, "خطأ في الاستيراد", str(e))
    
    def go_back(self):
        """العودة إلى الصفحة الرئيسية"""
        # TODO: تنفيذ العودة إلى الصفحة الرئيسية
        self.parent().setCurrentIndex(0)  # افتراض أن هذه الواجهة في QStackedWidget


class StudentDialog(QDialog):
    """نافذة إضافة/تعديل تلميذ"""
    
    def __init__(self, parent=None, student_data=None):
        super().__init__(parent)
        self.student_data = student_data
        self.setWindowTitle("إضافة تلميذ" if not student_data else "تعديل تلميذ")
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
        self.id_input = QLineEdit()
        if self.student_data:
            self.id_input.setText(self.student_data["id"])
            self.id_input.setReadOnly(True)
        basic_layout.addRow("الرقم التعريفي:", self.id_input)
        
        self.last_name_input = QLineEdit()
        if self.student_data:
            self.last_name_input.setText(self.student_data["last_name"])
        basic_layout.addRow("اللقب:", self.last_name_input)
        
        self.first_name_input = QLineEdit()
        if self.student_data:
            self.first_name_input.setText(self.student_data["first_name"])
        basic_layout.addRow("الاسم:", self.first_name_input)
        
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["ذكر", "أنثى"])
        if self.student_data:
            self.gender_combo.setCurrentText(self.student_data["gender"])
        basic_layout.addRow("الجنس:", self.gender_combo)
        
        self.birth_date_edit = QDateEdit()
        self.birth_date_edit.setCalendarPopup(True)
        self.birth_date_edit.setDisplayFormat("yyyy-MM-dd")
        if self.student_data and self.student_data["birth_date"]:
            self.birth_date_edit.setDate(QDate.fromString(self.student_data["birth_date"], "yyyy-MM-dd"))
        else:
            self.birth_date_edit.setDate(QDate.currentDate())
        basic_layout.addRow("تاريخ الميلاد:", self.birth_date_edit)
        
        self.birth_place_input = QLineEdit()
        if self.student_data and "birth_place" in self.student_data:
            self.birth_place_input.setText(self.student_data["birth_place"])
        basic_layout.addRow("مكان الميلاد:", self.birth_place_input)
        
        # إضافة علامة التبويب الأساسية
        tab_widget.addTab(basic_tab, "البيانات الأساسية")
        
        # علامة تبويب البيانات الدراسية
        academic_tab = QWidget()
        academic_layout = QFormLayout(academic_tab)
        
        self.year_combo = QComboBox()
        self.year_combo.addItems(["أولى", "ثانية", "ثالثة"])
        if self.student_data and "year" in self.student_data:
            self.year_combo.setCurrentText(self.student_data["year"])
        academic_layout.addRow("السنة:", self.year_combo)
        
        self.section_combo = QComboBox()
        self.section_combo.addItems(["جدع مشترك آداب", "جدع مشترك علوم", "آداب وفلسفة", "علوم تجريبية", "رياضيات", "تقني رياضي"])
        if self.student_data and "section" in self.student_data:
            self.section_combo.setCurrentText(self.student_data["section"])
        academic_layout.addRow("الشعبة:", self.section_combo)
        
        self.class_input = QLineEdit()
        if self.student_data and "class" in self.student_data:
            self.class_input.setText(self.student_data["class"])
        academic_layout.addRow("القسم:", self.class_input)
        
        self.study_system_combo = QComboBox()
        self.study_system_combo.addItems(["خارجي", "نصف داخلي", "داخلي"])
        if self.student_data and "study_system" in self.student_data:
            self.study_system_combo.setCurrentText(self.student_data["study_system"])
        academic_layout.addRow("نظام التمدرس:", self.study_system_combo)
        
        # إضافة علامة التبويب الدراسية
        tab_widget.addTab(academic_tab, "البيانات الدراسية")
        
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
        if not self.id_input.text():
            show_error(self, "خطأ", "الرجاء إدخال الرقم التعريفي")
            return
        
        if not self.last_name_input.text():
            show_error(self, "خطأ", "الرجاء إدخال اللقب")
            return
        
        if not self.first_name_input.text():
            show_error(self, "خطأ", "الرجاء إدخال الاسم")
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
            ("student_id", "الرقم التعريفي"),
            ("last_name", "اللقب"),
            ("first_name", "الاسم"),
            ("gender", "الجنس"),
            ("birth_date", "تاريخ الميلاد"),
            ("birth_place", "مكان الميلاد"),
            ("academic_year", "السنة الدراسية"),
            ("section", "الشعبة"),
            ("class_number", "القسم"),
            ("study_system", "نظام التمدرس")
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
