ZRPC is a simple and powerful tool to customize your Discord Rich Presence status using a GUI.  
You can show what you're doing (like playing GTA 6, coding, or listening to music) — no programming required.

---

## 📦 How to Use

1. **Download and run `ZRPC.exe`**
2. **Enter your Discord App's Client ID** (see below)
3. **Fill in description, image names, and time**
4. **Click “Launch”** to activate your Discord status

> No Python or installation required — just double-click the file.

---

## 🧙‍♂️ How to Set Up Rich Presence on Discord

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **"New Application"** and give it a name
3. Copy your **Client ID**
4. Go to **Rich Presence > Art Assets**
5. Upload images (recommended size: 512x512)
6. Use the image names exactly in ZRPC

---

## 💡 What Each Field Means

| Field                  | Description                                 |
|------------------------|---------------------------------------------|
| ClientID               | Your App's Client ID                        |
| Description Line 1     | Main title (e.g. Playing GTA 6)             |
| Description Line 2     | Subtitle (e.g. Story Mode - 87% Complete)   |
| Hours Ago              | How long ago activity started               |
| LargeImage             | Name of large image asset                   |
| SmallImage             | (Optional) Name of small image              |
| Tooltips               | Hover text for images                       |

---

## 📝 Profiles

- ZRPC lets you **save multiple profiles**
- They are stored in `profiles/` folder as `.ini` files
- You can load, edit, and relaunch them anytime

---

## 📌 Example Setup

- **ClientID:** `112233445566778899`
- **LargeImage:** `gtalogo`
- **Description Line 1:** Playing GTA 6
- **Description Line 2:** Vice City - Chapter 3
- **Hours Ago:** 5

This will show you're playing GTA 6 for the past 5 hours with your uploaded icon.

---

## 🔐 Is This Safe?

Yes. ZRPC uses Discord’s official Rich Presence system via the public `pypresence` library and your own App ID.  
No Discord token or login is ever required.

---

## 🧑‍💻 Credits

Made with ❤️ by Zartasht 
