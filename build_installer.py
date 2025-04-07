#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
سكريبت إنشاء حزمة التثبيت لنظام إدارة المدرسة
"""

import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path

# تحديد المسارات
PROJECT_ROOT = Path(__file__).parent.parent.absolute()
DIST_DIR = PROJECT_ROOT / "dist"
BUILD_DIR = PROJECT_ROOT / "build"
INSTALLER_DIR = PROJECT_ROOT / "installer"

def clean_directories():
    """تنظيف المجلدات السابقة"""
    print("تنظيف المجلدات السابقة...")
    for directory in [DIST_DIR, BUILD_DIR, INSTALLER_DIR]:
        if directory.exists():
            shutil.rmtree(directory)
        directory.mkdir(parents=True, exist_ok=True)

def create_requirements_file():
    """إنشاء ملف متطلبات التثبيت"""
    print("إنشاء ملف متطلبات التثبيت...")
    requirements = [
        "PyQt6==6.5.0",
        "SQLAlchemy==2.0.0",
        "pandas==2.0.0",
        "openpyxl==3.1.0",
        "reportlab==3.6.0",
        "arabic-reshaper==3.0.0",
        "python-bidi==0.4.2",
        "pyinstaller==5.0.0"
    ]
    
    with open(PROJECT_ROOT / "requirements.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(requirements))

def install_requirements():
    """تثبيت المتطلبات"""
    print("تثبيت المتطلبات...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(PROJECT_ROOT / "requirements.txt")])

def create_spec_file():
    """إنشاء ملف مواصفات PyInstaller"""
    print("إنشاء ملف مواصفات PyInstaller...")
    spec_content = f"""# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['{str(PROJECT_ROOT / "src" / "main.py")}'],
    pathex=['{str(PROJECT_ROOT / "src")}'],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='نظام إدارة المدرسة',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='{str(PROJECT_ROOT / "src" / "resources" / "icon.ico") if os.path.exists(str(PROJECT_ROOT / "src" / "resources" / "icon.ico")) else None}',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='نظام إدارة المدرسة',
)
"""
    
    with open(PROJECT_ROOT / "school_management.spec", "w", encoding="utf-8") as f:
        f.write(spec_content)

def create_resources():
    """إنشاء الموارد اللازمة"""
    print("إنشاء الموارد اللازمة...")
    resources_dir = PROJECT_ROOT / "src" / "resources"
    resources_dir.mkdir(parents=True, exist_ok=True)
    
    # إنشاء أيقونة التطبيق إذا لم تكن موجودة
    icon_path = resources_dir / "icon.ico"
    if not icon_path.exists():
        # يمكن إضافة كود لإنشاء أيقونة افتراضية هنا
        pass

def build_application():
    """بناء التطبيق باستخدام PyInstaller"""
    print("بناء التطبيق...")
    subprocess.run([
        sys.executable, 
        "-m", 
        "PyInstaller", 
        "--clean",
        str(PROJECT_ROOT / "school_management.spec")
    ])

def create_installer():
    """إنشاء ملف التثبيت"""
    print("إنشاء ملف التثبيت...")
    
    # نسخ ملفات إضافية إلى مجلد التوزيع
    dist_dir = DIST_DIR / "نظام إدارة المدرسة"
    
    # نسخ دليل المستخدم
    user_guide_path = PROJECT_ROOT / "docs" / "user_guide.pdf"
    if user_guide_path.exists():
        shutil.copy(user_guide_path, dist_dir)
    
    # إنشاء ملف README
    with open(dist_dir / "README.txt", "w", encoding="utf-8") as f:
        f.write("""نظام إدارة المدرسة
==============

شكراً لاستخدامك نظام إدارة المدرسة!

للبدء في استخدام البرنامج، انقر مرتين على ملف "نظام إدارة المدرسة.exe".

للحصول على مساعدة، يرجى الرجوع إلى دليل المستخدم المرفق "user_guide.pdf".

إذا واجهتك أي مشاكل، يرجى التواصل مع الدعم الفني.
""")
    
    # إنشاء ملف تثبيت باستخدام NSIS (للويندوز) أو DMG (للماك)
    if platform.system() == "Windows":
        create_windows_installer()
    elif platform.system() == "Darwin":  # macOS
        create_macos_installer()
    else:  # Linux
        create_linux_installer()

def create_windows_installer():
    """إنشاء ملف تثبيت لنظام ويندوز"""
    print("إنشاء ملف تثبيت لنظام ويندوز...")
    
    # إنشاء سكريبت NSIS
    nsis_script = """
; نظام إدارة المدرسة - سكريبت التثبيت

!include "MUI2.nsh"

; معلومات عامة
Name "نظام إدارة المدرسة"
OutFile "installer\\نظام إدارة المدرسة-Setup.exe"
InstallDir "$PROGRAMFILES\\نظام إدارة المدرسة"
InstallDirRegKey HKCU "Software\\نظام إدارة المدرسة" ""

