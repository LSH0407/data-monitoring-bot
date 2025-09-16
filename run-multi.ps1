param(
    [string[]]$Exchanges = @('NASDAQ','NYSE','OPRA')
)
$procs = @()
foreach ($ex in $Exchanges) {
    $env:EXCHANGE = $ex
    Write-Host "[spawn] starting monitor for $ex"
    $p = Start-Process powershell -ArgumentList "-ExecutionPolicy Bypass","-Command","$env:EXCHANGE='$ex'; python -m src.main" -PassThru -WindowStyle Minimized
    $procs += $p
}
Write-Host "[spawn] started $($procs.Count) processes."
