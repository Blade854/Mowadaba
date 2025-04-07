#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
واجهة إدارة الشهادات الطبية لنظام إدارة المدرسة
"""

import sys
import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
                            QTableWidget, QTableWidgetItem, QLineEdit, QComboBox,
                            QFormLayout, QDateEdit, QDialog, QCheckBox, QHeaderView,
                            QMessageBox, QGroupBox, QRadioButton, QSpinBox)
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt, QDate

# إضافة مسار المشروع إلى مسار البحث
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import reshape_arabic, date_to_qdate, qdate_to_date, show_error, show_info

class MedicalCertificateWidget(QWidget):
    """واجهة إدارة الشهادات الطبية"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.setup_ui()
    
    def setup_ui(self):
        """إعداد واجهة المستخدم"""
        main_layout = QVBoxLayout(self)
        
        # إضافة عنوان الصفحة
        title_label = QLabel("إدارة الشهادات الطبية")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # إضافة مجموعة البحث
        search_group = QGroupBox("البحث عن الشهادات الطبية")
        search_layout = QVBoxLayout(search_group)
        
        # إضافة خيارات البحث
        search_options_layout = QHBoxLayout()
        
        # البحث حسب التلميذ
        self.student_radio = QRadioButton("بحث حسب التلميذ")
        self.student_radio.setChecked(True)
        self.student_radio.toggled.connect(self.toggle_search_mode)
        search_options_layout.addWidget(self.student_radio)
        
        # البحث حسب التاريخ
        self.date_radio = QRadioButton("بحث حسب التاريخ")
        self.date_radio.toggled.connect(self.toggle_search_mode)
        search_options_layout.addWidget(self.date_radio)
        
        search_layout.addLayout(search_options_layout)
        
        # حقول البحث
        self.search_stack = QVBoxLayout()
        
        # حقل البحث عن التلميذ
        self.student_search_layout = QHBoxLayout()
        self.student_search_input = QLineEdit()
        self.student_search_input.setPlaceholderText("أدخل اسم التلميذ أو الرقم التعريفي...")
        self.student_search_button = QPushButton("بحث")
        self.student_search_button.clicked.connect(self.search_by_student)
        self.student_search_layout.addWidget(QLabel("التلميذ:"))
        self.student_search_layout.addWidget(self.student_search_input)
        self.student_search_layout.addWidget(self.student_search_button)
        self.search_stack.addLayout(self.student_search_layout)
        
        # حقل البحث حسب التاريخ
        self.date_search_layout = QHBoxLayout()
        self.date_search_edit = QDateEdit()
        self.date_search_edit.setCalendarPopup(True)
        self.date_search_edit.setDisplayFormat("yyyy-MM-dd")
        self.date_search_edit.setDate(QDate.currentDate())
        self.date_search_button = QPushButton("بحث")
        self.date_search_button.clicked.connect(self.search_by_date)
        self.date_search_layout.addWidget(QLabel("التاريخ:"))
        self.date_search_layout.addWidget(self.date_search_edit)
        self.date_search_layout.addWidget(self.date_search_button)
        
        # إخفاء حقل البحث بالتاريخ في البداية
        for i in range(self.date_search_layout.count()):
            widget = self.date_search_layout.itemAt(i).widget()
            if widget:
                widget.setVisible(False)
        
        self.search_stack.addLayout(self.date_search_layout)
        search_layout.addLayout(self.search_stack)
        
        main_layout.addWidget(search_group)
        
        # إضافة أزرار العمليات
        buttons_layout = QHBoxLayout()
        
        self.add_button = QPushButton("إضافة شهادة طبية")
        self.add_button.clicked.connect(self.add_certificate)
        buttons_layout.addWidget(self.add_button)
        
        self.edit_button = QPushButton("تعديل شهادة طبية")
        self.edit_button.clicked.connect(self.edit_certificate)
        buttons_layout.addWidget(self.edit_button)
        
        self.delete_button = QPushButton("حذف شهادة طبية")
        self.delete_button.clicked.connect(self.delete_certificate)
        buttons_layout.addWidget(self.delete_button)
        
        self.refresh_button = QPushButton("تحديث")
        self.refresh_button.clicked.connect(self.load_certificates)
        buttons_layout.addWidget(self.refresh_button)
        
        main_layout.addLayout(buttons_layout)
        
        # إضافة جدول الشهادات الطبية
        self.certificates_table = QTableWidget()
        self.certificates_table.setColumnCount(7)
        self.certificates_table.setHorizontalHeaderLabels([
            "رقم الشهادة", "اسم التلميذ", "تاريخ البداية", 
            "تاريخ النهاية", "تاريخ الاستلام", "مؤشرة من الطب المدرسي", "سلمت من طرف الولي"
        ])
        self.certificates_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.certificates_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.certificates_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.certificates_table.itemDoubleClicked.connect(self.edit_certificate)
        main_layout.addWidget(self.certificates_table)
        
        # إضافة زر العودة
        back_layout = QHBoxLayout()
        self.back_button = QPushButton("العودة إلى الصفحة الرئيسية")
        self.back_button.clicked.connect(self.go_back)
        back_layout.addWidget(self.back_button)
        main_layout.addLayout(back_layout)
        
        # تحميل بيانات الشهادات الطبية
        self.load_certificates()
    
    def toggle_search_mode(self):
        """تبديل وضع البحث بين التلميذ والتاريخ"""
        student_mode = self.student_radio.isChecked()
        
        # تبديل رؤية حقول البحث
        for i in range(self.student_search_layout.count()):
            widget = self.student_search_layout.itemAt(i).widget()
            if widget:
                widget.setVisible(student_mode)
        
        for i in range(self.date_search_layout.count()):
            widget = self.date_search_layout.itemAt(i).widget()
            if widget:
                widget.setVisible(not student_mode)
    
    def load_certificates(self):
        """تحميل بيانات الشهادات الطبية من قاعدة البيانات"""
        # TODO: تنفيذ تحميل بيانات الشهادات الطبية من قاعدة البيانات
        # هذه بيانات تجريبية للعرض فقط
        self.certificates_table.setRowCount(0)
        
        sample_data = [
            {"id": 1, "student_name": "رهام هبة الله مشري", "start_date": "2023-10-15", 
             "end_date": "2023-10-20", "receipt_date": "2023-10-16", "doctor_verified": True, "parent_delivered": True},
            {"id": 2, "student_name": "داوود حميدة", "start_date": "2023-11-05", 
             "end_date": "2023-11-10", "receipt_date": "2023-11-06", "doctor_verified": False, "parent_delivered": True},
            {"id": 3, "student_name": "نورالإيمان رحال", "start_date": "2023-12-01", 
             "end_date": "2023-12-03", "receipt_date": "2023-12-02", "doctor_verified": True, "parent_delivered": False}
        ]
        
        for row, certificate in enumerate(sample_data):
            self.certificates_table.insertRow(row)
            self.certificates_table.setItem(row, 0, QTableWidgetItem(str(certificate["id"])))
            self.certificates_table.setItem(row, 1, QTableWidgetItem(certificate["student_name"]))
            self.certificates_table.setItem(row, 2, QTableWidgetItem(certificate["start_date"]))
            self.certificates_table.setItem(row, 3, QTableWidgetItem(certificate["end_date"]))
            self.certificates_table.setItem(row, 4, QTableWidgetItem(certificate["receipt_date"]))
            self.certificates_table.setItem(row, 5, QTableWidgetItem("نعم" if certificate["doctor_verified"] else "لا"))
            self.certificates_table.setItem(row, 6, QTableWidgetItem("نعم" if certificate["parent_delivered"] else "لا"))
    
    def search_by_student(self):
        """البحث عن الشهادات الطبية حسب التلميذ"""
        search_text = self.student_search_input.text().lower()
        if not search_text:
            show_error(self, "خطأ", "الرجاء إدخال اسم التلميذ أو الرقم التعريفي")
            return
        
        # TODO: تنفيذ البحث عن الشهادات الطبية حسب التلميذ
        # هذا مجرد تصفية للبيانات التجريبية
        for row in range(self.certificates_table.rowCount()):
            student_name = self.certificates_table.item(row, 1).text().lower()
            self.certificates_table.setRowHidden(row, search_text not in student_name)
    
    def search_by_date(self):
        """البحث عن الشهادات الطبية حسب التاريخ"""
        search_date = self.date_search_edit.date().toString("yyyy-MM-dd")
        
        # TODO: تنفيذ البحث عن الشهادات الطبية حسب التاريخ
        # هذا مجرد تصفية للبيانات التجريبية
        for row in range(self.certificates_table.rowCount()):
            start_date = self.certificates_table.item(row, 2).text()
            end_date = self.certificates_table.item(row, 3).text()
            
            # التحقق مما إذا كان التاريخ المحدد يقع ضمن فترة الشهادة الطبية
            is_in_range = start_date <= search_date <= end_date
            self.certificates_table.setRowHidden(row, not is_in_range)
    
    def add_certificate(self):
        """إضافة شهادة طبية جديدة"""
        dialog = MedicalCertificateDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # TODO: تنفيذ إضافة الشهادة الطبية إلى قاعدة البيانات
            show_info(self, "إضافة شهادة طبية", "تم إضافة الشهادة الطبية بنجاح")
            self.load_certificates()
    
    def edit_certificate(self):
        """تعديل بيانات شهادة طبية"""
        selected_rows = self.certificates_table.selectedItems()
        if not selected_rows:
            show_error(self, "خطأ", "الرجاء اختيار شهادة طبية للتعديل")
            return
        
        row = selected_rows[0].row()
        certificate_id = int(self.certificates_table.item(row, 0).text())
        
        # TODO: تحميل بيانات الشهادة الطبية من قاعدة البيانات
        certificate_data = {
            "id": certificate_id,
            "student_name": self.certificates_table.item(row, 1).text(),
            "start_date": self.certificates_table.item(row, 2).text(),
            "end_date": self.certificates_table.item(row, 3).text(),
            "receipt_date": self.certificates_table.item(row, 4).text(),
            "doctor_verified": self.certificates_table.item(row, 5).text() == "نعم",
            "parent_delivered": self.certificates_table.item(row, 6).text() == "نعم"
        }
        
        dialog = MedicalCertificateDialog(self, certificate_data)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # TODO: تنفيذ تحديث بيانات الشهادة الطبية في قاعدة البيانات
            show_info(self, "تعديل شهادة طبية", "تم تعديل بيانات الشهادة الطبية بنجاح")
            self.load_certificates()
    
    def delete_certificate(self):
        """حذف شهادة طبية"""
        selected_rows = self.certificates_table.selectedItems()
        if not selected_rows:
            show_error(self, "خطأ", "الرجاء اختيار شهادة طبية للحذف")
            return
        
        row = selected_rows[0].row()
        certificate_id = int(self.certificates_table.item(row, 0).text())
        student_name = self.certificates_table.item(row, 1).text()
        
        confirm = QMessageBox.question(
            self, "تأكيد الحذف", 
            f"هل أنت متأكد من حذف الشهادة الطبية للتلميذ {student_name}؟",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if confirm == QMessageBox.StandardButton.Yes:
            # TODO: تنفيذ حذف الشهادة الطبية من قاعدة البيانات
            show_info(self, "حذف شهادة طبية", "تم حذف الشهادة الطبية بنجاح")
            self.load_certificates()
    
    def go_back(self):
        """العودة إلى الصفحة الرئيسية"""
        # TODO: تنفيذ العودة إلى الصفحة الرئيسية
        self.parent().setCurrentIndex(0)  # افتراض أن هذه الواجهة في QStackedWidget


class MedicalCertificateDialog(QDialog):
    """نافذة إضافة/تعديل شهادة طبية"""
    
    def __init__(self, parent=None, certificate_data=None):
        super().__init__(parent)
        self.certificate_data = certificate_data
        self.setWindowTitle("إضافة شهادة طبية" if not certificate_data else "تعديل شهادة طبية")
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.setMinimumWidth(500)
        self.setup_ui()
    
    def setup_ui(self):
        """إعداد واجهة المستخدم"""
        main_layout = QVBoxLayout(self)
        
        form_layout = QFormLayout()
        
        # اختيار التلميذ
        self.student_combo = QComboBox()
        # TODO: تحميل قائمة التلاميذ من قاعدة البيانات
        self.student_combo.addItems(["رهام هبة الله مشري", "داوود حميدة", "نورالإيمان رحال"])
        if self.certificate_data:
            self.student_combo.setCurrentText(self.certificate_data["student_name"])
            self.student_combo.setEnabled(False)  # تعطيل تغيير التلميذ عند التعديل
        form_layout.addRow("التلميذ:", self.student_combo)
        
        # تاريخ بداية الشهادة الطبية
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDisplayFormat("yyyy-MM-dd")
        if self.certificate_data and self.certificate_data["start_date"]:
            self.start_date_edit.setDate(QDate.fromString(self.certificate_data["start_date"], "yyyy-MM-dd"))
        else:
            self.start_date_edit.setDate(QDate.currentDate())
        form_layout.addRow("تاريخ البداية:", self.start_date_edit)
        
        # تاريخ نهاية الشهادة الطبية
        self.end_date_edit = QDateEdit()
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setDisplayFormat("yyyy-MM-dd")
        if self.certificate_data and self.certificate_data["end_date"]:
            self.end_date_edit.setDate(QDate.fromString(self.certificate_data["end_date"], "yyyy-MM-dd"))
        else:
            self.end_date_edit.setDate(QDate.currentDate().addDays(3))  # افتراضيًا 3 أيام
        form_layout.addRow("تاريخ النهاية:", self.end_date_edit)
        
        # تاريخ استلام الشهادة الطبية
        self.receipt_date_edit = QDateEdit()
        self.receipt_date_edit.setCalendarPopup(True)
        self.receipt_date_edit.setDisplayFormat("yyyy-MM-dd")
        if self.certificate_data and self.certificate_data["receipt_date"]:
            self.receipt_date_edit.setDate(QDate.fromString(self.certificate_data["receipt_date"], "yyyy-MM-dd"))
        else:
            self.receipt_date_edit.setDate(QDate.currentDate())
        form_layout.addRow("تاريخ الاستلام:", self.receipt_date_edit)
        
        # مؤشرة من الطب المدرسي
        self.doctor_verified_check = QCheckBox("نعم")
        if self.certificate_data:
            self.doctor_verified_check.setChecked(self.certificate_data["doctor_verified"])
        form_layout.addRow("مؤشرة من الطب المدرسي:", self.doctor_verified_check)
        
        # سلمت من طرف الولي
        self.parent_delivered_check = QCheckBox("نعم")
        if self.certificate_data:
            self.parent_delivered_check.setChecked(self.certificate_data["parent_delivered"])
        form_layout.addRow("سلمت من طرف الولي:", self.parent_delivered_check)
        
        # ملاحظات
        self.notes_input = QLineEdit()
        if self.certificate_data and "notes" in self.certificate_data:
            self.notes_input.setText(self.certificate_data["notes"])
        form_layout.addRow("ملاحظات:", self.notes_input)
        
        main_layout.addLayout(form_layout)
        
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
        # التحقق من اختيار تلميذ
        if self.student_combo.currentIndex() == -1:
            show_error(self, "خطأ", "الرجاء اختيار تلميذ")
            return
        
        # التحقق من صحة التواريخ
        start_date = self.start_date_edit.date()
        end_date = self.end_date_edit.date()
        receipt_date = self.receipt_date_edit.date()
        
        if start_date > end_date:
            show_error(self, "خطأ", "تاريخ البداية يجب أن يكون قبل تاريخ النهاية")
            return
        
        # TODO: جمع البيانات وإرسالها إلى الكنترولر
        
        super().accept()
