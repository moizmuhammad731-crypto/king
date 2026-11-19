param(
    [Parameter(Mandatory=$true)][string]$Docx,
    [Parameter(Mandatory=$true)][string]$Pdf
)
$ErrorActionPreference = "Stop"
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
    $doc = $word.Documents.Open($Docx, $false, $false)
    $doc.Fields.Update() | Out-Null
    if ($doc.TablesOfContents.Count -eq 0) { throw "no TOC field found" }
    $toc = $doc.TablesOfContents.Item(1)
    $toc.Update() | Out-Null
    $toc.UpdatePageNumbers() | Out-Null

    # Reference index grammar: chapter rows bold, section rows regular and indented.
    foreach ($p in $toc.Range.Paragraphs) {
        $txt = $p.Range.Text.Trim()
        if ($txt.Length -eq 0) { continue }
        $p.Range.Font.Name = "Times New Roman"
        $p.LineSpacingRule = 0
        if ($txt -match '^(CHAPTER|ABSTRACT|ACKNOWLEDGEMENT|ALGORITHM DESIGN DOCUMENT|DEMONSTRATION)') {
            $p.Range.Font.Size = 11.5
            $p.Range.Font.Bold = $true
            $p.LeftIndent = 0
            $p.SpaceBefore = 8
            $p.SpaceAfter = 1
        } else {
            $p.Range.Font.Size = 10.5
            $p.Range.Font.Bold = $false
            $p.LeftIndent = 20
            $p.SpaceBefore = 0
            $p.SpaceAfter = 0
        }
    }

    $doc.Repaginate()
    $pages = $doc.ComputeStatistics(2)
    $doc.Save()
    $doc.SaveAs([ref]$Pdf, [ref]17)
    Write-Output ("pages=" + $pages)
    $doc.Close([ref]0)
} finally {
    $word.Quit()
}
