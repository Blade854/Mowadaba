#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
تعديل وحدة التحكم في التقارير السلوكية لنظام إدارة المدرسة
"""

import os
from datetime import datetime, date
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from models.database import BehaviorReport, Action, Student, report_actions, Session as DBSession

class BehaviorReportController:
    """وحدة التحكم في التقارير السلوكية"""
    
    @staticmethod
    def get_all_reports():
        """الحصول على جميع التقارير السلوكية"""
        session = DBSession()
        try:
            reports = session.query(BehaviorReport).all()
            return reports
        except Exception as e:
            print(f"خطأ في الحصول على التقارير السلوكية: {e}")
            return []
        finally:
            session.close()
    
    @staticmethod
    def get_report_by_id(report_id):
        """الحصول على تقرير سلوكي حسب الرقم التعريفي"""
        session = DBSession()
        try:
            report = session.query(BehaviorReport).filter_by(report_id=report_id).first()
            return report
        except Exception as e:
            print(f"خطأ في الحصول على التقرير السلوكي: {e}")
            return None
        finally:
            session.close()
    
    @staticmethod
    def get_reports_by_student(student_id):
        """الحصول على التقارير السلوكية لتلميذ معين"""
        session = DBSession()
        try:
            reports = session.query(BehaviorReport).filter_by(student_id=student_id).all()
            return reports
        except Exception as e:
            print(f"خطأ في الحصول على التقارير السلوكية للتلميذ: {e}")
            return []
        finally:
            session.close()
    
    @staticmethod
    def search_reports_by_student_name(student_name):
        """البحث عن التقارير السلوكية حسب اسم التلميذ"""
        session = DBSession()
        try:
            # البحث عن التلاميذ الذين يطابق اسمهم نص البحث
            students = session.query(Student).filter(
                or_(
                    Student.first_name.like(f"%{student_name}%"),
                    Student.last_name.like(f"%{student_name}%")
                )
            ).all()
            
            # جمع التقارير السلوكية لهؤلاء التلاميذ
            reports = []
            for student in students:
                student_reports = session.query(BehaviorReport).filter_by(student_id=student.student_id).all()
                reports.extend(student_reports)
            
            return reports
        except Exception as e:
            print(f"خطأ في البحث عن التقارير السلوكية: {e}")
            return []
        finally:
            session.close()
    
    @staticmethod
    def add_report(report_data, actions_list):
        """إضافة تقرير سلوكي جديد"""
        session = DBSession()
        try:
            # التحقق من وجود التلميذ
            student_id = report_data["student_id"]
            student = session.query(Student).filter_by(student_id=student_id).first()
            if not student:
                return False, "التلميذ غير موجود"
            
            # إنشاء كائن التقرير السلوكي
            report = BehaviorReport(
                student_id=student_id,
                reporter_name=report_data["reporter_name"],
                reporter_role=report_data["reporter_role"],
                specialization=report_data.get("reporter_specialization"),
                report_date=report_data["report_date"],
                report_time=report_data["report_time"],
                description=report_data.get("description")
            )
            
            # إضافة التقرير السلوكي إلى قاعدة البيانات
            session.add(report)
            session.flush()  # للحصول على report_id
            
            # إضافة الإجراءات المتخذة
            for action_name in actions_list:
                # البحث عن الإجراء في قاعدة البيانات
                action = session.query(Action).filter_by(action_name=action_name).first()
                if not action:
                    # إنشاء إجراء جديد إذا لم يكن موجودًا
                    action = Action(action_name=action_name)
                    session.add(action)
                    session.flush()
                
                # إضافة الإجراء إلى التقرير
                report.actions.append(action)
            
            # إذا كان هناك استدعاء للولي، نقوم بإضافة معلومات الاستدعاء
            if "parent_summon" in report_data and report_data["parent_summon"]:
                from controllers.parent_summon_controller import ParentSummonController
                
                summon_data = {
                    "student_id": student_id,
                    "parent_name": report_data["parent_name"],
                    "summoner_name": report_data["summoner_name"],
                    "summon_date": report_data["summon_date"],
                    "summon_time": report_data["summon_time"],
                    "attended": report_data.get("attended", False),
                    "notes": report_data.get("notes"),
                    "report_id": report.report_id
                }
                
                ParentSummonController.add_summon(summon_data)
            
            session.commit()
            return True, "تم إضافة التقرير السلوكي بنجاح"
        except Exception as e:
            session.rollback()
            print(f"خطأ في إضافة التقرير السلوكي: {e}")
            return False, f"خطأ في إضافة التقرير السلوكي: {str(e)}"
        finally:
            session.close()
    
    @staticmethod
    def update_report(report_id, report_data, actions_list):
        """تحديث بيانات تقرير سلوكي"""
        session = DBSession()
        try:
            # الحصول على التقرير السلوكي
            report = session.query(BehaviorReport).filter_by(report_id=report_id).first()
            if not report:
                return False, "التقرير السلوكي غير موجود"
            
            # تحديث بيانات التقرير السلوكي
            report.reporter_name = report_data["reporter_name"]
            report.reporter_role = report_data["reporter_role"]
            report.specialization = report_data.get("reporter_specialization")
            report.report_date = report_data["report_date"]
            report.report_time = report_data["report_time"]
            report.description = report_data.get("description")
            
            # حذف الإجراءات المتخذة السابقة
            report.actions.clear()
            
            # إضافة الإجراءات المتخذة الجديدة
            for action_name in actions_list:
                # البحث عن الإجراء في قاعدة البيانات
                action = session.query(Action).filter_by(action_name=action_name).first()
                if not action:
                    # إنشاء إجراء جديد إذا لم يكن موجودًا
                    action = Action(action_name=action_name)
                    session.add(action)
                    session.flush()
                
                # إضافة الإجراء إلى التقرير
                report.actions.append(action)
            
            # إذا كان هناك استدعاء للولي، نقوم بتحديث معلومات الاستدعاء
            if "parent_summon" in report_data and report_data["parent_summon"]:
                from controllers.parent_summon_controller import ParentSummonController
                
                # البحث عن الاستدعاء المرتبط بالتقرير
                summon = ParentSummonController.get_summon_by_report_id(report_id)
                
                summon_data = {
                    "student_id": report.student_id,
                    "parent_name": report_data["parent_name"],
                    "summoner_name": report_data["summoner_name"],
                    "summon_date": report_data["summon_date"],
                    "summon_time": report_data["summon_time"],
                    "attended": report_data.get("attended", False),
                    "notes": report_data.get("notes"),
                    "report_id": report.report_id
                }
                
                if summon:
                    # تحديث الاستدعاء الموجود
                    ParentSummonController.update_summon(summon.summon_id, summon_data)
                else:
                    # إنشاء استدعاء جديد
                    ParentSummonController.add_summon(summon_data)
            
            session.commit()
            return True, "تم تحديث بيانات التقرير السلوكي بنجاح"
        except Exception as e:
            session.rollback()
            print(f"خطأ في تحديث بيانات التقرير السلوكي: {e}")
            return False, f"خطأ في تحديث بيانات التقرير السلوكي: {str(e)}"
        finally:
            session.close()
    
    @staticmethod
    def delete_report(report_id):
        """حذف تقرير سلوكي"""
        session = DBSession()
        try:
            # الحصول على التقرير السلوكي
            report = session.query(BehaviorReport).filter_by(report_id=report_id).first()
            if not report:
                return False, "التقرير السلوكي غير موجود"
            
            # حذف الإجراءات المتخذة المرتبطة بالتقرير
            report.actions.clear()
            
            # حذف الاستدعاءات المرتبطة بالتقرير
            from controllers.parent_summon_controller import ParentSummonController
            ParentSummonController.delete_summons_by_report_id(report_id)
            
            # حذف التقرير السلوكي
            session.delete(report)
            session.commit()
            return True, "تم حذف التقرير السلوكي بنجاح"
        except Exception as e:
            session.rollback()
            print(f"خطأ في حذف التقرير السلوكي: {e}")
            return False, f"خطأ في حذف التقرير السلوكي: {str(e)}"
        finally:
            session.close()
    
    @staticmethod
    def get_report_actions(report_id):
        """الحصول على الإجراءات المتخذة لتقرير سلوكي معين"""
        session = DBSession()
        try:
            # الحصول على التقرير السلوكي
            report = session.query(BehaviorReport).filter_by(report_id=report_id).first()
            if not report:
                return []
            
            # جمع أسماء الإجراءات
            actions = [action.action_name for action in report.actions]
            return actions
        except Exception as e:
            print(f"خطأ في الحصول على الإجراءات المتخذة للتقرير: {e}")
            return []
        finally:
            session.close()
    
    @staticmethod
    def get_report_with_student_info(report_id):
        """الحصول على التقرير السلوكي مع معلومات التلميذ والإجراءات المتخذة"""
        session = DBSession()
        try:
            # الحصول على التقرير السلوكي
            report = session.query(BehaviorReport).filter_by(report_id=report_id).first()
            if not report:
                return None
            
            # الحصول على معلومات التلميذ
            student = session.query(Student).filter_by(student_id=report.student_id).first()
            if not student:
                return None
            
            # الحصول على الإجراءات المتخذة
            actions = BehaviorReportController.get_report_actions(report_id)
            
            # إنشاء قاموس يحتوي على معلومات التقرير والتلميذ والإجراءات
            report_info = {
                "report_id": report.report_id,
                "student_id": report.student_id,
                "student_name": f"{student.first_name} {student.last_name}",
                "reporter_name": report.reporter_name,
                "reporter_role": report.reporter_role,
                "reporter_specialization": report.specialization,
                "report_date": report.report_date,
                "report_time": report.report_time,
                "description": report.description,
                "actions": actions
            }
            
            # الحصول على معلومات الاستدعاء إذا كان موجودًا
            from controllers.parent_summon_controller import ParentSummonController
            summon = ParentSummonController.get_summon_by_report_id(report_id)
            if summon:
                report_info["parent_summon"] = True
                report_info["parent_name"] = summon.parent_name
                report_info["summoner_name"] = summon.summoner_name
                report_info["summon_date"] = summon.summon_date
                report_info["summon_time"] = summon.summon_time
                report_info["attended"] = summon.attended
                report_info["notes"] = summon.notes
            
            return report_info
        except Exception as e:
            print(f"خطأ في الحصول على التقرير السلوكي مع معلومات التلميذ: {e}")
            return None
        finally:
            session.close()
    
    @staticmethod
    def get_all_reports_with_student_info():
        """الحصول على جميع التقارير السلوكية مع معلومات التلاميذ والإجراءات المتخذة"""
        session = DBSession()
        try:
            # الحصول على جميع التقارير السلوكية
            reports = session.query(BehaviorReport).all()
            
            # إنشاء قائمة تحتوي على معلومات التقارير والتلاميذ والإجراءات
            reports_info = []
            for report in reports:
                # الحصول على معلومات التلميذ
                student = session.query(Student).filter_by(student_id=report.student_id).first()
                if not student:
                    continue
                
                # الحصول على الإجراءات المتخذة
                actions = [action.action_name for action in report.actions]
                
                # إنشاء قاموس يحتوي على معلومات التقرير والتلميذ والإجراءات
                report_info = {
                    "report_id": report.report_id,
                    "student_id": report.student_id,
                    "student_name": f"{student.first_name} {student.last_name}",
                    "reporter_name": report.reporter_name,
                    "reporter_role": report.reporter_role,
                    "reporter_specialization": report.specialization,
                    "report_date": report.report_date,
                    "report_time": report.report_time,
                    "description": report.description,
                    "actions": actions
                }
                
                reports_info.append(report_info)
            
            return reports_info
        except Exception as e:
            print(f"خطأ في الحصول على التقارير السلوكية مع معلومات التلاميذ: {e}")
            return []
        finally:
            session.close()
