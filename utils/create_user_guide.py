#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
دليل المستخدم لنظام إدارة المدرسة
"""

import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import arabic_reshaper
from bidi.algorithm import get_display

# تسجيل الخطوط العربية
def register_arabic_fonts():
    """تسجيل الخطوط العربية"""
    fonts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "resources", "fonts")
    os.makedirs(fonts_dir, exist_ok=True)
    
    # يمكن إضافة خطوط عربية هنا
    # مثال: pdfmetrics.registerFont(TTFont('Arabic', os.path.join(fonts_dir, 'arabic.ttf')))
    
    # استخدام خط افتراضي
    pdfmetrics.registerFont(TTFont('Arabic', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))

# دالة لمعالجة النص العربي
def arabic_text(text):
    """معالجة النص العربي للعرض الصحيح في PDF"""
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    return bidi_text

# إنشاء دليل المستخدم
def create_user_guide():
    """إنشاء دليل المستخدم بصيغة PDF"""
    # تسجيل الخطوط العربية
    register_arabic_fonts()
    
    # إنشاء مجلد للوثائق
    docs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")
    os.makedirs(docs_dir, exist_ok=True)
    
    # مسار ملف دليل المستخدم
    user_guide_path = os.path.join(docs_dir, "user_guide.pdf")
    
    # إنشاء مستند PDF
    doc = SimpleDocTemplate(
        user_guide_path,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # إنشاء الأنماط
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='Arabic',
        fontName='Arabic',
        fontSize=12,
        leading=14,
        alignment=1  # وسط
    ))
    styles.add(ParagraphStyle(
        name='ArabicTitle',
        fontName='Arabic',
        fontSize=18,
        leading=22,
        alignment=1,  # وسط
        spaceAfter=12
    ))
    styles.add(ParagraphStyle(
        name='ArabicHeading',
        fontName='Arabic',
        fontSize=14,
        leading=18,
        alignment=1,  # وسط
        spaceAfter=10
    ))
    
    # إنشاء محتوى المستند
    content = []
    
    # العنوان
    content.append(Paragraph(arabic_text("دليل المستخدم - نظام إدارة المدرسة"), styles['ArabicTitle']))
    content.append(Spacer(1, 12))
    
    # تاريخ الإنشاء
    content.append(Paragraph(arabic_text(f"تاريخ الإنشاء: {datetime.now().strftime('%Y-%m-%d')}"), styles['Arabic']))
    content.append(Spacer(1, 24))
    
    # جدول المحتويات
    content.append(Paragraph(arabic_text("جدول المحتويات"), styles['ArabicHeading']))
    content.append(Spacer(1, 12))
    
    toc_data = [
        [arabic_text("1. مقدمة"), arabic_text("3")],
        [arabic_text("2. متطلبات النظام"), arabic_text("3")],
        [arabic_text("3. تثبيت البرنامج"), arabic_text("4")],
        [arabic_text("4. واجهة المستخدم الرئيسية"), arabic_text("5")],
        [arabic_text("5. إدارة التلاميذ"), arabic_text("6")],
        [arabic_text("6. إدارة الأساتذة والعمال"), arabic_text("8")],
        [arabic_text("7. إدارة الشهادات الطبية"), arabic_text("10")],
        [arabic_text("8. إدارة التقارير السلوكية"), arabic_text("12")],
        [arabic_text("9. إدارة استدعاءات الأولياء"), arabic_text("14")],
        [arabic_text("10. طباعة التقارير والإحصائيات"), arabic_text("16")],
        [arabic_text("11. الدعم الفني"), arabic_text("18")]
    ]
    
    toc = Table(toc_data, colWidths=[350, 50])
    toc.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Arabic'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    content.append(toc)
    content.append(Spacer(1, 24))
    
    # المقدمة
    content.append(Paragraph(arabic_text("1. مقدمة"), styles['ArabicHeading']))
    content.append(Paragraph(arabic_text("""
    نظام إدارة المدرسة هو برنامج متكامل يهدف إلى تسهيل العمليات الإدارية في المدرسة. يوفر النظام واجهة سهلة الاستخدام لإدارة بيانات التلاميذ والأساتذة والعمال، وكذلك إدارة الشهادات الطبية والتقارير السلوكية واستدعاءات الأولياء.
    
    يتميز النظام بالقدرة على استيراد البيانات من ملفات Excel، وإمكانية البحث السريع، وطباعة التقارير والإحصائيات المختلفة.
    """), styles['Arabic']))
    content.append(Spacer(1, 12))
    
    # متطلبات النظام
    content.append(Paragraph(arabic_text("2. متطلبات النظام"), styles['ArabicHeading']))
    content.append(Paragraph(arabic_text("""
    للاستفادة من جميع مزايا نظام إدارة المدرسة، يجب أن يتوفر جهاز الكمبيوتر على المتطلبات التالية:
    
    • نظام التشغيل: Windows 10 أو أحدث، macOS 10.14 أو أحدث، أو Linux
    • المعالج: Intel Core i3 أو ما يعادله
    • الذاكرة العشوائية: 4 جيجابايت على الأقل
    • مساحة القرص الصلب: 500 ميجابايت على الأقل
    • الشاشة: دقة 1366×768 أو أعلى
    """), styles['Arabic']))
    content.append(Spacer(1, 12))
    
    # تثبيت البرنامج
    content.append(Paragraph(arabic_text("3. تثبيت البرنامج"), styles['ArabicHeading']))
    content.append(Paragraph(arabic_text("""
    لتثبيت نظام إدارة المدرسة، اتبع الخطوات التالية:
    
    1. قم بتشغيل ملف التثبيت "نظام إدارة المدرسة-Setup.exe"
    2. اتبع التعليمات التي تظهر في معالج التثبيت
    3. اختر مجلد التثبيت المناسب
    4. انتظر حتى اكتمال عملية التثبيت
    5. انقر على "إنهاء" لإكمال عملية التثبيت
    
    بعد اكتمال التثبيت، يمكنك تشغيل البرنامج من خلال النقر على أيقونة "نظام إدارة المدرسة" على سطح المكتب أو من قائمة ابدأ.
    """), styles['Arabic']))
    content.append(Spacer(1, 12))
    
    # واجهة المستخدم الرئيسية
    content.append(Paragraph(arabic_text("4. واجهة المستخدم الرئيسية"), styles['ArabicHeading']))
    content.append(Paragraph(arabic_text("""
    عند تشغيل البرنامج، ستظهر الواجهة الرئيسية التي تحتوي على الأزرار التالية:
    
    • إدارة التلاميذ: للوصول إلى واجهة إدارة بيانات التلاميذ
    • إدارة الأساتذة والعمال: للوصول إلى واجهة إدارة بيانات الأساتذة والعمال
    • إدارة الشهادات الطبية: للوصول إلى واجهة إدارة الشهادات الطبية
    • إدارة التقارير السلوكية: للوصول إلى واجهة إدارة التقارير السلوكية
    • إدارة استدعاءات الأولياء: للوصول إلى واجهة إدارة استدعاءات الأولياء
    • طباعة التقارير والإحصائيات: للوصول إلى واجهة طباعة التقارير والإحصائيات
    
    تحتوي جميع الواجهات على زر "العودة إلى الصفحة الرئيسية" للرجوع إلى الواجهة الرئيسية.
    """), styles['Arabic']))
    content.append(Spacer(1, 12))
    
    # إدارة التلاميذ
    content.append(Paragraph(arabic_text("5. إدارة التلاميذ"), styles['ArabicHeading']))
    content.append(Paragraph(arabic_text("""
    تتيح واجهة إدارة التلاميذ القيام بالعمليات التالية:
    
    • استيراد قوائم التلاميذ من ملفات Excel
    • إضافة تلميذ جديد
    • تعديل بيانات تلميذ
    • حذف تلميذ
    • البحث عن تلميذ
    
    لاستيراد قوائم التلاميذ من ملف Excel:
    1. انقر على زر "استيراد من Excel"
    2. اختر ملف Excel الذي يحتوي على بيانات التلاميذ
    3. قم بتعيين الأعمدة المطلوبة في نافذة تعيين الأعمدة
    4. انقر على "استيراد" لبدء عملية الاستيراد
    
    لإضافة تلميذ جديد:
    1. انقر على زر "إضافة تلميذ"
    2. أدخل بيانات التلميذ في النموذج
    3. انقر على "حفظ" لإضافة التلميذ
    
    لتعديل بيانات تلميذ:
    1. حدد التلميذ من الجدول
    2. انقر على زر "تعديل"
    3. قم بتعديل البيانات في النموذج
    4. انقر على "حفظ" لحفظ التغييرات
    
    لحذف تلميذ:
    1. حدد التلميذ من الجدول
    2. انقر على زر "حذف"
    3. أكد عملية الحذف في نافذة التأكيد
    
    للبحث عن تلميذ:
    1. أدخل اسم التلميذ أو جزء منه في حقل البحث
    2. اضغط على Enter أو انقر على زر "بحث"
    """), styles['Arabic']))
    content.append(Spacer(1, 12))
    
    # إدارة الأساتذة والعمال
    content.append(Paragraph(arabic_text("6. إدارة الأساتذة والعمال"), styles['ArabicHeading']))
    content.append(Paragraph(arabic_text("""
    تتيح واجهة إدارة الأساتذة والعمال القيام بالعمليات التالية:
    
    • استيراد قوائم الأساتذة والعمال من ملفات Excel
    • إضافة أستاذ أو عامل جديد
    • تعديل بيانات أستاذ أو عامل
    • حذف أستاذ أو عامل
    • البحث عن أستاذ أو عامل
    
    العمليات مشابهة لتلك الموجودة في واجهة إدارة التلاميذ.
    """), styles['Arabic']))
    content.append(Spacer(1, 12))
    
    # إدارة الشهادات الطبية
    content.append(Paragraph(arabic_text("7. إدارة الشهادات الطبية"), styles['ArabicHeading']))
    content.append(Paragraph(arabic_text("""
    تتيح واجهة إدارة الشهادات الطبية القيام بالعمليات التالية:
    
    • تسجيل شهادة طبية جديدة
    • تعديل بيانات شهادة طبية
    • حذف شهادة طبية
    • عرض الشهادات الطبية ليوم معين
    • عرض الشهادات الطبية لتلميذ معين
    
    لتسجيل شهادة طبية جديدة:
    1. انقر على زر "إضافة شهادة طبية"
    2. ابحث عن التلميذ وحدده
    3. أدخل بيانات الشهادة الطبية (تاريخ البداية، تاريخ النهاية، تاريخ الاستلام)
    4. حدد ما إذا كانت الشهادة مؤشرة من الطب المدرسي
    5. حدد ما إذا كانت الشهادة سلمت من طرف الولي
    6. أدخل ملاحظات إضافية إذا لزم الأمر
    7. انقر على "حفظ" لتسجيل الشهادة الطبية
    
    لعرض الشهادات الطبية ليوم معين:
    1. حدد خيار "عرض حسب التاريخ"
    2. اختر التاريخ المطلوب
    3. انقر على "عرض" لعرض الشهادات الطبية التي تشمل التاريخ المحدد
    
    لعرض الشهادات الطبية لتلميذ معين:
    1. حدد خيار "عرض حسب التلميذ"
    2. ابحث عن التلميذ وحدده
    3. انقر على "عرض" لعرض الشهادات الطبية للتلميذ المحدد
    """), styles['Arabic']))
    content.append(Spacer(1, 12))
    
    # إدارة التقارير السلوكية
    content.append(Paragraph(arabic_text("8. إدارة التقارير السلوكية"), styles['ArabicHeading']))
    content.append(Paragraph(arabic_text("""
    تتيح واجهة إدارة التقارير السلوكية القيام بالعمليات التالية:
    
    • إضافة تقرير سلوكي جديد
    • تعديل بيانات تقرير سلوكي
    • حذف تقرير سلوكي
    • عرض التقارير السلوكية لتلميذ معين
    
    لإضافة تقرير سلوكي جديد:
    1. انقر على زر "إضافة تقرير"
    2. ابحث عن التلميذ وحدده
    3. أدخل بيانات صاحب التقرير (الاسم واللقب، الوظيفة)
    4. إذا كان صاحب التقرير أستاذاً، أدخل التخصص
    5. أدخل تاريخ ووقت التقرير
    6. حدد الإجراءات المتخذة (يمكن اختيار أكثر من إجراء)
    7. إذا اخترت "استدعاء الولي"، أدخل معلومات الاستدعاء
    8. انقر على "حفظ" لتسجيل التقرير السلوكي
    """), styles['Arabic']))
    content.append(Spacer(1, 12))
    
    # إدارة استدعاءات الأولياء
    content.append(Paragraph(arabic_text("9. إدارة استدعاءات الأولياء"), styles['ArabicHeading']))
    content.append(Paragraph(arabic_text("""
    تتيح واجهة إدارة استدعاءات الأولياء القيام بالعمليات التالية:
    
    • تسجيل استدعاء جديد
    • تعديل بيانات استدعاء
    • حذف استدعاء
    • عرض الاستدعاءات المعلقة
    • عرض الاستدعاءات المبرمجة لتاريخ معين
    
    لتسجيل استدعاء جديد:
    1. انقر على زر "إضافة استدعاء"
    2. ابحث عن التلميذ وحدده
    3. أدخل اسم الولي
    4. أدخل اسم المستدعي (الشخص الذي طلب مقابلة الولي)
    5. أدخل تاريخ ووقت الاستدعاء
    6. حدد ما إذا كان الولي قد حضر أم لا
    7. أدخل ملاحظات إضافية إذا لزم الأمر
    8. انقر على "حفظ" لتسجيل الاستدعاء
    
    لعرض الاستدعاءات المعلقة:
    1. حدد خيار "عرض الاستدعاءات المعلقة"
    2. انقر على "عرض" لعرض الاستدعاءات التي لم يحضر فيها الأولياء بعد
    
    لعرض الاستدعاءات المبرمجة لتاريخ معين:
    1. حدد خيار "عرض حسب التاريخ"
    2. اختر التاريخ المطلوب
    3. انقر على "عرض" لعرض الاستدعاءات المبرمجة للتاريخ المحدد
    """), styles['Arabic']))
    content.append(Spacer(1, 12))
    
    # طباعة التقارير والإحصائيات
    content.append(Paragraph(arabic_text("10. طباعة التقارير والإحصائيات"), styles['ArabicHeading']))
    content.append(Paragraph(arabic_text("""
    تتيح واجهة طباعة التقارير والإحصائيات إنشاء وطباعة تقارير مختلفة، مثل:
    
    • قائمة التلاميذ
    • قائمة الأساتذة والعمال
    • إحصائيات الشهادات الطبية
    • إحصائيات التقارير السلوكية
    • إحصائيات استدعاءات الأولياء
    
    لطباعة تقرير:
    1. اختر نوع التقرير من القائمة
    2. حدد معايير التقرير (إن وجدت)
    3. انقر على "إنشاء التقرير" لإنشاء التقرير
    4. انقر على "طباعة" لطباعة التقرير أو "حفظ" لحفظه كملف PDF
    """), styles['Arabic']))
    content.append(Spacer(1, 12))
    
    # الدعم الفني
    content.append(Paragraph(arabic_text("11. الدعم الفني"), styles['ArabicHeading']))
    content.append(Paragraph(arabic_text("""
    إذا واجهتك أي مشاكل أثناء استخدام البرنامج، يرجى التواصل مع الدعم الفني عبر:
    
    • البريد الإلكتروني: support@schoolmanagement.com
    • الهاتف: 0123456789
    
    يرجى تقديم وصف تفصيلي للمشكلة ورسائل الخطأ (إن وجدت) لمساعدتنا في حل المشكلة بسرعة.
    """), styles['Arabic']))
    
    # بناء المستند
    doc.build(content)
    
    print(f"تم إنشاء دليل المستخدم بنجاح في: {user_guide_path}")
    return user_guide_path

if __name__ == "__main__":
    create_user_guide()
