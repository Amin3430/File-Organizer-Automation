# File Organizer Automation With GUI 

A powerful desktop application built with **Python**, **Tkinter GUI**, **JSON**, **OS**, and **Shutil** libraries for automating file organization. This intelligent tool helps users sort and move files into categorized folders (e.g., Documents, Images, Videos, Music, etc.) based on file extensions, eliminating the chaos of cluttered directories.

---
## 🚀 Features  

### Core Functionality
- **Intuitive Tkinter GUI** - Clean, user-friendly interface for easy interaction
- **Smart File Categorization** - Automatically organizes files into predefined categories:
  - 📄 **Documents** (PDF, DOCX, TXT, XLSX, etc.)
  - 🖼️ **Images** (JPG, PNG, GIF, SVG, etc.)
  - 🎵 **Music** (MP3, WAV, FLAC, etc.)
  - 🎬 **Videos** (MP4, AVI, MKV, MOV, etc.)
  - 📦 **Archives** (ZIP, RAR, 7Z, etc.)
  - 💻 **Code** (PY, JS, HTML, CSS, etc.)
  - ⚙️ **Others** (Unrecognized file types)

### Advanced Features
- **JSON Configuration** - Easily customizable extension-to-folder mapping
- **Multiple Input Methods** - Support for:
  - Manual folder path input
  - Browse folder dialog
  - Drag-and-drop functionality (future enhancement)
- **Real-time Progress Display** - Live updates during file organization
- **Safe File Operations** - Uses `shutil` for reliable file moving with error handling
- **Duplicate Handling** - Automatically renames files if duplicates exist
- **Cross-platform Support** - Works seamlessly on Windows, Linux, and macOS
- **Dry Run Mode** - Preview changes before applying them
- **Hidden Files Filter** - Option to ignore hidden files during organization
- **Threaded Processing** - Non-blocking UI during file operations

---

