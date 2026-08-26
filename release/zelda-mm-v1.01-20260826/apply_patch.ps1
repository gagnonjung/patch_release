param(
  [Parameter(Mandatory=$true)]
  [ValidateSet('Nintendo64','HyundaiComboy64')]
  [string]$Variant,
  [Parameter(ValueFromRemainingArguments=$true)]
  [string[]]$InputFiles
)

$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Xdelta = Join-Path $Root 'tools\xdelta3.exe'
$SupportedMd5 = 'C38A7F6F6B61862EA383A75CDF888279'.ToLowerInvariant()
$SupportedSha256 = '7F81367323B3FACE9DFF8961ABE1937DF9F87A13C558EC038838C25490029BF3'.ToLowerInvariant()
$DialogTitle = 'Select the original Japanese Majora Mask Rev A ROM'
$Variants = @{
  'Nintendo64' = @{
    Patch = 'mm_ko_v1.01_nintendo64.xdelta'
    TargetMd5 = '9B109731BC9202514514A5C34257F868'.ToLowerInvariant()
    TargetSha256 = '63FA649670FE07086BD42A2C370D634A3D17B6BB32A03A186DAEA68363C08D1E'.ToLowerInvariant()
    OutputName = 'Zelda no Densetsu - Mujura no Kamen (Korea) (Rev A) [NINTENDO64].z64'
    Label = 'Nintendo 64'
  }
  'HyundaiComboy64' = @{
    Patch = 'mm_ko_v1.01_hyundai_comboy64.xdelta'
    TargetMd5 = 'C8DDA397C0ADAE03D736117BF2FDE918'.ToLowerInvariant()
    TargetSha256 = 'F9041331DBA2966DF2544333C2CA3E8B26BD8AB1531E3837263C65F8ED8C99DE'.ToLowerInvariant()
    OutputName = 'Zelda no Densetsu - Mujura no Kamen (Korea) (Rev A) [HYUNDAI-COMBOY64].z64'
    Label = 'Hyundai Comboy 64'
  }
}
$Config = $Variants[$Variant]
$Patch = Join-Path $Root $Config.Patch

function Get-HashHex([string]$Path, [string]$Algorithm) {
  return (Get-FileHash -LiteralPath $Path -Algorithm $Algorithm).Hash.ToLowerInvariant()
}
function Get-AvailableOutputPath([string]$Directory, [string]$FileName) {
  $candidate = Join-Path $Directory $FileName
  if (-not (Test-Path -LiteralPath $candidate)) { return $candidate }
  $stem = [System.IO.Path]::GetFileNameWithoutExtension($FileName)
  $ext = [System.IO.Path]::GetExtension($FileName)
  for ($i = 2; $i -le 999; $i++) {
    $candidate = Join-Path $Directory (('{0}_{1}{2}' -f $stem, $i, $ext))
    if (-not (Test-Path -LiteralPath $candidate)) { return $candidate }
  }
  throw 'Could not choose a free output file name.'
}
function Select-SourceFile {
  Add-Type -AssemblyName System.Windows.Forms
  $dialog = New-Object System.Windows.Forms.OpenFileDialog
  $dialog.Title = $DialogTitle
  $dialog.Filter = 'Nintendo 64 ROM (*.z64)|*.z64|All files (*.*)|*.*'
  $dialog.Multiselect = $false
  if ($dialog.ShowDialog() -ne [System.Windows.Forms.DialogResult]::OK) { return $null }
  return $dialog.FileName
}

if (-not (Test-Path -LiteralPath $Xdelta -PathType Leaf)) { throw 'tools\xdelta3.exe is missing.' }
if (-not (Test-Path -LiteralPath $Patch -PathType Leaf)) { throw ('Patch file is missing: {0}' -f $Config.Patch) }

if ($null -eq $InputFiles -or $InputFiles.Count -eq 0) {
  $picked = Select-SourceFile
  if ([string]::IsNullOrWhiteSpace($picked)) { exit 1 }
  $InputFiles = @($picked)
}

$Failures = 0
foreach ($InputFile in $InputFiles) {
  $TempOutput = $null
  try {
    $Source = [System.IO.Path]::GetFullPath([string]$InputFile)
    if (-not (Test-Path -LiteralPath $Source -PathType Leaf)) { throw ('Input file not found: {0}' -f $Source) }
    Write-Host ''
    Write-Host ('Variant: {0}' -f $Config.Label)
    Write-Host ('Input : {0}' -f $Source)
    $md5 = Get-HashHex $Source 'MD5'
    $sha = Get-HashHex $Source 'SHA256'
    if ($md5 -ne $SupportedMd5 -or $sha -ne $SupportedSha256) {
      throw ('Unsupported ROM. MD5={0}, SHA256={1}' -f $md5, $sha)
    }
    $OutputDirectory = Split-Path -Parent $Source
    $Output = Get-AvailableOutputPath $OutputDirectory $Config.OutputName
    $TempOutput = $Output + '.partial'
    if (Test-Path -LiteralPath $TempOutput) { Remove-Item -LiteralPath $TempOutput -Force }
    & $Xdelta -d -f -s $Source $Patch $TempOutput
    if ($LASTEXITCODE -ne 0) { throw ('xdelta3 failed with exit code {0}.' -f $LASTEXITCODE) }
    $actualMd5 = Get-HashHex $TempOutput 'MD5'
    $actualSha = Get-HashHex $TempOutput 'SHA256'
    if ($actualMd5 -ne $Config.TargetMd5 -or $actualSha -ne $Config.TargetSha256) {
      throw ('Output hash mismatch. MD5={0}, SHA256={1}' -f $actualMd5, $actualSha)
    }
    Move-Item -LiteralPath $TempOutput -Destination $Output
    $TempOutput = $null
    Write-Host '[OK] Patch complete and verified.' -ForegroundColor Green
    Write-Host ('MD5  : {0}' -f $actualMd5)
    Write-Host ('SHA256: {0}' -f $actualSha)
    Write-Host ('Created: {0}' -f $Output)
  }
  catch {
    if ($null -ne $TempOutput -and (Test-Path -LiteralPath $TempOutput)) { Remove-Item -LiteralPath $TempOutput -Force -ErrorAction SilentlyContinue }
    $Failures++
    Write-Host ('[ERROR] {0}' -f $_.Exception.Message) -ForegroundColor Red
  }
}
if ($Failures -gt 0) { exit 2 }
exit 0
