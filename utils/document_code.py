#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
سكريبت توثيق الكود لنظام إدارة المدرسة
"""

import os
import re
import glob
from pathlib import Path

def document_code():
    """توثيق الكود المصدري للمشروع"""
    # تحديد مسار المشروع
    project_root = Path(__file__).parent.parent.parent.absolute()
    src_dir = project_root / "src"
    docs_dir = project_root / "docs"
    
    # إنشاء مجلد للوثائق
    os.makedirs(docs_dir, exist_ok=True)
    
    # مسار ملف التوثيق
    documentation_path = docs_dir / "code_documentation.md"
    
    # قائمة بالمجلدات التي سيتم توثيقها
    folders = [
        ("models", "نماذج قاعدة البيانات"),
        ("controllers", "وحدات التحكم"),
        ("views", "واجهات المستخدم"),
        ("utils", "أدوات مساعدة"),
        ("tests", "اختبارات")
    ]
    
    # بدء كتابة ملف التوثيق
    with open(documentation_path, "w", encoding="utf-8") as doc_file:
        # كتابة العنوان
        doc_file.write("# توثيق الكود المصدري لنظام إدارة المدرسة\n\n")
        
        # كتابة مقدمة
        doc_file.write("""
هذا المستند يوثق الكود المصدري لنظام إدارة المدرسة. يتضمن وصفاً لكل وحدة وملف في المشروع، مع شرح للوظائف والفئات الرئيسية.

## هيكل المشروع

```
school_management/
├── src/                    # الكود المصدري
│   ├── controllers/        # وحدات التحكم
│   ├── models/             # نماذج قاعدة البيانات
│   ├── views/              # واجهات المستخدم
│   ├── utils/              # أدوات مساعدة
│   ├── resources/          # موارد (صور، أيقونات، خطوط)
│   ├── tests/              # اختبارات
│   └── main.py             # نقطة الدخول الرئيسية
├── docs/                   # الوثائق
├── dist/                   # ملفات التوزيع
├── build/                  # ملفات البناء
├── installer/              # ملفات التثبيت
└── README.md               # ملف القراءة
```

## الملفات الرئيسية

""")
        
        # توثيق الملف الرئيسي
        main_file = src_dir / "main.py"
        if main_file.exists():
            doc_file.write("### main.py\n\n")
            doc_file.write("نقطة الدخول الرئيسية للتطبيق. يقوم بتهيئة قاعدة البيانات وإطلاق واجهة المستخدم الرئيسية.\n\n")
            
            # استخراج الوظائف من الملف الرئيسي
            with open(main_file, "r", encoding="utf-8") as f:
                content = f.read()
                functions = re.findall(r"def ([a-zA-Z0-9_]+)\(.*\):", content)
                if functions:
                    doc_file.write("**الوظائف الرئيسية:**\n\n")
                    for func in functions:
                        doc_file.write(f"- `{func}`: ")
                        # محاولة استخراج التعليق التوثيقي للوظيفة
                        doc_match = re.search(rf"def {func}\(.*\):.*?\"\"\"(.*?)\"\"\"", content, re.DOTALL)
                        if doc_match:
                            doc = doc_match.group(1).strip().split("\n")[0]
                            doc_file.write(f"{doc}\n")
                        else:
                            doc_file.write("(بدون توثيق)\n")
                    doc_file.write("\n")
        
        # توثيق كل مجلد
        for folder_name, folder_description in folders:
            folder_path = src_dir / folder_name
            if not folder_path.exists():
                continue
            
            doc_file.write(f"## {folder_description} ({folder_name}/)\n\n")
            doc_file.write(f"يحتوي مجلد `{folder_name}` على {folder_description} للتطبيق.\n\n")
            
            # الحصول على قائمة ملفات Python في المجلد
            py_files = list(folder_path.glob("*.py"))
            
            if not py_files:
                doc_file.write("لا توجد ملفات Python في هذا المجلد.\n\n")
                continue
            
            # توثيق كل ملف
            for py_file in sorted(py_files):
                file_name = py_file.name
                doc_file.write(f"### {file_name}\n\n")
                
                # قراءة محتوى الملف
                with open(py_file, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # استخراج التعليق التوثيقي للملف
                module_doc = re.search(r'"""(.*?)"""', content, re.DOTALL)
                if module_doc:
                    doc_file.write(f"{module_doc.group(1).strip()}\n\n")
                
                # استخراج الفئات
                classes = re.findall(r"class ([a-zA-Z0-9_]+)(?:\(.*?\))?:", content)
                if classes:
                    doc_file.write("**الفئات:**\n\n")
                    for cls in classes:
                        doc_file.write(f"- `{cls}`: ")
                        # محاولة استخراج التعليق التوثيقي للفئة
                        class_doc = re.search(rf"class {cls}(?:\(.*?\))?:.*?\"\"\"(.*?)\"\"\"", content, re.DOTALL)
                        if class_doc:
                            doc = class_doc.group(1).strip().split("\n")[0]
                            doc_file.write(f"{doc}\n")
                        else:
                            doc_file.write("(بدون توثيق)\n")
                    doc_file.write("\n")
                
                # استخراج الوظائف (خارج الفئات)
                # هذا تقريبي ولا يستبعد الوظائف داخل الفئات بشكل كامل
                functions = re.findall(r"^def ([a-zA-Z0-9_]+)\(.*\):", content, re.MULTILINE)
                if functions:
                    doc_file.write("**الوظائف:**\n\n")
                    for func in functions:
                        doc_file.write(f"- `{func}`: ")
                        # محاولة استخراج التعليق التوثيقي للوظيفة
                        func_doc = re.search(rf"def {func}\(.*\):.*?\"\"\"(.*?)\"\"\"", content, re.DOTALL)
                        if func_doc:
                            doc = func_doc.group(1).strip().split("\n")[0]
                            doc_file.write(f"{doc}\n")
                        else:
                            doc_file.write("(بدون توثيق)\n")
                    doc_file.write("\n")
            
            doc_file.write("\n")
        
        # إضافة معلومات إضافية
        doc_file.write("""
## تفاصيل التنفيذ

### نمط التصميم

تم تطوير النظام باستخدام نمط التصميم Model-View-Controller (MVC):

- **النماذج (Models)**: تمثل هيكل البيانات وتتعامل مع قاعدة البيانات.
- **العروض (Views)**: تمثل واجهة المستخدم وتعرض البيانات للمستخدم.
- **وحدات التحكم (Controllers)**: تربط بين النماذج والعروض وتحتوي على منطق الأعمال.

### التقنيات المستخدمة

- **Python**: لغة البرمجة الأساسية.
- **PyQt6**: لإنشاء واجهة المستخدم الرسومية.
- **SQLAlchemy**: للتعامل مع قاعدة البيانات بطريقة ORM.
- **SQLite**: كنظام قاعدة بيانات محلي.
- **Pandas**: لمعالجة البيانات واستيراد ملفات Excel.
- **ReportLab**: لإنشاء ملفات PDF وطباعة التقارير.
- **PyInstaller**: لإنشاء ملفات تنفيذية قابلة للتوزيع.

## الخاتمة

هذا التوثيق يقدم نظرة عامة على الكود المصدري لنظام إدارة المدرسة. للحصول على مزيد من التفاصيل حول استخدام النظام، يرجى الرجوع إلى دليل المستخدم.
""")
    
    print(f"تم إنشاء توثيق الكود بنجاح في: {documentation_path}")
    return documentation_path

if __name__ == "__main__":
    document_code()
