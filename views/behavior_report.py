#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
واجهة إدارة التقارير السلوكية لنظام إدارة المدرسة
"""

import sys
import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
                            QTableWidget, QTableWidgetItem, QLineEdit, QComboBox,
                            QFormLayout, QDateEdit, QTimeEdit, QDialog, QHeaderView,
                            QMessageBox, QGroupBox, QCheckBox, QListWidget, QTextEdit)
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt, QDate, QTime

# إضافة مسار المشروع إلى مسار البحث
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import reshape_arabic, date_to_qdate, qdate_to_date, time_to_qtime, qtime_to_time, show_error, show_info

class BehaviorReportWidget(QWidget):
    """واجهة إدارة التقارير السلوكية"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.setup_ui()
    
    def setup_ui(self):
        """إعداد واجهة المستخدم"""
        main_layout = QVBoxLayout(self)
        
        # إضافة عنوان الصفحة
        title_label = QLabel("إدارة التقارير السلوكية")
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
        self.search_input.textChanged.connect(self.filter_reports)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        main_layout.addLayout(search_layout)
        
        # إضافة أزرار العمليات
        buttons_layout = QHBoxLayout()
        
        self.add_button = QPushButton("إضافة تقرير جديد")
        self.add_button.clicked.connect(self.add_report)
        buttons_layout.addWidget(self.add_button)
        
        self.edit_button = QPushButton("تعديل تقرير")
        self.edit_button.clicked.connect(self.edit_report)
        buttons_layout.addWidget(self.edit_button)
        
        self.delete_button = QPushButton("حذف تقرير")
        self.delete_button.clicked.connect(self.delete_report)
        buttons_layout.addWidget(self.delete_button)
        
        self.refresh_button = QPushButton("تحديث")
        self.refresh_button.clicked.connect(self.load_reports)
        buttons_layout.addWidget(self.refresh_button)
        
        main_layout.addLayout(buttons_layout)
        
        # إضافة جدول التقارير
        self.reports_table = QTableWidget()
        self.reports_table.setColumnCount(7)
        self.reports_table.setHorizontalHeaderLabels([
            "رقم التقرير", "اسم التلميذ", "صاحب التقرير", 
            "الوظيفة", "تاريخ التقرير", "الساعة", "الإجراءات المتخذة"
        ])
        self.reports_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.reports_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.reports_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.reports_table.itemDoubleClicked.connect(self.edit_report)
        main_layout.addWidget(self.reports_table)
        
        # إضافة زر العودة
        back_layout = QHBoxLayout()
        self.back_button = QPushButton("العودة إلى الصفحة الرئيسية")
        self.back_button.clicked.connect(self.go_back)
        back_layout.addWidget(self.back_button)
        main_layout.addLayout(back_layout)
        
        # تحميل بيانات التقارير
        self.load_reports()
    
    def load_reports(self):
        """تحميل بيانات التقارير من قاعدة البيانات"""
        # TODO: تنفيذ تحميل بيانات التقارير من قاعدة البيانات
        # هذه بيانات تجريبية للعرض فقط
        self.reports_table.setRowCount(0)
        
        sample_data = [
            {"id": 1, "student_name": "رهام هبة الله مشري", "reporter_name": "أحمد محمد", 
             "reporter_role": "أستاذ", "report_date": "2023-10-15", "report_time": "10:30", 
             "actions": "إنذار شفهي، توبيخ"},
            {"id": 2, "student_name": "داوود حميدة", "reporter_name": "سمير علي", 
             "reporter_role": "مستشار التربية", "report_date": "2023-11-05", "report_time": "11:45", 
             "actions": "إنذار كتابي، استدعاء الولي"},
            {"id": 3, "student_name": "نورالإيمان رحال", "reporter_name": "فاطمة أحمد", 
             "reporter_role": "مشرف", "report_date": "2023-12-01", "report_time": "09:15", 
             "actions": "عرض على لجنة الإرشاد والمتابعة"}
        ]
        
        for row, report in enumerate(sample_data):
            self.reports_table.insertRow(row)
            self.reports_table.setItem(row, 0, QTableWidgetItem(str(report["id"])))
            self.reports_table.setItem(row, 1, QTableWidgetItem(report["student_name"]))
            self.reports_table.setItem(row, 2, QTableWidgetItem(report["reporter_name"]))
            self.reports_table.setItem(row, 3, QTableWidgetItem(report["reporter_role"]))
            self.reports_table.setItem(row, 4, QTableWidgetItem(report["report_date"]))
            self.reports_table.setItem(row, 5, QTableWidgetItem(report["report_time"]))
            self.reports_table.setItem(row, 6, QTableWidgetItem(report["actions"]))
    
    def filter_reports(self):
        """تصفية التقارير حسب نص البحث"""
        search_text = self.search_input.text().lower()
        for row in range(self.reports_table.rowCount()):
            match = False
            for col in range(self.reports_table.columnCount()):
                item = self.reports_table.item(row, col)
                if item and search_text in item.text().lower():
                    match = True
                    break
            self.reports_table.setRowHidden(row, not match)
    
    def add_report(self):
        """إضافة تقرير جديد"""
        dialog = BehaviorReportDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # TODO: تنفيذ إضافة التقرير إلى قاعدة البيانات
            show_info(self, "إضافة تقرير", "تم إضافة التقرير بنجاح")
            self.load_reports()
    
    def edit_report(self):
        """تعديل بيانات تقرير"""
        selected_rows = self.reports_table.selectedItems()
        if not selected_rows:
            show_error(self, "خطأ", "الرجاء اختيار تقرير للتعديل")
            return
        
        row = selected_rows[0].row()
        report_id = int(self.reports_table.item(row, 0).text())
        
        # TODO: تحميل بيانات التقرير من قاعدة البيانات
        report_data = {
            "id": report_id,
            "student_name": self.reports_table.item(row, 1).text(),
            "reporter_name": self.reports_table.item(row, 2).text(),
            "reporter_role": self.reports_table.item(row, 3).text(),
            "report_date": self.reports_table.item(row, 4).text(),
            "report_time": self.reports_table.item(row, 5).text(),
            "actions": self.reports_table.item(row, 6).text().split("، ")
        }
        
        dialog = BehaviorReportDialog(self, report_data)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # TODO: تنفيذ تحديث بيانات التقرير في قاعدة البيانات
            show_info(self, "تعديل تقرير", "تم تعديل بيانات التقرير بنجاح")
            self.load_reports()
    
    def delete_report(self):
        """حذف تقرير"""
        selected_rows = self.reports_table.selectedItems()
        if not selected_rows:
            show_error(self, "خطأ", "الرجاء اختيار تقرير للحذف")
            return
        
        row = selected_rows[0].row()
        report_id = int(self.reports_table.item(row, 0).text())
        student_name = self.reports_table.item(row, 1).text()
        
        confirm = QMessageBox.question(
            self, "تأكيد الحذف", 
            f"هل أنت متأكد من حذف التقرير للتلميذ {student_name}؟",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if confirm == QMessageBox.StandardButton.Yes:
            # TODO: تنفيذ حذف التقرير من قاعدة البيانات
            show_info(self, "حذف تقرير", "تم حذف التقرير بنجاح")
            self.load_reports()
    
    def go_back(self):
        """العودة إلى الصفحة الرئيسية"""
        # TODO: تنفيذ العودة إلى الصفحة الرئيسية
        self.parent().setCurrentIndex(0)  # افتراض أن هذه الواجهة في QStackedWidget


class BehaviorReportDialog(QDialog):
    """نافذة إضافة/تعديل تقرير سلوكي"""
    
    def __init__(self, parent=None, report_data=None):
        super().__init__(parent)
        self.report_data = report_data
        self.setWindowTitle("إضافة تقرير جديد" if not report_data else "تعديل تقرير")
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.setMinimumWidth(600)
        self.setup_ui()
    
    def setup_ui(self):
        """إعداد واجهة المستخدم"""
        main_layout = QVBoxLayout(self)
        
        # مجموعة بيانات التلميذ
        student_group = QGroupBox("بيانات التلميذ")
        student_layout = QFormLayout(student_group)
        
        # اختيار التلميذ
        self.student_combo = QComboBox()
        # TODO: تحميل قائمة التلاميذ من قاعدة البيانات
        self.student_combo.addItems(["رهام هبة الله مشري", "داوود حميدة", "نورالإيمان رحال"])
        if self.report_data:
            self.student_combo.setCurrentText(self.report_data["student_name"])
            self.student_combo.setEnabled(False)  # تعطيل تغيير التلميذ عند التعديل
        student_layout.addRow("التلميذ:", self.student_combo)
        
        main_layout.addWidget(student_group)
        
        # مجموعة بيانات صاحب التقرير
        reporter_group = QGroupBox("بيانات صاحب التقرير")
        reporter_layout = QFormLayout(reporter_group)
        
        # اسم صاحب التقرير
        self.reporter_name_input = QLineEdit()
        if self.report_data:
            self.reporter_name_input.setText(self.report_data["reporter_name"])
        reporter_layout.addRow("الاسم واللقب:", self.reporter_name_input)
        
        # وظيفة صاحب التقرير
        self.reporter_role_combo = QComboBox()
        self.reporter_role_combo.addItems(["أستاذ", "مشرف", "مستشار التربية", "عامل"])
        self.reporter_role_combo.currentTextChanged.connect(self.toggle_specialization)
        if self.report_data:
            self.reporter_role_combo.setCurrentText(self.report_data["reporter_role"])
        reporter_layout.addRow("الوظيفة:", self.reporter_role_combo)
        
        # تخصص الأستاذ (يظهر فقط إذا كان صاحب التقرير أستاذًا)
        self.specialization_input = QLineEdit()
        if self.report_data and "specialization" in self.report_data:
            self.specialization_input.setText(self.report_data["specialization"])
        self.specialization_label = QLabel("التخصص:")
        reporter_layout.addRow(self.specialization_label, self.specialization_input)
        
        # إخفاء حقل التخصص إذا لم يكن صاحب التقرير أستاذًا
        self.toggle_specialization(self.reporter_role_combo.currentText())
        
        main_layout.addWidget(reporter_group)
        
        # مجموعة بيانات التقرير
        report_group = QGroupBox("بيانات التقرير")
        report_layout = QFormLayout(report_group)
        
        # تاريخ التقرير
        self.report_date_edit = QDateEdit()
        self.report_date_edit.setCalendarPopup(True)
        self.report_date_edit.setDisplayFormat("yyyy-MM-dd")
        if self.report_data and self.report_data["report_date"]:
            self.report_date_edit.setDate(QDate.fromString(self.report_data["report_date"], "yyyy-MM-dd"))
        else:
            self.report_date_edit.setDate(QDate.currentDate())
        report_layout.addRow("تاريخ التقرير:", self.report_date_edit)
        
        # ساعة التقرير
        self.report_time_edit = QTimeEdit()
        self.report_time_edit.setDisplayFormat("hh:mm")
        if self.report_data and self.report_data["report_time"]:
            self.report_time_edit.setTime(QTime.fromString(self.report_data["report_time"], "hh:mm"))
        else:
            self.report_time_edit.setTime(QTime.currentTime())
        report_layout.addRow("الساعة:", self.report_time_edit)
        
        # وصف التقرير
        self.description_text = QTextEdit()
        if self.report_data and "description" in self.report_data:
            self.description_text.setText(self.report_data["description"])
        report_layout.addRow("الوصف:", self.description_text)
        
        main_layout.addWidget(report_group)
        
        # مجموعة الإجراءات المتخذة
        actions_group = QGroupBox("الإجراءات المتخذة")
        actions_layout = QVBoxLayout(actions_group)
        
        # خيارات الإجراءات
        self.action_checks = {}
        actions = [
            "إنذار شفهي",
            "إنذار كتابي",
            "توبيخ",
            "عرض على لجنة الإرشاد والمتابعة",
            "استدعاء الولي"
        ]
        
        for action in actions:
            check = QCheckBox(action)
            if self.report_data and "actions" in self.report_data:
                check.setChecked(action in self.report_data["actions"])
            actions_layout.addWidget(check)
            self.action_checks[action] = check
            
            # إذا كان الإجراء هو استدعاء الولي، نضيف مجموعة بيانات الاستدعاء
            if action == "استدعاء الولي":
                check.toggled.connect(self.toggle_summon_group)
        
        main_layout.addWidget(actions_group)
        
        # مجموعة بيانات استدعاء الولي
        self.summon_group = QGroupBox("بيانات استدعاء الولي")
        summon_layout = QFormLayout(self.summon_group)
        
        # اسم الولي
        self.parent_name_input = QLineEdit()
        if self.report_data and "parent_name" in self.report_data:
            self.parent_name_input.setText(self.report_data["parent_name"])
        summon_layout.addRow("اسم الولي:", self.parent_name_input)
        
        # المستدعي
        self.summoner_name_input = QLineEdit()
        if self.report_data and "summoner_name" in self.report_data:
            self.summoner_name_input.setText(self.report_data["summoner_name"])
        else:
            self.summoner_name_input.setText(self.reporter_name_input.text())  # افتراضيًا نفس صاحب التقرير
        summon_layout.addRow("المستدعي:", self.summoner_name_input)
        
        # تاريخ الاستدعاء
        self.summon_date_edit = QDateEdit()
        self.summon_date_edit.setCalendarPopup(True)
        self.summon_date_edit.setDisplayFormat("yyyy-MM-dd")
        if self.report_data and "summon_date" in self.report_data:
            self.summon_date_edit.setDate(QDate.fromString(self.report_data["summon_date"], "yyyy-MM-dd"))
        else:
            self.summon_date_edit.setDate(QDate.currentDate().addDays(1))  # افتراضيًا اليوم التالي
        summon_layout.addRow("تاريخ الاستدعاء:", self.summon_date_edit)
        
        # ساعة الاستدعاء
        self.summon_time_edit = QTimeEdit()
        self.summon_time_edit.setDisplayFormat("hh:mm")
        if self.report_data and "summon_time" in self.report_data:
            self.summon_time_edit.setTime(QTime.fromString(self.report_data["summon_time"], "hh:mm"))
        else:
            self.summon_time_edit.setTime(QTime(10, 0))  # افتراضيًا الساعة 10:00
        summon_layout.addRow("الساعة:", self.summon_time_edit)
        
        # حضور الولي
        self.attended_check = QCheckBox("نعم")
        if self.report_data and "attended" in self.report_data:
            self.attended_check.setChecked(self.report_data["attended"])
        summon_layout.addRow("الحضور:", self.attended_check)
        
        self.summon_group.setLayout(summon_layout)
        main_layout.addWidget(self.summon_group)
        
        # إخفاء مجموعة بيانات الاستدعاء إذا لم يتم اختيار استدعاء الولي
        self.toggle_summon_group(self.action_checks["استدعاء الولي"].isChecked())
        
        # أزرار الحفظ والإلغاء
        buttons_layout = QHBoxLayout()
        
        self.cancel_button = QPushButton("إلغاء")
        self.cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(self.cancel_button)
        
        self.save_button = QPushButton("حفظ")
        self.save_button.clicked.connect(self.accept)
        buttons_layout.addWidget(self.save_button)
        
        main_layout.addLayout(buttons_layout)
    
    def toggle_specialization(self, role):
        """إظهار أو إخفاء حقل التخصص حسب الوظيفة"""
        is_teacher = role == "أستاذ"
        self.specialization_label.setVisible(is_teacher)
        self.specialization_input.setVisible(is_teacher)
    
    def toggle_summon_group(self, checked):
        """إظهار أو إخفاء مجموعة بيانات استدعاء الولي"""
        self.summon_group.setVisible(checked)
        if checked and not self.parent_name_input.text():
            # محاولة ملء اسم الولي تلقائيًا
            student_name = self.student_combo.currentText()
            if student_name:
                parts = student_name.split()
                if len(parts) > 1:
                    self.parent_name_input.setText(f"ولي التلميذ(ة) {parts[-1]}")
    
    def accept(self):
        """التحقق من البيانات وحفظها"""
        # التحقق من اختيار تلميذ
        if self.student_combo.currentIndex() == -1:
            show_error(self, "خطأ", "الرجاء اختيار تلميذ")
            return
        
        # التحقق من إدخال اسم صاحب التقرير
        if not self.reporter_name_input.text():
            show_error(self, "خطأ", "الرجاء إدخال اسم صاحب التقرير")
            return
        
        # التحقق من إدخال تخصص الأستاذ إذا كان صاحب التقرير أستاذًا
        if self.reporter_role_combo.currentText() == "أستاذ" and not self.specialization_input.text():
            show_error(self, "خطأ", "الرجاء إدخال تخصص الأستاذ")
            return
        
        # التحقق من اختيار إجراء واحد على الأقل
        has_action = False
        for check in self.action_checks.values():
            if check.isChecked():
                has_action = True
                break
        
        if not has_action:
            show_error(self, "خطأ", "الرجاء اختيار إجراء واحد على الأقل")
            return
        
        # التحقق من بيانات استدعاء الولي إذا تم اختيار هذا الإجراء
        if self.action_checks["استدعاء الولي"].isChecked():
            if not self.parent_name_input.text():
                show_error(self, "خطأ", "الرجاء إدخال اسم الولي")
                return
            
            if not self.summoner_name_input.text():
                show_error(self, "خطأ", "الرجاء إدخال اسم المستدعي")
                return
        
        # TODO: جمع البيانات وإرسالها إلى الكنترولر
        
        super().accept()
