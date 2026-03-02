# Source - https://stackoverflow.com/a/13992221
# Posted by Ten98, modified by community. See post 'Timeline' for change history
# Retrieved 2026-02-26, License - CC BY-SA 3.0

[int]$LinesInFile = 0
$reader = New-Object IO.StreamReader 'P:\Projects\PhySimTwin\01 Munich bridge data\Export\Neuer Ordner\UniBw_2022-04-08_ref_ambient_0125.csv'
 while($reader.ReadLine() -ne $null){ $LinesInFile++ }

# Print value on screen
write-output $LinesInFile

# Close the file at the end of the process
$reader.Dispose()
