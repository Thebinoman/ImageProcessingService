# Welcome to the Binoman's Image Processing Bot

The bot that uses digital effects that are available for the public for decades, like rotating and blurring an image, while having awful performance and mediocre results. All that goodness is brought to you in true RGB with 8-bits per channel, invented in the 80's with the old and over-sized VGA display. This is the one bot you never needed and never will.

## Setup

> [!CAUTION]
> This repo was created as an experiment. It is not built for production. The following setup guide is for development and testing only. If you want to deploy it for production, do your own research.

Here are the steps needed in order to run the bot:

- [Install dependencies](#install-dependencies)
- [Create a bot with _BotFather_](#create-a-bot-with-botfather)
- [Setup _ngrok_](#ngrok-setup) 
- [Clone This Repo](#clone-this-repo)
- [Setup virtual environment](#setup-virtual-environment)
- [Run the server](#run-the-server) 

### Install Dependencies

The bot server is a flask application, running on python and communication with Telegram's API.

These are the dependencies required to run the bot server in dev environment:

1. [_Telegram Desktop_](#1-telegram-desktop)
2. [_Python_ >= 3.9](#2-python)
3. [_ngrok_](#3-nkrok)
4. [_git_](#4-git) 

Lets go over them...

#### 1. Telegram Desktop

_Telegram Desktop_ is just for conveniency, but you must at least install it on your mobile phone. You can download and install _Telegram Desktop_ from <a href="https://desktop.telegram.org/" target="_blank">here</a>.
> [!NOTE] 
> You will probably have to download the _Telegram_ app on your mobile device, and connect it to your _Telegram Desktop_ app.

#### 2. Python

You can find instructions of how to install _Python_ on all platforms <a href="https://realpython.com/installing-python/" target="_blank">here</a>.
The bot should work on _Python 3.9_, and maybe even older, but it must be _Python 3_. This repo was tested on _Python 3.11.4_ and _3.12.2_.

#### 3. nkrok

_nkrok_ is also not a real requirement, but it is highly recommended. It exposes your port to the internet with much lower risk than you probably do yourself.
For instructions on how to download and install _ngrok_ please visit <a href="https://ngrok.com/download" target="_blank">here</a>.
<br>**TL:DR**: On _Windows_ it is recommended to install _ngrok_ using _Chocolatey_, on _Mac_ use _Homebrew_ and on _Linux_ it depends on your destro and your machine's architecture.

#### 4. git

It is also possible to avoid installing git. We use it to clone this repo. If you don't want to install it, you can download the zip file from this page instead of cloning.
<a href="https://git-scm.com/book/en/v2/Getting-Started-Installing-Git" target="_blank">Here</a> are the instructions of how to download and install git on your platform.

## Create a bot with _BotFather_

1. If you haven't already, install [_Telegram Desktop_ or _Telegram Mobile_ application](#1-telegram-desktop).
2. Go to <a href="https://t.me/botfather" target="_blank">this link</a> to start talking to _BotFather_.
3. Use the  `/newbot`  command to create a new bot. It will ask you to:
	a. **Choose a _name_ for your bot**
	This will be the name displayed in _Telegram_'s interface.
	b. **choose a _username_ for your bot**
	This will be the url for you bot like this: `https://t.me/<username>`
> [!WARNING] 
> You cannot change the _username_ after you create the bot. You can change the _name_ however.
4. After creating the bot successfully, _BotFather_ will reply with a message to congrat you for your new bot. In this message, you should find a token string that looks like this:
	```
	110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw
	```
	You will need this token later
> [!IMPORTANT]
> **Never** share tokens with anyone, and **DON'T** commit your tokens in Git repos, even if the repo is private.
    
You should also see the URL of your bot in the message (`https://t.me/<username>`). You can click on it to chat with the bot. The bot will not answer back, because we haven't setup and got the bot running yet.

## _ngrok_ Setup
> [!NOTE] 
> _ngrok_ is not required but highly recommended. It securely exposes a port for you to the internet and gives you a temporary URL, so Telegram could communicate with your bot server. If you prefer to do it differently, do your own research.

Please follow these steps to setup _ngrok_
1. If you haven't already, [download and install _ngrok_](#3-nkrok).
2. Go to <a href="https://ngrok.com/" target="_blank">https://ngrok.com/</a> and signup.
3. After signing in, you should see a line like this:
	```bash
	ngrok config add-authtoken <your-authtoken>
	```
	Run this line, with the token you see in _ngrok_'s site, in your terminal (_bash_/_Powershell_/_CMD_).
>[!NOTE] You need to run the line above only once.
4. Then, run the next line:
	```bash
	ngrok http 8443
	```
	Your bot public URL is the URL specified in the `Forwarding` line.
	e.g. `https://16ae-2a06-c701-4501-3a00-ecce-30e9-3e61-3069.ngrok-free.app`
5. Keep _ngrok_ running in your terminal, and we will also need this URL later...

## Clone This Repo

### Option 1 - _git_

1. If you decided to [install _git_](#4-git), go to the location you would like to copy this repo to. 
<br>e.g. `C:\Users\MyUser\Projects\ImageProcessingBot\` on _Windows_,
<br>or `/home/myuser/Projects/ImageProcessingBot/ on _Linux_ or _Mac_`.
<br>You can copy it wherever you like.
2. Then run this command:
	```bash
	git clone https://github.com/Thebinoman/ImageProcessingService.git .
	```
	It will copy all this repo into the folder your terminal is running from.

### Option 2 - Download and extract zip file

1. If you do not want to install git, just download the repo from the top of this page. You should see a green button with `<> code` in it. Click on it. You should be able to download a zip file from the popup menu.
2. Download the zip file and extract it to a location of your liking.

## Setup Virtual Environment
We need to setup a virtual environment for _Python_, install all dependency packages, and set the needed environment variables.
> [!WARNING] 
> When running _Python 3_, on some systems it's executable called simply `python`, and on some `python3`. Please ensure you are using the right one for your system.

Folow these steps:
1. [Create new virtual environment](#create-new-virtual-environment) 
2. [Inject environment variables](#inject-virtual-environment)
3. [Activate virtual environment](#activate-the-virtual-environment) 
4. [Install dependency packages](#install-dependency-packages) 
5. [Run the server!](#run-the-server) 

### Create New Virtual Environment

1. Go to the location you cloned or exported this repo. For consistency, lets call this folder _"ImageProcessingBot"_.
2. Run the following command:
	```bash
	python -m venv venv
	```
	A new folder named `venv` should appear in your _"ImageProcessingBot"_ folder.

### Inject Virtual Environment

We need to inject two environment variables into our new virtual environment. This process is a bit different on each terminal type:

#### On _Mac_ or _Linux_

1. With the editor of your choice, edit the file `ImageProcessingBot/venv/bin/activate`
2. Add the following lines at the top of the file, before all text:
	```bash
	export TELEGRAM_TOKEN="<your bot token>"
	export TELEGRAM_APP_URL="<fowarding URL from ngrok>"
	```

#### On _CMD_

1. With the editor of your choice, edit the file `ImageProcessingBot\venv\bin\activate.bat`
2. Add the following lines at the top of the file, before all text:
	```powershell
	set TELEGRAM_TOKEN="<your bot token>"
	set TELEGRAM_APP_URL="<fowarding URL from ngrok>"
	```

#### On _PowerShell_

1. Create a new file in `ImageProcessingBot\venv\bin\` and call it `Activate with Vars.ps1`.
> [!IMPORTANT]
> Make sure the extension of the file is `.ps1` and not something else like `.ps1.txt`. By default, the extension of the file is hidden in _Windows Explorer_. Go to `View` and check `File name extensions` to see the extensions of all files.
2. In the editor of your choice, edit the file, and add the following content:
	```powershell
	$Env:TELEGRAM_TOKEN  =  "<your bot token>"
	$Env:TELEGRAM_APP_URL  =  "<fowarding URL from ngrok>"
	&  "$(Split-Path  $MyInvocation.MyCommand.Path)/Activate.ps1"
	```

#### Finally

1. Replace `<your bot token>` with the [token you received from _BotFather_](#create-a-bot-with-botfather) when you created the bot. It should look something like this: `110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw`.
2. Replace `<fowarding URL from ngrok>` with the forwarding URL that is running on _ngrok_. It should look something like this: `https://16ae-2a06-c701-4501-3a00-ecce-30e9-3e61-3069.ngrok-free.app`.
3. Save the file.
> [!NOTE]
> The token will stay the same every time you run the server. However the forwarding URL will change every time you start _ngrok_. You have to re-edit the file and replace the injected URL.

### Activate The Virtual Environment
From _"ImageProcessingBot"_, according to your system run the following:

#### On _Linux_ or _Mac_
```bash
venv/bin/activate
```
#### On _CMD_
```powershell
venv\Scripts\activate
```

#### On _PowerShell_

You may need to run this line before running the file:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
You will only have to run it once.

Then, run this line:
```powershell
& '.\venv\Scripts\Activate with Vars.ps1'
```

#### Finally

You should see `(venv)` before the new line in your terminal, that indicate that the virtual environment is activated.

### Install Dependency Packages

From _"ImageProcessingBot"_, run this line:
```bash
pip install -r polybot/requirements.txt
```
You should see pip installing the packages.

### Run The Server!

If everything done correctly, you could run the following line, and the bot should be alive and active:
```bash
python -m polybot.app
```

## Done!
If haven't already, go to the URL of your bot (`https://t.me/<username>`). You should find it in your [conversation with _BotFather_](#create-a-bot-with-botfather). You can now say `Hi!` to your new image processing bot!