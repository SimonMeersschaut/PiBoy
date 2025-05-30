const { app, BrowserWindow } = require('electron');
const path = require('path');

// This function creates the main window
function createWindow() {
    const mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        },
        autoHideMenuBar: true, // hides the menu bar by default
        frame: true            // true means standard window frame, false removes even the window borders and buttons
    });
    mainWindow.loadFile('index.html');
}


// Called when Electron is ready
app.whenReady().then(createWindow);

// On macOS, re-create a window in the app when the dock icon is clicked
app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});

// Quit when all windows are closed (except on macOS)
app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});