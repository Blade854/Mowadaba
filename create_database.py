#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
سكريبت إنشاء قاعدة البيانات لنظام إدارة المدرسة
"""

import os
import sqlite3
import sys

# تحديد مسار قاعدة البيانات
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'school.db')

def create_database():
    """إنشاء قاعدة البيانات وجداولها"""
    
    # التحقق من وجود قاعدة البيانات
    if os.path.exists(DB_PATH):
        choice = input(f"قاعدة البيانات موجودة بالفعل في {DB_PATH}. هل تريد إعادة إنشائها؟ (نعم/لا): ")
        if choice.lower() not in ['نعم', 'y', 'yes']:
            print("تم إلغاء العملية.")
            return False
        
    # إنشاء اتصال بقاعدة البيانات
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # إنشاء جدول التلاميذ
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Students (
            student_id TEXT PRIMARY KEY,
            last_name TEXT NOT NULL,
            first_name TEXT NOT NULL,
            gender TEXT NOT NULL,
            birth_date DATE NOT NULL,
            birth_judgment TEXT,
            birth_certificate_type TEXT,
            registration_year INTEGER,
            birth_certificate_number TEXT,
            birth_place TEXT,
            academic_year TEXT,
            section TEXT,
            class_number TEXT,
            study_system TEXT,
            registration_number INTEGER,
            registration_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # إنشاء جدول الأساتذة
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Teachers (
            teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
            last_name TEXT NOT NULL,
            first_name TEXT NOT NULL,
            gender TEXT NOT NULL,
            birth_date DATE,
            specialization TEXT,
            phone_number TEXT,
            email TEXT,
            address TEXT,
            hire_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # إنشاء جدول العمال
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Staff (
            staff_id INTEGER PRIMARY KEY AUTOINCREMENT,
            last_name TEXT NOT NULL,
            first_name TEXT NOT NULL,
            gender TEXT NOT NULL,
            birth_date DATE,
            job_title TEXT NOT NULL,
            phone_number TEXT,
            email TEXT,
            address TEXT,
            hire_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # إنشاء جدول الشهادات الطبية
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS MedicalCertificates (
            certificate_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            receipt_date DATE NOT NULL,
            school_doctor_verified BOOLEAN DEFAULT 0,
            parent_delivered BOOLEAN DEFAULT 0,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES Students(student_id) ON DELETE CASCADE
        )
        ''')
        
        # إنشاء جدول التقارير السلوكية
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS BehaviorReports (
            report_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            reporter_name TEXT NOT NULL,
            reporter_role TEXT NOT NULL,
            specialization TEXT,
            report_date DATE NOT NULL,
            report_time TIME NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES Students(student_id) ON DELETE CASCADE
        )
        ''')
        
        # إنشاء جدول الإجراءات المتخذة
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Actions (
            action_id INTEGER PRIMARY KEY AUTOINCREMENT,
            action_name TEXT NOT NULL UNIQUE
        )
        ''')
        
        # إدراج الإجراءات المتاحة
        actions = [
            ('إنذار شفهي',),
            ('إنذار كتابي',),
            ('توبيخ',),
            ('عرض على لجنة الإرشاد والمتابعة',),
            ('استدعاء الولي',)
        ]
        cursor.executemany('INSERT OR IGNORE INTO Actions (action_name) VALUES (?)', actions)
        
        # إنشاء جدول العلاقة بين التقارير والإجراءات
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS ReportActions (
            report_id INTEGER NOT NULL,
            action_id INTEGER NOT NULL,
            PRIMARY KEY (report_id, action_id),
            FOREIGN KEY (report_id) REFERENCES BehaviorReports(report_id) ON DELETE CASCADE,
            FOREIGN KEY (action_id) REFERENCES Actions(action_id) ON DELETE CASCADE
        )
        ''')
        
        # إنشاء جدول استدعاءات الأولياء
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS ParentSummons (
            summon_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            parent_name TEXT NOT NULL,
            summoner_name TEXT NOT NULL,
            summon_date DATE NOT NULL,
            summon_time TIME NOT NULL,
            attended BOOLEAN DEFAULT 0,
            report_id INTEGER,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES Students(student_id) ON DELETE CASCADE,
            FOREIGN KEY (report_id) REFERENCES BehaviorReports(report_id) ON DELETE SET NULL
        )
        ''')
        
        # إنشاء الفهارس
        # فهارس جدول التلاميذ
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_students_name ON Students(last_name, first_name)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_students_class ON Students(academic_year, section, class_number)')
        
        # فهارس جدول الأساتذة
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_teachers_name ON Teachers(last_name, first_name)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_teachers_specialization ON Teachers(specialization)')
        
        # فهارس جدول العمال
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_staff_name ON Staff(last_name, first_name)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_staff_job ON Staff(job_title)')
        
        # فهارس جدول الشهادات الطبية
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_certificates_student ON MedicalCertificates(student_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_certificates_dates ON MedicalCertificates(start_date, end_date)')
        
        # فهارس جدول التقارير السلوكية
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_reports_student ON BehaviorReports(student_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_reports_date ON BehaviorReports(report_date)')
        
        # فهارس جدول استدعاءات الأولياء
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_summons_student ON ParentSummons(student_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_summons_date ON ParentSummons(summon_date)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_summons_attended ON ParentSummons(attended)')
        
        # إنشاء المشغلات (Triggers)
        # مشغل تحديث التلاميذ
        cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS update_students_timestamp 
        AFTER UPDATE ON Students
        BEGIN
            UPDATE Students SET updated_at = CURRENT_TIMESTAMP WHERE student_id = NEW.student_id;
        END;
        ''')
        
        # مشغل تحديث الأساتذة
        cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS update_teachers_timestamp 
        AFTER UPDATE ON Teachers
        BEGIN
            UPDATE Teachers SET updated_at = CURRENT_TIMESTAMP WHERE teacher_id = NEW.teacher_id;
        END;
        ''')
        
        # مشغل تحديث العمال
        cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS update_staff_timestamp 
        AFTER UPDATE ON Staff
        BEGIN
            UPDATE Staff SET updated_at = CURRENT_TIMESTAMP WHERE staff_id = NEW.staff_id;
        END;
        ''')
        
        # مشغل تحديث الشهادات الطبية
        cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS update_certificates_timestamp 
        AFTER UPDATE ON MedicalCertificates
        BEGIN
            UPDATE MedicalCertificates SET updated_at = CURRENT_TIMESTAMP 
            WHERE certificate_id = NEW.certificate_id;
        END;
        ''')
        
        # مشغل تحديث التقارير السلوكية
        cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS update_reports_timestamp 
        AFTER UPDATE ON BehaviorReports
        BEGIN
            UPDATE BehaviorReports SET updated_at = CURRENT_TIMESTAMP 
            WHERE report_id = NEW.report_id;
        END;
        ''')
        
        # مشغل تحديث استدعاءات الأولياء
        cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS update_summons_timestamp 
        AFTER UPDATE ON ParentSummons
        BEGIN
            UPDATE ParentSummons SET updated_at = CURRENT_TIMESTAMP 
            WHERE summon_id = NEW.summon_id;
        END;
        ''')
        
        # حفظ التغييرات
        conn.commit()
        print(f"تم إنشاء قاعدة البيانات بنجاح في {DB_PATH}")
        return True
        
    except sqlite3.Error as e:
        print(f"حدث خطأ أثناء إنشاء قاعدة البيانات: {e}")
        return False
        
    finally:
        # إغلاق الاتصال
        conn.close()

if __name__ == "__main__":
    create_database()
