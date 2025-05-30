# Install Node.js on the Pi
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Install Electron on the pi
cd /home/pi/Desktop/PiBoy/my-electron-app/
npm install electron

# Verify instalation
node -v
npm -v

# Run
npx electron .