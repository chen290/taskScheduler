param(
    # Commands
    [Parameter(Mandatory=$false)]
    [string]
    $commands,

    # Flush
    [Parameter(Mandatory=$false)]
    [switch]
    $flush
)
if ($flush){
    Remove-Item 'tasks.node'
}
else{
    python ./taskScheduler.py $commands
}
