; AgriSage (桂收·甘蔗专用版) 安装脚本
; 使用 Inno Setup 6.x 编译
; 内嵌中文消息，无需外部语言文件

#define MyAppName "桂收 · 甘蔗专用版"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "AgriSage"
#define MyAppURL "https://github.com/AgriSage"
#define MyAppExeName "AgriSage.exe"
#define MyAppAssocName "AgriSage Cane"
#define MyAppAssocExt ".agrisage"
#define MyAppAssocKeyString "AgriSage.Cane.File"

[Setup]
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
InfoBeforeFile=..\docs\INSTALL_NOTES.txt
OutputDir=..\installer
OutputBaseFilename=AgriSage-Setup-{#MyAppVersion}
SetupIconFile=favicon.ico
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequired=lowest
UninstallDisplayIcon={app}\{#MyAppExeName}
UninstallDisplayName={#MyAppName}
VersionInfoDescription={#MyAppName} 安装程序
VersionInfoProductName={#MyAppName}
VersionInfoProductVersion={#MyAppVersion}
VersionInfoCompany={#MyAppPublisher}

[Languages]
Name: "chinese"; MessagesFile: "compiler:Default.isl"

[Messages]
chinese.SetupAppTitle=安装
chinese.SetupWindowTitle=安装 - %1
chinese.UninstallAppTitle=卸载
chinese.UninstallAppFullTitle=%1 卸载
chinese.InformationTitle=信息
chinese.ConfirmTitle=确认
chinese.ErrorTitle=错误
chinese.ClickNext=点击"下一步"继续，或点击"取消"退出安装程序。
chinese.WelcomeLabel1=欢迎使用 [name] 安装向导
chinese.WelcomeLabel2=现在将安装 [name/ver] 到您的电脑中。%n%n推荐您在继续安装前关闭所有其它应用程序。
chinese.WizardSelectDir=选择目标位置
chinese.SelectDirDesc=您想将 [name] 安装在哪里？
chinese.SelectDirLabel3=安装程序将安装 [name] 到下列文件夹中。
chinese.SelectDirBrowseLabel=点击"下一步"继续。如果您想选择其它文件夹，点击"浏览"。
chinese.DiskSpaceMBLabel=至少需要有 [mb] MB 的可用磁盘空间。
chinese.DirExistsTitle=文件夹已存在
chinese.DirExists=文件夹：%n%n%1%n%n已经存在。您一定要安装到这个文件夹中吗？
chinese.DirDoesntExistTitle=文件夹不存在
chinese.DirDoesntExist=文件夹：%n%n%1%n%n不存在。您想要创建此文件夹吗？
chinese.WizardReady=准备安装
chinese.ReadyLabel1=安装程序现在准备开始安装 [name] 到您的电脑中。
chinese.ReadyLabel2a=点击"安装"继续此安装程序。如果您想要回顾或修改设置，请点击"上一步"。
chinese.ReadyMemoDir=目标位置：
chinese.WizardPreparing=正在准备安装
chinese.PreparingDesc=安装程序正在准备安装 [name] 到您的电脑中。
chinese.WizardInstalling=正在安装
chinese.InstallingLabel=安装程序正在安装 [name] 到您的电脑中，请稍等。
chinese.FinishedHeadingLabel=[name] 安装完成
chinese.FinishedLabelNoIcons=安装程序已在您的电脑中安装了 [name]。
chinese.FinishedLabel=安装程序已在您的电脑中安装了 [name]。此应用程序可以通过选择安装的快捷方式运行。
chinese.ClickFinish=点击"完成"退出安装程序。
chinese.ButtonBack=< 上一步(&B)
chinese.ButtonNext=下一步(&N) >
chinese.ButtonInstall=安装(&I)
chinese.ButtonOK=确定
chinese.ButtonCancel=取消
chinese.ButtonYes=是(&Y)
chinese.ButtonNo=否(&N)
chinese.ButtonFinish=完成(&F)
chinese.ButtonBrowse=浏览(&B)...
chinese.SetupAborted=安装程序未完成安装。%n%n请修正这个问题并重新运行安装程序。
chinese.ExitSetupTitle=退出安装程序
chinese.ExitSetupMessage=安装程序尚未完成安装。如果您现在退出，程序将不能安装。%n%n您可以以后再运行安装程序完成安装。%n%n现在退出安装程序吗？

[Tasks]
Name: "desktopicon"; Description: "创建桌面快捷方式"; GroupDescription: "附加图标:"; Flags: unchecked
Name: "quicklaunchicon"; Description: "创建快速启动栏快捷方式"; GroupDescription: "附加图标:"; Flags: unchecked; OnlyBelowVersion: 6.1

[Files]
Source: "..\dist\AgriSage\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\dist\AgriSage\*.dll"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\dist\AgriSage\*.pyd"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\dist\AgriSage\frontend\*"; DestDir: "{app}\frontend"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\dist\AgriSage\tiles\*"; DestDir: "{app}\tiles"; Flags: ignoreversion recursesubdirs createallsubdirs skipifsourcedoesntexist
Source: "favicon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Dirs]
Name: "{app}\uploads"
Name: "{app}\data"

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\卸载 {#MyAppName}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "运行 桂收 · 甘蔗专用版"; Flags: nowait postinstall skipifsilent

[Registry]
Root: HKCR; Subkey: ".agrisage"; ValueType: string; ValueName: ""; ValueData: "{#MyAppAssocKeyString}"; Flags: uninsdeletevalue
Root: HKCR; Subkey: "{#MyAppAssocKeyString}"; ValueType: string; ValueName: ""; ValueData: "{#MyAppAssocName}"; Flags: uninsdeletekey
Root: HKCR; Subkey: "{#MyAppAssocKeyString}\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\{#MyAppExeName},0"
Root: HKCR; Subkey: "{#MyAppAssocKeyString}\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""

[InstallDelete]
Type: filesandordirs; Name: "{app}"

[Code]
function InitializeSetup(): Boolean;
var
  ResultCode: Integer;
begin
  Result := True;
  Exec('taskkill', '/f /im AgriSage.exe', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
end;

function InitializeUninstall(): Boolean;
var
  ResultCode: Integer;
begin
  Result := True;
  Exec('taskkill', '/f /im AgriSage.exe', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
  Sleep(1000);
end;
