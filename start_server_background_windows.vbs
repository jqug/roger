Set oShell = CreateObject ("Wscript.Shell") 
Dim strArgs
strArgs = "cmd /c run_app.cmd"
oShell.Run strArgs, 0, false