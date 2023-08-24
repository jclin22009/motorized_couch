## Ethernet Setup

### For MAC users:

1. Connect an Ethernet cable between your computer and the couch pi.
2. Turn on the couch pi.
3. Open a terminal and run this command 
    `ssh evelynn@couch`
4. When asked for a password, enter `potato`

### For Windows users:

1. If your PC runs Windows, [download Bonjour](https://support.apple.com/kb/DL999?locale=en_US) onto your PC and configure with all the default settings: This application will help interpret the Ethernet connection and find IP addresses for you. 
2. Download [Putty](https://www.putty.org/) with all the default settings.
3. Connect an Ethernet cable between your PC and the couch pi.
4. Turn on the couch pi.
5. Using Putty, enter `couch.local` as the RPi's hostname and login with the following:

    - Username: `evelynn`
    - Password: `potato`

After logging in:
1. Download [RealVNCViewer](https://www.realvnc.com/en/connect/download/viewer/) with the default settings and log into your RealVNC account (make an account if you don't have one).
2. Run `vncserver` in your terminal (Putty terminal for windows). The terminal will give you a VNC desktop to log into in the format `hostname.local:1`
3. Add a new connection in the RealVNCViewer and enter `couch.local:1` or whatever the terminal gave you.
4. Start the connection and log into the desktop with your SSH information. 
5. If you see the RPi Desktop, you're in!