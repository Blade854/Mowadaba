#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
واجهة إدارة استدعاءات الأولياء لنظام إدارة المدرسة
"""

import sys
import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
                            QTableWidget, QTableWidgetItem, QLineEdit, QComboBox,
                            QFormLayout, QDateEdit, QTimeEdit, QDialog, QHeaderView,
                            QMessageBox, QGroupBox, QCheckBox, QRadioButton)
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt, QDate, QTime

# إضافة مسار المشروع إلى مسار البحث
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import reshape_arabic, date_to_qdate, qdate_to_date, time_to_qtime, qtime_to_time, show_error, show_info

class ParentSummonWidget(QWidget):
    """واجهة إدارة استدعاءات الأولياء"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.setup_ui()
    
    def setup_ui(self):
        """إعداد واجهة المستخدم"""
        main_layout = QVBoxLayout(self)
        
        # إضافة عنوان الصفحة
        title_label = QLabel("إدارة استدعاءات الأولياء")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # إضافة مجموعة البحث
        search_group = QGroupBox("البحث عن الاستدعاءات")
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
        
        # البحث عن الاستدعاءات المعلقة
        self.pending_radio = QRadioButton("الاستدعاءات المعلقة")
        self.pending_radio.toggled.connect(self.toggle_search_mode)
        search_options_layout.addWidget(self.pending_radio)
        
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
        
        # إخفاء حقول البحث غير المستخدمة في البداية
        for i in range(self.date_search_layout.count()):
            widget = self.date_search_layout.itemAt(i).widget()
            if widget:
                widget.setVisible(False)
        
        self.search_stack.addLayout(self.date_search_layout)
        search_layout.addLayout(self.search_stack)
        
        main_layout.addWidget(search_group)
        
        # إضافة أزرار العمليات
        buttons_layout = QHBoxLayout()
        
        self.add_button = QPushButton("إضافة استدعاء جديد")
        self.add_button.clicked.connect(self.add_summon)
        buttons_layout.addWidget(self.add_button)
        
        self.edit_button = QPushButton("تعديل استدعاء")
        self.edit_button.clicked.connect(self.edit_summon)
        buttons_layout.addWidget(self.edit_button)
        
        self.delete_button = QPushButton("حذف استدعاء")
        self.delete_button.clicked.connect(self.delete_summon)
        buttons_layout.addWidget(self.delete_button)
        
        self.refresh_button = QPushButton("تحديث")
        self.refresh_button.clicked.connect(self.load_summons)
        buttons_layout.addWidget(self.refresh_button)
        
        main_layout.addLayout(buttons_layout)
        
        # إضافة جدول الاستدعاءات
        self.summons_table = QTableWidget()
        self.summons_table.setColumnCount(7)
        self.summons_table.setHorizontalHeaderLabels([
            "رقم الاستدعاء", "اسم التلميذ", "اسم الولي", 
            "المستدعي", "تاريخ الاستدعاء", "الساعة", "الحضور"
        ])
        self.summons_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.summons_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.summons_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.summons_table.itemDoubleClicked.connect(self.edit_summon)
        main_layout.addWidget(self.summons_table)
        
        # إضافة زر العودة
        back_layout = QHBoxLayout()
        self.back_button = QPushButton("العودة إلى الصفحة الرئيسية")
        self.back_button.clicked.connect(self.go_back)
        back_layout.addWidget(self.back_button)
        main_layout.addLayout(back_layout)
        
        # تحميل بيانات الاستدعاءات
        self.load_summons()
    
    def toggle_search_mode(self):
        """تبديل وضع البحث بين التلميذ والتاريخ والاستدعاءات المعلقة"""
        student_mode = self.student_radio.isChecked()
        date_mode = self.date_radio.isChecked()
        pending_mode = self.pending_radio.isChecked()
        
        # تبديل رؤية حقول البحث
        for i in range(self.student_search_layout.count()):
            widget = self.student_search_layout.itemAt(i).widget()
            if widget:
                widget.setVisible(student_mode)
        
        for i in range(self.date_search_layout.count()):
            widget = self.date_search_layout.itemAt(i).widget()
            if widget:
                widget.setVisible(date_mode)
        
        # إذا تم اختيار الاستدعاءات المعلقة، نقوم بالبحث مباشرة
        if pending_mode:
            self.search_pending_summons()
    
    def load_summons(self):
        """تحميل بيانات الاستدعاءات من قاعدة البيانات"""
        # TODO: تنفيذ تحميل بيانات الاستدعاءات من قاعدة البيانات
        # هذه بيانات تجريبية للعرض فقط
        self.summons_table.setRowCount(0)
        
        sample_data = [
            {"id": 1, "student_name": "رهام هبة الله مشري", "parent_name": "والد رهام", 
             "summoner_name": "أحمد محمد", "summon_date": "2023-10-20", "summon_time": "10:30", "attended": True},
            {"id": 2, "student_name": "داوود حميدة", "parent_name": "والد داوود", 
             "summoner_name": "سمير علي", "summon_date": "2023-11-10", "summon_time": "11:45", "attended": False},
            {"id": 3, "student_name": "نورالإيمان رحال", "parent_name": "والد نورالإيمان", 
             "summoner_name": "فاطمة أحمد", "summon_date": "2023-12-05", "summon_time": "09:15", "attended": False}
        ]
        
        for row, summon in enumerate(sample_data):
            self.summons_table.insertRow(row)
            self.summons_table.setItem(row, 0, QTableWidgetItem(str(summon["id"])))
            self.summons_table.setItem(row, 1, QTableWidgetItem(summon["student_name"]))
            self.summons_table.setItem(row, 2, QTableWidgetItem(summon["parent_name"]))
            self.summons_table.setItem(row, 3, QTableWidgetItem(summon["summoner_name"]))
            self.summons_table.setItem(row, 4, QTableWidgetItem(summon["summon_date"]))
            self.summons_table.setItem(row, 5, QTableWidgetItem(summon["summon_time"]))
            self.summons_table.setItem(row, 6, QTableWidgetItem("نعم" if summon["attended"] else "لا"))
    
    def search_by_student(self):
        """البحث عن الاستدعاءات حسب التلميذ"""
        search_text = self.student_search_input.text().lower()
        if not search_text:
            show_error(self, "خطأ", "الرجاء إدخال اسم التلميذ أو الرقم التعريفي")
            return
        
        # TODO: تنفيذ البحث عن الاستدعاءات حسب التلميذ
        # هذا مجرد تصفية للبيانات التجريبية
        for row in range(self.summons_table.rowCount()):
            student_name = self.summons_table.item(row, 1).text().lower()
            self.summons_table.setRowHidden(row, search_text not in student_name)
    
    def search_by_date(self):
        """البحث عن الاستدعاءات حسب التاريخ"""
        search_date = self.date_search_edit.date().toString("yyyy-MM-dd")
        
        # TODO: تنفيذ البحث عن الاستدعاءات حسب التاريخ
        # هذا مجرد تصفية للبيانات التجريبية
        for row in range(self.summons_table.rowCount()):
            summon_date = self.summons_table.item(row, 4).text()
            self.summons_table.setRowHidden(row, summon_date != search_date)
    
    def search_pending_summons(self):
        """البحث عن الاستدعاءات المعلقة (التي لم يحضر فيها الأولياء)"""
        # TODO: تنفيذ البحث عن الاستدعاءات المعلقة
        # هذا مجرد تصفية للبيانات التجريبية
        for row in range(self.summons_table.rowCount()):
            attended = self.summons_table.item(row, 6).text() == "نعم"
            self.summons_table.setRowHidden(row, attended)
    
    def add_summon(self):
        """إضافة استدعاء جديد"""
        dialog = ParentSummonDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # TODO: تنفيذ إضافة الاستدعاء إلى قاعدة البيانات
            show_info(self, "إضافة استدعاء", "تم إضافة الاستدعاء بنجاح")
            self.load_summons()
    
    def edit_summon(self):
        """تعديل بيانات استدعاء"""
        selected_rows = self.summons_table.selectedItems()
        if not selected_rows:
            show_error(self, "خطأ", "الرجاء اختيار استدعاء للتعديل")
            return
        
        row = selected_rows[0].row()
        summon_id = int(self.summons_table.item(row, 0).text())
        
        # TODO: تحميل بيانات الاستدعاء من قاعدة البيانات
        summon_data = {
            "id": summon_id,
            "student_name": self.summons_table.item(row, 1).text(),
            "parent_name": self.summons_table.item(row, 2).text(),
            "summoner_name": self.summons_table.item(row, 3).text(),
            "summon_date": self.summons_table.item(row, 4).text(),
            "summon_time": self.summons_table.item(row, 5).text(),
            "attended": self.summons_table.item(row, 6).text() == "نعم"
        }
        
        dialog = ParentSummonDialog(self, summon_data)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # TODO: تنفيذ تحديث بيانات الاستدعاء في قاعدة البيانات
            show_info(self, "تعديل استدعاء", "تم تعديل بيانات الاستدعاء بنجاح")
            self.load_summons()
    
    def delete_summon(self):
        """حذف استدعاء"""
        selected_rows = self.summons_table.selectedItems()
        if not selected_rows:
            show_error(self, "خطأ", "الرجاء اختيار استدعاء للحذف")
            return
        
        row = selected_rows[0].row()
        summon_id = int(self.summons_table.item(row, 0).text())
        student_name = self.summons_table.item(row, 1).text()
        
        confirm = QMessageBox.question(
            self, "تأكيد الحذف", 
            f"هل أنت متأكد من حذف استدعاء ولي التلميذ {student_name}؟",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if confirm == QMessageBox.StandardButton.Yes:
            # TODO: تنفيذ حذف الاستدعاء من قاعدة البيانات
            show_info(self, "حذف استدعاء", "تم حذف الاستدعاء بنجاح")
            self.load_summons()
    
    def go_back(self):
        """العودة إلى الصفحة الرئيسية"""
        # TODO: تنفيذ العودة إلى الصفحة الرئيسية
        self.parent().setCurrentIndex(0)  # افتراض أن هذه الواجهة في QStackedWidget


class ParentSummonDialog(QDialog):
    """نافذة إضافة/تعديل استدعاء ولي"""
    
    def __init__(self, parent=None, summon_data=None):
        super().__init__(parent)
        self.summon_data = summon_data
        self.setWindowTitle("إضافة استدعاء جديد" if not summon_data else "تعديل استدعاء")
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
        if self.summon_data:
            self.student_combo.setCurrentText(self.summon_data["student_name"])
            self.student_combo.setEnabled(False)  # تعطيل تغيير التلميذ عند التعديل
        form_layout.addRow("التلميذ:", self.student_combo)
        
        # اسم الولي
        self.parent_name_input = QLineEdit()
        if self.summon_data:
            self.parent_name_input.setText(self.summon_data["parent_name"])
        form_layout.addRow("اسم الولي:", self.parent_name_input)
        
        # المستدعي
        self.summoner_name_input = QLineEdit()
        if self.summon_data:
            self.summoner_name_input.setText(self.summon_data["summoner_name"])
        form_layout.addRow("المستدعي:", self.summoner_name_input)
        
        # تاريخ الاستدعاء
        self.summon_date_edit = QDateEdit()
        self.summon_date_edit.setCalendarPopup(True)
        self.summon_date_edit.setDisplayFormat("yyyy-MM-dd")
        if self.summon_data and self.summon_data["summon_date"]:
            self.summon_date_edit.setDate(QDate.fromString(self.summon_data["summon_date"], "yyyy-MM-dd"))
        else:
            self.summon_date_edit.setDate(QDate.currentDate().addDays(1))  # افتراضيًا اليوم التالي
        form_layout.addRow("تاريخ الاستدعاء:", self.summon_date_edit)
        
        # ساعة الاستدعاء
        self.summon_time_edit = QTimeEdit()
        self.summon_time_edit.setDisplayFormat("hh:mm")
        if self.summon_data and self.summon_data["summon_time"]:
            self.summon_time_edit.setTime(QTime.fromString(self.summon_data["summon_time"], "hh:mm"))
        else:
            self.summon_time_edit.setTime(QTime(10, 0))  # افتراضيًا الساعة 10:00
        form_layout.addRow("الساعة:", self.summon_time_edit)
        
        # حضور الولي
        self.attended_check = QCheckBox("نعم")
        if self.summon_data:
            self.attended_check.setChecked(self.summon_data["attended"])
        form_layout.addRow("الحضور:", self.attended_check)
        
        # ملاحظات
        self.notes_input = QLineEdit()
        if self.summon_data and "notes" in self.summon_data:
            self.notes_input.setText(self.summon_data["notes"])
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
        
        # التحقق من إدخال اسم الولي
        if not self.parent_name_input.text():
            show_error(self, "خطأ", "الرجاء إدخال اسم الولي")
            return
        
        # التحقق من إدخال اسم المستدعي
        if not self.summoner_name_input.text():
            show_error(self, "خطأ", "الرجاء إدخال اسم المستدعي")
            return
        
        # TODO: جمع البيانات وإرسالها إلى الكنترولر
        
        super().accept()
