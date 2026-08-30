[Setup]
AppId={{7C4E6A91-3F28-4B75-9D62-8A1F5C73E204}
AppName=Pulse Music
AppVersion=0.1.0
AppPublisher=Barboza Software
DefaultDirName={autopf}\Pulse Music
DefaultGroupName=Pulse Music
OutputDir=..\release\windows
OutputBaseFilename=PulseMusicSetup v0.1.0
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "Criar atalho na área de trabalho"; GroupDescription: "Atalhos:"

[Files]
Source: "..\project\build\windows\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Pulse Music"; Filename: "{app}\Pulse Music.exe"
Name: "{autodesktop}\Pulse Music"; Filename: "{app}\Pulse Music.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\Pulse Music.exe"; Description: "Executar Pulse Music"; Flags: nowait postinstall skipifsilent