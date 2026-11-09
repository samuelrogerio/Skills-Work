param(
    [Parameter(Mandatory=$true)][string]$Documento,
    [Parameter(Mandatory=$true)][string]$Pdf
)

$origem = (Resolve-Path -LiteralPath $Documento).Path
$destino = [System.IO.Path]::GetFullPath($Pdf)
[System.IO.Directory]::CreateDirectory([System.IO.Path]::GetDirectoryName($destino)) | Out-Null
$word = $null
$doc = $null
try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0
    $word.AutomationSecurity = 3
    $doc = $word.Documents.Open($origem, $false, $true, $false)
    $doc.ExportAsFixedFormat($destino, 17)
    $doc.Close($false)
    $word.Quit()
    Get-Item -LiteralPath $destino
}
finally {
    if ($doc -ne $null) { try { $doc.Close($false) } catch {} }
    if ($word -ne $null) { try { $word.Quit() } catch {} }
}
