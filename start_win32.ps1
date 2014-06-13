<## CONSTANTS ##>
# The port where the server will be deployed
$script:SERVER_PORT = 8000

# Whether to run with the bundled virtualenv or with global python variables.
# WARNING: This needs, at least, RemoteSigned execution policy
$script:RUN_WITH_VIRTUALENV = 1

<## FUNCTIONS ##>
function Write-Message($Message, $FColor='yellow', $BColor='black')
{
    Write-Host $Message -ForegroundColor $FColor -BackgroundColor $BColor
}

function Make-Preparations()
{
    if($script:RUN_WITH_VIRTUALENV) 
    {
        # Activate virtualenv with installed dependencies
        .\env\Scripts\activate.ps1
    }

    # Sync the database each time the script is launched
    .\taskrP\manage.py syncdb
}

function Start-Server() 
{
    # Starts the django development server
    .\taskrP\manage.py runserver $script:SERVER_PORT --insecure
}

Function Start-Pause($Message = 'Press any key to exit...')
{
    Write-Message $Message; [System.Console]::ReadKey($true) | Out-Null
}


<## SCRIPT START ##>
Try 
{
    Write-Message '-- TASKR POWERSHELL LAUNCHER v0.1 --'
    Write-Message 'Making preparations...'; Make-Preparations
    Write-Message 'Deploying server...'; Start-Server 
}
Catch [System.Exception] # Bad practice, but should not burp any exception unless touched with installation
{
    Write-Message 'Could not start the server, verify your installation' -fcolor 'red'
}
Finally
{
    Write-Message '-- END OF SCRIPT --'; Start-Pause
}
