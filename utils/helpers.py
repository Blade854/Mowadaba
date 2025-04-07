#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
وحدة المساعدة لنظام إدارة المدرسة
"""

import os
import pandas as pd
import datetime
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QDate, QTime
import arabic_reshaper
from bidi.algorithm import get_display

def reshape_arabic(text):
    """إعادة تشكيل النص العربي للعرض الصحيح"""
    if not text:
        return ""
    reshaped_text = arabic_reshaper.reshape(str(text))
    return get_display(reshaped_text)

def date_to_qdate(date_obj):
    """تحويل كائن التاريخ إلى كائن QDate"""
    if not date_obj:
        return QDate.currentDate()
    if isinstance(date_obj, str):
        try:
            date_obj = datetime.datetime.strptime(date_obj, "%Y-%m-%d").date()
        except ValueError:
            return QDate.currentDate()
    return QDate(date_obj.year, date_obj.month, date_obj.day)

def qdate_to_date(qdate):
    """تحويل كائن QDate إلى كائن تاريخ Python"""
    if not qdate:
        return None
    return datetime.date(qdate.year(), qdate.month(), qdate.day())

def time_to_qtime(time_obj):
    """تحويل كائن الوقت إلى كائن QTime"""
    if not time_obj:
        return QTime.currentTime()
    if isinstance(time_obj, str):
        try:
            time_obj = datetime.datetime.strptime(time_obj, "%H:%M:%S").time()
        except ValueError:
            return QTime.currentTime()
    return QTime(time_obj.hour, time_obj.minute, time_obj.second)

def qtime_to_time(qtime):
    """تحويل كائن QTime إلى كائن وقت Python"""
    if not qtime:
        return None
    return datetime.time(qtime.hour(), qtime.minute(), qtime.second())

def show_error(parent, title, message):
    """عرض رسالة خطأ"""
    QMessageBox.critical(parent, title, message)

def show_info(parent, title, message):
    """عرض رسالة معلومات"""
    QMessageBox.information(parent, title, message)

def show_warning(parent, title, message):
    """عرض رسالة تحذير"""
    QMessageBox.warning(parent, title, message)

def show_question(parent, title, message):
    """عرض سؤال نعم/لا"""
    return QMessageBox.question(parent, title, message) == QMessageBox.StandardButton.Yes

def read_excel_file(file_path):
    """قراءة ملف Excel أو HTML"""
    try:
        if file_path.endswith('.xls') or file_path.endswith('.xlsx'):
            return pd.read_excel(file_path)
        elif file_path.endswith('.html') or file_path.endswith('.htm'):
            return pd.read_html(file_path)[0]
        else:
            raise ValueError("نوع الملف غير مدعوم. يجب أن يكون Excel أو HTML.")
    except Exception as e:
        raise Exception(f"خطأ في قراءة الملف: {str(e)}")

def map_columns(df, column_mapping):
    """تعيين أعمدة DataFrame إلى أعمدة قاعدة البيانات"""
    new_df = pd.DataFrame()
    for db_col, file_col in column_mapping.items():
        if file_col in df.columns:
            new_df[db_col] = df[file_col]
    return new_df
