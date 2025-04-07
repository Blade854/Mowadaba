#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
تعديل وظيفة تهيئة قاعدة البيانات لدعم وضع الاختبار
"""

import os
import datetime
from sqlalchemy import create_engine, Column, Integer, String, Date, Time, Boolean, ForeignKey, Table, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# تحديد مسار قاعدة البيانات
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'school.db')
ENGINE = create_engine(f'sqlite:///{DB_PATH}', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=ENGINE)

# جدول العلاقة بين التقارير والإجراءات
report_actions = Table(
    'ReportActions',
    Base.metadata,
    Column('report_id', Integer, ForeignKey('BehaviorReports.report_id'), primary_key=True),
    Column('action_id', Integer, ForeignKey('Actions.action_id'), primary_key=True)
)

class Student(Base):
    """نموذج التلميذ"""
    __tablename__ = 'Students'
    
    student_id = Column(String, primary_key=True)
    last_name = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    birth_judgment = Column(String)
    birth_certificate_type = Column(String)
    registration_year = Column(Integer)
    birth_certificate_number = Column(String)
    birth_place = Column(String)
    academic_year = Column(String)
    section = Column(String)
    class_number = Column(String)
    study_system = Column(String)
    registration_number = Column(Integer)
    registration_date = Column(Date)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    
    # العلاقات
    medical_certificates = relationship("MedicalCertificate", back_populates="student", cascade="all, delete-orphan")
    behavior_reports = relationship("BehaviorReport", back_populates="student", cascade="all, delete-orphan")
    parent_summons = relationship("ParentSummon", back_populates="student", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Student(id={self.student_id}, name={self.first_name} {self.last_name})>"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class Teacher(Base):
    """نموذج الأستاذ"""
    __tablename__ = 'Teachers'
    
    teacher_id = Column(Integer, primary_key=True, autoincrement=True)
    last_name = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    birth_date = Column(Date)
    specialization = Column(String)
    phone_number = Column(String)
    email = Column(String)
    address = Column(String)
    hire_date = Column(Date)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    
    def __repr__(self):
        return f"<Teacher(id={self.teacher_id}, name={self.first_name} {self.last_name})>"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class Staff(Base):
    """نموذج العامل"""
    __tablename__ = 'Staff'
    
    staff_id = Column(Integer, primary_key=True, autoincrement=True)
    last_name = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    birth_date = Column(Date)
    job_title = Column(String, nullable=False)
    phone_number = Column(String)
    email = Column(String)
    address = Column(String)
    hire_date = Column(Date)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    
    def __repr__(self):
        return f"<Staff(id={self.staff_id}, name={self.first_name} {self.last_name})>"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class MedicalCertificate(Base):
    """نموذج الشهادة الطبية"""
    __tablename__ = 'MedicalCertificates'
    
    certificate_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(String, ForeignKey('Students.student_id'), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    receipt_date = Column(Date, nullable=False)
    school_doctor_verified = Column(Boolean, default=False)
    parent_delivered = Column(Boolean, default=False)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    
    # العلاقات
    student = relationship("Student", back_populates="medical_certificates")
    
    def __repr__(self):
        return f"<MedicalCertificate(id={self.certificate_id}, student_id={self.student_id})>"

class Action(Base):
    """نموذج الإجراء المتخذ"""
    __tablename__ = 'Actions'
    
    action_id = Column(Integer, primary_key=True, autoincrement=True)
    action_name = Column(String, nullable=False, unique=True)
    
    # العلاقات
    reports = relationship("BehaviorReport", secondary=report_actions, back_populates="actions")
    
    def __repr__(self):
        return f"<Action(id={self.action_id}, name={self.action_name})>"

class BehaviorReport(Base):
    """نموذج التقرير السلوكي"""
    __tablename__ = 'BehaviorReports'
    
    report_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(String, ForeignKey('Students.student_id'), nullable=False)
    reporter_name = Column(String, nullable=False)
    reporter_role = Column(String, nullable=False)
    specialization = Column(String)
    report_date = Column(Date, nullable=False)
    report_time = Column(Time, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    
    # العلاقات
    student = relationship("Student", back_populates="behavior_reports")
    actions = relationship("Action", secondary=report_actions, back_populates="reports")
    parent_summons = relationship("ParentSummon", back_populates="report")
    
    def __repr__(self):
        return f"<BehaviorReport(id={self.report_id}, student_id={self.student_id})>"

class ParentSummon(Base):
    """نموذج استدعاء الولي"""
    __tablename__ = 'ParentSummons'
    
    summon_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(String, ForeignKey('Students.student_id'), nullable=False)
    parent_name = Column(String, nullable=False)
    summoner_name = Column(String, nullable=False)
    summon_date = Column(Date, nullable=False)
    summon_time = Column(Time, nullable=False)
    attended = Column(Boolean, default=False)
    report_id = Column(Integer, ForeignKey('BehaviorReports.report_id'))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    
    # العلاقات
    student = relationship("Student", back_populates="parent_summons")
    report = relationship("BehaviorReport", back_populates="parent_summons")
    
    def __repr__(self):
        return f"<ParentSummon(id={self.summon_id}, student_id={self.student_id})>"

def init_db(test=False):
    """تهيئة قاعدة البيانات
    
    المعلمات:
        test (bool): إذا كانت True، يتم استخدام قاعدة بيانات اختبار منفصلة
    """
    # إذا كان وضع الاختبار، نستخدم قاعدة بيانات في الذاكرة
    if test:
        engine = create_engine('sqlite:///:memory:', echo=False)
        Base.metadata.create_all(engine)
        Session.configure(bind=engine)
    else:
        Base.metadata.create_all(ENGINE)
    
    # إضافة الإجراءات المتاحة إذا لم تكن موجودة
    session = Session()
    actions = [
        "إنذار شفهي",
        "إنذار كتابي",
        "توبيخ",
        "عرض على لجنة الإرشاد والمتابعة",
        "استدعاء الولي"
    ]
    
    for action_name in actions:
        existing = session.query(Action).filter_by(action_name=action_name).first()
        if not existing:
            session.add(Action(action_name=action_name))
    
    session.commit()
    session.close()

if __name__ == "__main__":
    init_db()