; إعدادات الواجهة
!define MUI_ABORTWARNING
!define MUI_ICON "${NSISDIR}\\Contrib\\Graphics\\Icons\\modern-install.ico"
!define MUI_UNICON "${NSISDIR}\\Contrib\\Graphics\\Icons\\modern-uninstall.ico"

; صفحات المعالج
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

; اللغات
!insertmacro MUI_LANGUAGE "Arabic"

; قسم التثبيت
Section "تثبيت البرنامج" SecInstall
  SetOutPath "$INSTDIR"
  
  ; نسخ الملفات
  File /r "dist\\نظام إدارة المدرسة\\*.*"
  
  ; إنشاء اختصار في قائمة ابدأ
  CreateDirectory "$SMPROGRAMS\\نظام إدارة المدرسة"
  CreateShortcut "$SMPROGRAMS\\نظام إدارة المدرسة\\نظام إدارة المدرسة.lnk" "$INSTDIR\\نظام إدارة المدرسة.exe"
  CreateShortcut "$SMPROGRAMS\\نظام إدارة المدرسة\\إلغاء التثبيت.lnk" "$INSTDIR\\Uninstall.exe"
  
  ; إنشاء اختصار على سطح المكتب
  CreateShortcut "$DESKTOP\\نظام إدارة المدرسة.lnk" "$INSTDIR\\نظام إدارة المدرسة.exe"
  
  ; تسجيل معلومات إلغاء التثبيت
  WriteRegStr HKCU "Software\\نظام إدارة المدرسة" "" $INSTDIR
  WriteUninstaller "$INSTDIR\\Uninstall.exe"
SectionEnd

; قسم إلغاء التثبيت
Section "Uninstall"
  ; حذف الملفات
  RMDir /r "$INSTDIR"
  
  ; حذف الاختصارات
  Delete "$SMPROGRAMS\\نظام إدارة المدرسة\\نظام إدارة المدرسة.lnk"
  Delete "$SMPROGRAMS\\نظام إدارة المدرسة\\إلغاء التثبيت.lnk"
  RMDir "$SMPROGRAMS\\نظام إدارة المدرسة"
  Delete "$DESKTOP\\نظام إدارة المدرسة.lnk"
  
  ; حذف معلومات التسجيل
  DeleteRegKey HKCU "Software\\نظام إدارة المدرسة"
SectionEnd
"""
    
    with open(PROJECT_ROOT / "installer.nsi", "w", encoding="utf-8") as f:
        f.write(nsis_script)
    
    # تنفيذ سكريبت NSIS (إذا كان متاحاً)
    try:
        subprocess.run(["makensis", str(PROJECT_ROOT / "installer.nsi")])
    except FileNotFoundError:
        print("تحذير: لم يتم العثور على برنامج NSIS. يرجى تثبيته لإنشاء ملف التثبيت.")
        print("يمكنك استخدام مجلد التوزيع مباشرة: " + str(DIST_DIR / "نظام إدارة المدرسة"))

def create_macos_installer():
    """إنشاء ملف تثبيت لنظام ماك"""
    print("إنشاء ملف تثبيت لنظام ماك...")
    # يمكن استخدام أدوات مثل create-dmg لإنشاء ملف DMG
    print("تحذير: لم يتم تنفيذ إنشاء ملف تثبيت لنظام ماك. يرجى استخدام مجلد التوزيع مباشرة.")

def create_linux_installer():
    """إنشاء ملف تثبيت لنظام لينكس"""
    print("إنشاء ملف تثبيت لنظام لينكس...")
    # يمكن إنشاء حزمة DEB أو RPM
    print("تحذير: لم يتم تنفيذ إنشاء ملف تثبيت لنظام لينكس. يرجى استخدام مجلد التوزيع مباشرة.")

def create_zip_package():
    """إنشاء ملف مضغوط للتطبيق"""
    print("إنشاء ملف مضغوط للتطبيق...")
    shutil.make_archive(
        str(INSTALLER_DIR / "نظام إدارة المدرسة"),
        'zip',
        str(DIST_DIR),
        "نظام إدارة المدرسة"
    )
    print(f"تم إنشاء ملف مضغوط في: {INSTALLER_DIR / 'نظام إدارة المدرسة.zip'}")

def main():
    """الدالة الرئيسية"""
    print("بدء إنشاء حزمة التثبيت لنظام إدارة المدرسة...")
    
    # تنفيذ خطوات إنشاء حزمة التثبيت
    clean_directories()
    create_requirements_file()
    install_requirements()
    create_resources()
    create_spec_file()
    build_application()
    create_installer()
    create_zip_package()
    
    print("تم الانتهاء من إنشاء حزمة التثبيت بنجاح!")

if __name__ == "__main__":
    main()
