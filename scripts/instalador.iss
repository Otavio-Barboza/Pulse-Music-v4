[Setup]
AppId={{NOVO-GUID-AQUI}
AppName=Pulse Music
AppVersion=0.1.0
AppPublisher=Barboza Software
DefaultDirName={autopf}\Pulse Music
DefaultGroupName=Pulse Music
OutputDir=..\Release\Windows
OutputBaseFilename=PulseMusicSetup v0.1.0
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "Criar atalho na área de trabalho"; GroupDescription: "Atalhos:"

[Files]
Source: "..\Project\build\windows\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Pulse Music"; Filename: "{app}\pulse_music.exe"
Name: "{autodesktop}\Pulse Music"; Filename: "{app}\pulse_music.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\pulse_music.exe"; Description: "Executar Pulse Music"; Flags: nowait postinstall skipifsilent