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

### Create a bot with _BotFather_

1. If you haven't already, install [_Telegram Desktop_ or _Telegram Mobile_ application](#1-telegram-desktop).
2. Go to <a href="https://t.me/botfather" target="_blank">this link</a> to start talking to _BotFather_.
3. Use the  `/newbot`  command to create a new bot. It will ask you to:
	1. **Choose a _name_ for your bot**
	This will be the name displayed in _Telegram_'s interface.
	2. **choose a _username_ for your bot**
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

### _ngrok_ Setup
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

### Clone This Repo

#### Option 1 - _git_

1. If you decided to [install _git_](#4-git), go to the location you would like to copy this repo to. 
<br>e.g. `C:\Users\MyUser\Projects\ImageProcessingBot\` on _Windows_,
<br>or `/home/myuser/Projects/ImageProcessingBot/ on _Linux_ or _Mac_`.
<br>You can copy it wherever you like.
2. Then run this command:
	```bash
	git clone https://github.com/Thebinoman/ImageProcessingService.git .
	```
	It will copy all this repo into the folder your terminal is running from.

#### Option 2 - Download and extract zip file

1. If you do not want to install git, just download the repo from the top of this page. You should see a green button with `<> code` in it. Click on it. You should be able to download a zip file from the popup menu.
2. Download the zip file and extract it to a location of your liking.

### Setup Virtual Environment
We need to setup a virtual environment for _Python_, install all dependency packages, and set the needed environment variables.
> [!WARNING] 
> When running _Python 3_, on some systems it's executable called simply `python`, and on some `python3`. Please ensure you are using the right one for your system.

Folow these steps:
1. [Create new virtual environment](#create-new-virtual-environment) 
2. [Inject environment variables](#inject-virtual-environment)
3. [Activate virtual environment](#activate-the-virtual-environment) 
4. [Install dependency packages](#install-dependency-packages) 
5. [Run the server!](#run-the-server) 

#### Create New Virtual Environment

1. Go to the location you cloned or exported this repo. For consistency, lets call this folder _"ImageProcessingBot"_.
2. Run the following command:
	```bash
	python -m venv venv
	```
	A new folder named `venv` should appear in your _"ImageProcessingBot"_ folder.

#### Inject Virtual Environment

We need to inject two environment variables into our new virtual environment. This process is a bit different on each terminal type:

##### On _Mac_ or _Linux_

1. With the editor of your choice, edit the file `ImageProcessingBot/venv/bin/activate`
2. Add the following lines at the top of the file, before all text:
	```bash
	export TELEGRAM_TOKEN="<your bot token>"
	export TELEGRAM_APP_URL="<fowarding URL from ngrok>"
	```

##### On _CMD_

1. With the editor of your choice, edit the file `ImageProcessingBot\venv\bin\activate.bat`
2. Add the following lines at the top of the file, before all text:
	```powershell
	set TELEGRAM_TOKEN="<your bot token>"
	set TELEGRAM_APP_URL="<fowarding URL from ngrok>"
	```

##### On _PowerShell_

1. Create a new file in `ImageProcessingBot\venv\bin\` and call it `Activate with Vars.ps1`.
> [!IMPORTANT]
> Make sure the extension of the file is `.ps1` and not something else like `.ps1.txt`. By default, the extension of the file is hidden in _Windows Explorer_. Go to `View` and check `File name extensions` to see the extensions of all files.
2. In the editor of your choice, edit the file, and add the following content:
	```powershell
	$Env:TELEGRAM_TOKEN  =  "<your bot token>"
	$Env:TELEGRAM_APP_URL  =  "<fowarding URL from ngrok>"
	&  "$(Split-Path  $MyInvocation.MyCommand.Path)/Activate.ps1"
	```

##### Finally

1. Replace `<your bot token>` with the [token you received from _BotFather_](#create-a-bot-with-botfather) when you created the bot. It should look something like this: `110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw`.
2. Replace `<fowarding URL from ngrok>` with the forwarding URL that is running on _ngrok_. It should look something like this: `https://16ae-2a06-c701-4501-3a00-ecce-30e9-3e61-3069.ngrok-free.app`.
3. Save the file.
> [!NOTE]
> The token will stay the same every time you run the server. However the forwarding URL will change every time you start _ngrok_. You have to re-edit the file and replace the injected URL.

#### Activate The Virtual Environment
From _"ImageProcessingBot"_, according to your system run the following:

##### On _Linux_ or _Mac_
```bash
venv/bin/activate
```
##### On _CMD_
```powershell
venv\Scripts\activate
```

##### On _PowerShell_

You may need to run this line before running the file:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
You will only have to run it once.

Then, run this line:
```powershell
& '.\venv\Scripts\Activate with Vars.ps1'
```

##### Finally

You should see `(venv)` before the new line in your terminal, that indicate that the virtual environment is activated.

#### Install Dependency Packages

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

### Done!
If you haven't already, go to the URL of your bot (`https://t.me/<username>`). You should find it in your [conversation with _BotFather_](#create-a-bot-with-botfather). You can now say `Hi!` to your new image processing bot!
<br>
<br>

## Adding Effects
 There are several aspects when implementing a new effect into the project:    
1. [The algorithm of the effect](#add-effect-algorithm) in `polybot/img_proc.py`
2. The [effect parsing rules](#effect-parsing-rules) in `polybot/effect_rules.py`
3. If needed, create new [argument rules](#Create-new-argument-rules) in `polybot/effect_arg_rules.py`
4. [Handle CommandErrors](#handling-command-errors-for-argument-rules) for the new argument rules (if needed)
5. [Add help replies](#add-help-replies-to-explain-how-to-use-your-effect) on `polybot/replies/Image_processing_bot_replies.json`

Let's go over each aspect...    

### Add Effect Algorithm
 In `polybot/img_proc.py`, you will find the `Img` class. This class is responsible to load, process, save and delete images. You will find all effects algorithms as methods (e.g `rotate`, `concat`, etc.).  
You will need to add a method with the name of your effect. Your effect name should match the common convention of naming methods in _Python_. In short it mostly means to name with _[Snake Case]((https://en.wikipedia.org/wiki/Snake_case))_ (e.g. `rbg_posterize` or `canvas_resize`).  
If you have arguments you want to pass from the user, you should add them to the method definition.  
In addition, if your effect uses a second image, add the second image as the first argument (after self), as an instance of `Img` class, and call it `other_img`. The images will be created automatically during the process of parsing the messages from the user.  

### Effect Parsing Rules
  
For parsing each effect's arguments, received from the user, there are rules written for each and every effect. These rules are located in `polybot/effect_rules.py`, in the dictionary `EffectRules`. You need to add your rules with a key, identical to the name of the method you created in `polybot/img_proc.py`.  
As a value you will create a new instance of `EffectArgParser`, with the following arguments:  
1. `arg_amount_start` - What is the minimal amount of arguments, necessary for the effect to process. (of type `int`)  
2. `arg_amount_end` - What is the maximum amount of arguments, needed for the effect to process. (of type `int`)  
3. `arg_rule_list` - A list of instances of `ArgRuleBase` as rules for the arguments. An instance as item in the list, for each argument. (list of items of `ArgRangeRule`/`ArgOptionRule`/`ArgPositiveInt`/`ArgColorRule`)  
4. `multi` - [Optional] Is your effect use two images. `True` = two images, `False` = one image. (of type `bool`). Default is `False`.
  
> [!IMPORTANT]
> If your effect is using two images, **do not** add the `other_img` as an argument, because it is not added as text in the message.  

For your convince, you can take a look of [this example](#example-of-implementing-effect-parsing-rules) of implementing the parsing rules of an effect. 

#### Effect Argument Rules
  
As mentioned above, when creating parsing rules for an effect, you add a list of items in `arg_rule_list`. For each argument the user is entering, required or optional, you need to specify the rule of parsing for that argument.  
There are currently 4 types of argument rules:
1. [ArgRangeRule](#argrangerule)
2. [ArgOptionRule](#argoptionrule)
3. [ArgPositiveInt](#argpositiveint)
4. [ArgColorRule](#argcolorrule)

The job of these argument rules is to parse the input argument from the sent message, convert them to values that can be passed into the methods for processing in `polybot/img_proc.py`, or return appropriate errors, that will later will be messaged back to the user.
<br>We'll go now over each argument rule... 

##### ArgRangeRule

This rule is for arguments that can have a value within a range. e.g. an argument that it's value must be between 0 to 255.  
It's arguments are:
<br>`start` - The minimum limit of the range (including).
<br>`end` - The maximum limit of the range (including).
<br>`convert_func` - [Optional] A function to convert the input (string) into the desired type (e.g. int or float). Default is `int`.  

##### ArgOptionRule

This rule is `enum`-like arguments. Their value must be on of a given list e.g.  one of `[90, -90, 180, 270]`.
It's arguments are:
<br>`options` - a list of optional values allowed.
<br>`convert_func` - [Optional] A function to convert the input (string) into the desired type (e.g. int or float). Default is `None` (stays string).

##### ArgPositiveInt

As the name suggests, this rule is for arguments with positive value, although 0 is also acceptable. The name is a bit misleading. It is actually non-negative argument.
<br>This argument rule has no input arguments of its own.

##### ArgColorRule

This rule is for parsing color values from the user. The user should enter  [HTML color name](https://www.w3schools.com/cssref/css_colors.php) or [hexadecimal color value](https://www.w3schools.com/colors/colors_hexadecimal.asp).
<br>This argument rule has no input arguments of its own.

#### Example of Implementing Effect Parsing Rules

After we understand what each and every argument rule does, it is easier to understand the syntax of writing parsing rules for effects.
<br>Let's look at the implementation of the rules for the `concat` effect. The following is taken from `polybot/effect_rules.py`.

```python
EffectRules = {
...
'concat': EffectArgParser(0, 2, [
        ArgOptionRule(['horizontal', 'vertical']),
        ArgColorRule()
    ], True),
...
}
```
You can see:
1. The key `'concat'` is identical to the name of the method `Img.concat` from `polybot/img_proc.py`.
2. The value is an instance of `EffectArgParser`.
3. The first argument `arg_amount_start` is `0`, meaning that this effect have no (0) required arguments.
4. The second argument `arg_amount_end` is `2`, meaning that this effect have the maximum of 2 arguments. If the user will enter more than 2 arguments to this effect, an error will be messaged in return.
5. The third argument is a list of argument rules:
   1. `ArgOptionRule(['horizontal', 'vertical'])` - an instance of `ArgOptionRule`. This argument can have the value `horizontal` or `vertical`. It will parse the value for the `direction` argument in the `concat` method from `Img` class, and its default value is defined in the definition of the method.
   2. `ArgColorRule()` - an instance of `ArgColorRule`. This argument can have a color value as described [here](#argcolorrule), and is parsing the value for the `bg_color` argument. Its default value is again defined in the `concat` method.
6. The forth and last is the `multi` argument, and it is set to `True`, which means that this effect require 2 images, and the first value of the method `concat` takes the second `Img` instance named `other_img`.

### Create New Argument Rules

If any of the 4 argument rules does not suit your effect needs, you can always create new ones on `polybot/effect_arg_rules.py`.
<br>Essentially, as mentioned [above](#effect-argument-rules), the argument rules responsible for:
1. Parsing the arguments from the message, so they can be injected into the processing methods in `Img` class
2. Or return errors when the input is not suitable for the effect.

<br>In addition:
- They are located in `polybot/effect_arg_rules.py`
- All of them are inheriting from `ArgRuleBase`.
- They all have a `parse` method for parsing the value or the errors.
- The `parse` method should have two arguments (beside self):
  1. `value` which will hold the value from the message as an incoming string
  2. `effect_string` that will hold the full string of the command of the effect, as writen in the message from the user.

> [!NOTE]
> When you create argument rules, you don't need to inject the values yourself. It is done automatically. You only need to add the argument rules to the appropriate effect rules, as explained [above](#effect-parsing-rules) and shown in [this example](#example-of-implementing-effect-parsing-rules).

In the `parse` method, you should return the value that the effect need to use as input, in case it is parsable and the input value string is valid according to the argument rule. Otherwise, it should return a `polybot.error.CommandError` instance.

### Handling Command Errors for Argument Rules

If the user has sent an argument for the given effect, in its message, in a way that does not match the rules of the argument rules (e.g. send a negative number for an argument rule of type `ArgPositiveInt`), you should reply an instance of `CommandError`.
<br>`CommandError` is taking two arguments to be created:
1. `error_type`
2. `error_args`

#### error_type:

Holds a string value, with the related key of response. More on error [replies and responses](#error-replies-and-responses-types) coming next.

#### error_args;

Is a list with the following structure:
- The first item is the `effect_string`, given as an input argument for the `parse` method.
- The last item is the `value`, again given as an input argument for the `parse` method.
- Between the first and the last items, you should insert all the data you want to dynamically respond to the user according to the corresponding reply format. More on that [below](#error-replies-and-responses-types).

### Error Replies and Responses Types

`polybot/replies/Image_processing_bot_replies.json` holds format strings for all the replies that can be sent to the user. The format strings:
- must embrace [_Telegram_'s `MarkdownV2`](https://core.telegram.org/bots/api#markdownv2-style) rules.
- can reference items from the `CommandError.error_args` list. e.g. if you will add the response `'Here is the first item of error_args: {0}'` than `{0}` will be replaced by the first item of `error_args` (which is the full command of the effect `effect_string`).

When adding an error reply for argument rules you must put them under the object `['photos']`, like `arg-not-color` or `arg-out-of-range`. According to the key of the reply you chose, you need to set it as `error_type` in the argument rule you create.
<br>In addition, in `polybot/response_types.py` you'll find reference of all the keys of all errors under the `ErrorTypes` class. you can add your own reference, and use it in your argument rules instead of inserting hard coded strings.

### Add Help Replies To Explain How To Use Your Effect

As mention in [_Error Replies and Responses Types_](#error-replies-and-responses-types), `polybot/replies/Image_processing_bot_replies.json` holds all replies that can be sent to the users. You should add to this file replies that present the user information about your new effect. There are two main places to add this info:
1. `['help']['help']` is the main response for general help to explain to the user how to use the bot and call command. It also lists all effect. You should add the name of your own effect in the appropriate location.
2. In `['help']`, alongside `['help']['help']`, you'll find a key for each effect, with a reply with the effect's details as the value. This reply is sent when the user is sending a message with the text `help <effect_name>` (e.g. `help concat`). Observe the pattern of the existing replies, and add your own for your new effect.

### Done!

If everything done correctly, your new effect should work and respond perfectly! just like the existing effects.