# Heads-Up
# You must have X11 or Wayland running before Electron will work, even after you install libgbm1.
sudo apt -y install xorg

# Install Libraries
sudo apt update
sudo apt install -y \
  libatk1.0-0 \
  libatk-bridge2.0-0 \
  libgtk-3-0 \
  libnss3 \
  libxss1 \
  libasound2 \
  libgconf-2-4 \
  libxtst6 \
  libx11-xcb1 \
  libgbm1

# Install Node.js on the Pi
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Install Electron on the pi
cd my-electron-app
npm install electron

# Verify instalation
node -v
npm -v