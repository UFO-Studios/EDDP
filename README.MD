# Elite:Dangerous Discord Presence 
![EDDP Logo](https://beta.thealiendoctor.com/img/eddp.png)

## Usage (Manual):

Download the exe<br>
Run the exe<br>
Open Elite:Dangerous<br>
The exe should show up in your system tray (bottom right)<br>

## Usage (Automatic):

Download the exe<br>
Copy the exe to "C:\Users\YOUR_USERNAME\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup".<br></br>
Replace "YOUR_USERNAME" with your window username. (This can be found by checking the "C:/Users" folder for you account) <br></br>
Reboot your PC<br></br>
The folder you moved EDDP to, windows opens all of these on startup. <br></br>
The exe should show up in your system tray (bottom right) when running<br></br>

## FAQ
- Q: How do I know this is safe?
- A: You can check the source code yourself, or you can download the exe from the releases page. The EXE is signed with my GPG key, and the signature is avalible on the releases page. You should expect the following output when running `gpg --verify EDDP.exe.sig EDDP.exe`:
<br></br>
![GPG output](https://cdn.niceygylive.xyz/gpg.png)

- Q: What do I do if I find a bug?
- A: Open an issue! You can open them [here](https://github.com/ufo-studios/eddp/issues)