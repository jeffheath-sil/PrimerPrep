# show commands
set -x

# remove the previous build directories
rm -r build
rm -r dist
rm -r Output

# call PyInstaller to build the program in the "dist" folder
pyinstaller PrimerPrep-Folder.spec

# run Inno Setup to build the installer
/c/Program\ Files\ \(x86\)/Inno\ Setup\ 6/ISCC.exe PrimerPrep.iss
