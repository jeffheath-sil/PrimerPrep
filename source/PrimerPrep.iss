; -- PrimerPrep.iss --
; Inno Setup configuration for PrimerPrep.

[Setup]
AppId={{98147582-17F0-4551-B49E-DB30B1607314}
AppName=PrimerPrep
AppVersion=3.28
AppPublisher=SIL International
VersionInfoVersion=3.28
DefaultDirName={autopf}\SIL\PrimerPrep
DefaultGroupName=PrimerPrep
UninstallDisplayIcon={uninstallexe}
SetupIconFile=PrimerPrep.ico
Compression=lzma2
SolidCompression=yes
OutputBaseFilename=PrimerPrep Installer v3.28

[Files]
Source: "dist\PrimerPrep\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "CharisSILCompact-R.ttf"; DestDir: "{autofonts}"; FontInstall: "Charis SIL Compact Regular"; Flags: onlyifdoesntexist uninsneveruninstall
Source: "CharisSILCompact-B.ttf"; DestDir: "{autofonts}"; FontInstall: "Charis SIL Compact Bold"; Flags: onlyifdoesntexist uninsneveruninstall

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Icons]
Name: "{group}\PrimerPrep"; Filename: "{app}\PrimerPrep.exe"; IconFilename: "{app}\PrimerPrep.ico"; Comment: "Tool for preparing primers"
Name: "{group}\Uninstall PrimerPrep"; Filename: "{uninstallexe}"; IconFilename: "{app}\PrimerPrep.ico"
Name: "{autodesktop}\PrimerPrep"; Filename: "{app}\PrimerPrep.exe"; IconFilename: "{app}\PrimerPrep.ico"; Comment: "Tool for preparing primers"; Tasks: desktopicon

[Run]
Filename: "{app}\PrimerPrep.exe"; Description: "{cm:LaunchProgram,PrimerPrep}"; Flags: nowait postinstall skipifsilent

