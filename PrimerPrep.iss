; -- PrimerPrep.iss --
; Inno Setup configuration for PrimerPrep.

[Setup]
AppId={{98147582-17F0-4551-B49E-DB30B1607314}
AppName=PrimerPrep
AppVersion=3.40
AppPublisher=SIL International
VersionInfoVersion=3.40
DefaultDirName={autopf}\SIL\PrimerPrep
DefaultGroupName=PrimerPrep
UninstallDisplayIcon={uninstallexe}
SetupIconFile=PrimerPrep.ico
Compression=lzma2
SolidCompression=yes
OutputBaseFilename=PrimerPrep Installer v3.40

[Files]
Source: "dist\PrimerPrep\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "PrimerPrep_project.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "CharisSIL-Regular.ttf"; DestDir: "{autofonts}"; FontInstall: "Charis SIL Regular"; Flags: onlyifdoesntexist uninsneveruninstall
Source: "CharisSIL-Bold.ttf"; DestDir: "{autofonts}"; FontInstall: "Charis SIL Bold"; Flags: onlyifdoesntexist uninsneveruninstall
Source: "CharisSILCompact-Regular.ttf"; DestDir: "{autofonts}"; FontInstall: "Charis SIL Compact Regular"; Flags: onlyifdoesntexist uninsneveruninstall
Source: "CharisSILCompact-Bold.ttf"; DestDir: "{autofonts}"; FontInstall: "Charis SIL Compact Bold"; Flags: onlyifdoesntexist uninsneveruninstall

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Icons]
Name: "{group}\PrimerPrep"; Filename: "{app}\PrimerPrep.exe"; IconFilename: "{app}\PrimerPrep.ico"; Comment: "Tool for preparing primers"
Name: "{group}\Uninstall PrimerPrep"; Filename: "{uninstallexe}"; IconFilename: "{app}\PrimerPrep.ico"
Name: "{autodesktop}\PrimerPrep"; Filename: "{app}\PrimerPrep.exe"; IconFilename: "{app}\PrimerPrep.ico"; Comment: "Tool for preparing primers"; Tasks: desktopicon

[Registry]
; Associate .ppdata extension with PrimerPrep
Root: HKCR; Subkey: ".ppdata"; ValueType: string; ValueData: "PrimerPrep.DataFile"; Flags: uninsdeletevalue
; Define the file type name
Root: HKCR; Subkey: "PrimerPrep.DataFile"; ValueType: string; ValueData: "PrimerPrep Data File"; Flags: uninsdeletekey
; Define the icon for .ppdata files
Root: HKCR; Subkey: "PrimerPrep.DataFile\DefaultIcon"; ValueType: string; ValueData: "{app}\PrimerPrep_project.ico"
; Define the command used to open .ppdata files
Root: HKCR; Subkey: "PrimerPrep.DataFile\shell\open\command"; ValueType: string; ValueData: """{app}\PrimerPrep.exe"" ""%1"""

[Run]
Filename: "{app}\PrimerPrep.exe"; Description: "{cm:LaunchProgram,PrimerPrep}"; Flags: nowait postinstall skipifsilent