## 🛠️ Tech Stack  

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Tkinter](https://img.shields.io/badge/Tkinter-GUI-orange)](https://docs.python.org/3/library/tkinter.html)
[![JSON](https://img.shields.io/badge/JSON-Data%20Config-lightgrey?logo=json&logoColor=black)](https://www.json.org/json-en.html)
[![OS](https://img.shields.io/badge/OS-File%20Handling-grey)](https://docs.python.org/3/library/os.html)
[![Shutil](https://img.shields.io/badge/Shutil-File%20Operations-lightblue)](https://docs.python.org/3/library/shutil.html)
[![VS Code](https://img.shields.io/badge/VS%20Code-Editor-blueviolet?logo=visualstudiocode&logoColor=white)](https://code.visualstudio.com/)
[![GitHub](https://img.shields.io/badge/GitHub-Repo-black?logo=github&logoColor=white)](https://github.com/)

### Technology Breakdown

**Python 3.10+**  
The core programming language providing robust file handling and system operations. Python's simplicity and extensive standard library make it perfect for automation tasks.

**Tkinter**  
Python's standard GUI library used to create an intuitive desktop interface with buttons, labels, text entries, and progress bars. Tkinter comes pre-installed with Python, requiring no additional dependencies.

**JSON**  
Configuration file format storing the mapping between file extensions and destination folders, making the application highly customizable without code modifications. JSON's human-readable format allows users to easily add or modify file categories.

**OS Library**  
Handles operating system operations like:
- Listing directory contents
- Checking file/folder existence
- Path manipulations (join, split, etc.)
- Creating directories
- Cross-platform path handling

**Shutil Library**  
Provides high-level file operations including:
- Safe file moving with metadata preservation
- Error handling for locked files
- Atomic operations to prevent data loss
- Directory tree operations

**Threading**  
Enables non-blocking UI by running file operations in background threads, keeping the application responsive during long operations.

**Pathlib**  
Modern Python library for elegant path manipulations and file extension handling.

---

## 🔍 How It Works

### Workflow Overview

1. **User Input** - User selects a folder to organize through the GUI browser or manual path entry
2. **File Scanning** - Application scans the directory using `os.listdir()` to get all files
3. **Extension Detection** - Identifies file types based on extensions using `Path().suffix`
4. **Category Mapping** - Matches extensions to categories using JSON config lookup
5. **Folder Creation** - Creates category folders using `os.makedirs()` if they don't exist
6. **Duplicate Check** - Verifies if file already exists in destination and handles conflicts
7. **File Movement** - Moves files to appropriate folders using `shutil.move()`
8. **Progress Feedback** - Updates GUI progress bar and status label in real-time
9. **Completion Report** - Displays detailed summary with statistics and timestamps

### Algorithm Logic

```python
# Simplified algorithm
for each file in selected_directory:
    # Get file extension
    extension = get_file_extension(file)
    
    # Look up category from config
    category = find_category_by_extension(extension)
    
    # Create destination folder if needed
    destination_folder = create_category_folder(category)
    
    # Handle duplicate filenames
    final_destination = handle_duplicate_filename(destination_folder, file)
    
    # Move file safely
    shutil.move(file, final_destination)
    
    # Update progress
    update_ui_progress()
```

### File Extension Mapping Example

The application uses a JSON configuration structure like this:

```json
{
  "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx", ".odt", ".csv"],
  "Images": [".jpg", ".jpeg", ".png", ".gif", ".svg", ".bmp", ".webp"],
  "Videos": [".mp4", ".avi", ".mkv", ".mov", ".flv", ".wmv"],
  "Music": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
  "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
  "Code": [".py", ".js", ".html", ".css", ".java", ".cpp"]
}
```

### Duplicate Handling Strategy

When a file with the same name exists in the destination:
```
Original: document.pdf
Already exists: document.pdf
New name: document_1.pdf

If document_1.pdf also exists:
New name: document_2.pdf

And so on...
```

---

## 📦 Installation

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Tkinter (usually pre-installed with Python)

### Verify Prerequisites

**Check Python version:**
```bash
python --version
# or
python3 --version
```

**Check if Tkinter is installed:**
```bash
python -m tkinter
```
A small window should appear if Tkinter is installed correctly.

### Step-by-Step Setup

1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/file-organizer-automation.git
cd file-organizer-automation
```

2. **Create Virtual Environment (Recommended)**
```bash
# Create virtual environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

3. **Install Dependencies (if any)**
```bash
pip install -r requirements.txt
```
*Note: This project uses only Python standard libraries, so no external packages are required!*

4. **Verify Installation**
```bash
python file_organizer.py
```
The application window should open successfully.

### Alternative Installation Methods

**Download as ZIP:**
1. Download repository as ZIP file
2. Extract to your desired location
3. Navigate to folder in terminal
4. Run `python file_organizer.py`

**Install System-wide (Advanced):**
```bash
pip install .
file-organizer
```

---

## 💻 Usage

### Running the Application

**Method 1: Direct Execution**
```bash
python file_organizer.py
```

**Method 2: From IDE**
- Open `file_organizer.py` in your favorite IDE (VS Code, PyCharm, etc.)
- Run the file directly

**Method 3: Create Executable (Optional)**
```bash
pip install pyinstaller
pyinstaller --onefile --windowed file_organizer.py
```

### Using the GUI Interface

#### Step-by-Step Guide

1. **Launch Application**
   - Run the Python script
   - Main window will appear

2. **Select Folder**
   - Click "Browse" button to open folder picker
   - Or manually type/paste folder path
   - Selected path appears in text field

3. **Configure Options**
   - ☑️ **Ignore hidden files** - Skip files starting with dot (.)
   - ☑️ **Dry run** - Preview changes without actually moving files

4. **Start Organization**
   - Click "🚀 Organize Files" button
   - Watch progress bar and status updates
   - View detailed results in text area

5. **Review Results**
   - Check completion summary
   - Verify files in organized folders
   - Review any errors or warnings

### Example Usage Scenarios

#### Scenario 1: Cleaning Downloads Folder

**Before Organization:**
```
Downloads/
├── vacation_photo.jpg
├── meeting_notes.pdf
├── favorite_song.mp3
├── tutorial_video.mp4
├── project.zip
├── script.py
├── installer.exe
└── data.csv
```

**After Organization:**
```
Downloads/
├── Images/
│   └── vacation_photo.jpg
├── Documents/
│   ├── meeting_notes.pdf
│   └── data.csv
├── Music/
│   └── favorite_song.mp3
├── Videos/
│   └── tutorial_video.mp4
├── Archives/
│   └── project.zip
├── Code/
│   └── script.py
└── Executables/
    └── installer.exe
```

### File Descriptions

**file_organizer.py**  
Main application containing:
- GUI layout and components
- File organization logic
- Configuration loading
- Threading implementation
- Error handling

**config.json**  
JSON configuration file defining:
- File categories
- Extension mappings
- Auto-generated on first run
- User-customizable

**requirements.txt**  
Python dependencies (currently empty as project uses only standard libraries)

**README.md**  
Comprehensive documentation including:
- Installation instructions
- Usage guidelines
- Configuration details
- Examples and screenshots
---
**Made with ❤️ and Python**

*Last Updated: October 2025*