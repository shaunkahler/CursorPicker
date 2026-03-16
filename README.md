# CursorPicker

A desktop launcher for Cursor projects

## How to build the .exe (Windows)

**Requirements:** Python 3.10+ installed and on your PATH  
(download from https://python.org if needed — tick "Add to PATH" during install)

### Steps

1. Put both files in the same folder:
   - `cursor_picker.py`
   - `build.bat`

2. Double-click **`build.bat`**

3. Wait ~30 seconds — it installs PyInstaller and compiles everything.

4. **`CursorPicker.exe`** appears in the same folder. Done!

---

## Usage

- **Add Project** — click the purple button, pick any folder
- **Open in Cursor** — click anywhere on a project card
- **Remove** — click the ✕ on the right of any card

Your project list is saved to `~/.cursor_picker_projects.json` so it persists between launches.

## Troubleshooting

| Problem | Fix |
|---|---|
| "cursor is not recognized" | Make sure Cursor's `cursor` CLI is on your PATH. In Cursor: `Cmd/Ctrl+Shift+P → Install 'cursor' command in PATH` |
| Antivirus blocks the .exe | This is common with PyInstaller — add an exception or run from source with `python cursor_picker.py` |
| Python not found | Re-install Python and tick "Add Python to PATH" |
