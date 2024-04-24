@echo on
REM Use this Batch file to build PrimerPrep Installer for Windows
REM by Jeff Heath (with inspiration from Mark Penny and Martin Hosken)
REM Last updated: Apr-2024

REM Delete any existing build folders before starting the new build process
rmdir /s /q build
rmdir /s /q dist

REM Call PyInstaller to build the program in the "dist" folder
pyinstaller PrimerPrep-Folder.spec

REM Call InnoSetup to build the final installer file for distribution
if "%INNOSETUP_PATH%"=="" (
    SET "INNOSETUP_PATH=%ProgramFiles(x86)%\Inno Setup 6"
)
"%INNOSETUP_PATH%\ISCC.exe" PrimerPrep.iss

echo Windows Installer executable file is located in "Output" folder
