import os
import json
import urllib.request
import zipfile
import shutil
from pathlib import Path

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent
OUTPUT_FOLDER_PARENT = PROJECT_ROOT / "app" / "src" / "main" / "assets"
OUTPUT_FOLDER = OUTPUT_FOLDER_PARENT / "embedded"
JNI_LIBS_FOLDER = PROJECT_ROOT / "app" / "src" / "main" / "jniLibs"

DEPS = [
    {
        "file": "katex.min.css",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.16.19/dist/katex.min.css",
    },
    {
        "file": "katex.min.js",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.16.19/dist/katex.min.js",
    },
    {
        "file": "fonts/KaTeX_AMS-Regular.ttf",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_AMS-Regular.ttf",
    },
    {
        "file": "fonts/KaTeX_AMS-Regular.woff",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_AMS-Regular.woff",
    },
    {
        "file": "fonts/KaTeX_AMS-Regular.woff2",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_AMS-Regular.woff2",
    },
    {
        "file": "fonts/KaTeX_Caligraphic-Bold.ttf",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_Caligraphic-Bold.ttf",
    },
    {
        "file": "fonts/KaTeX_Caligraphic-Bold.woff",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_Caligraphic-Bold.woff",
    },
    {
        "file": "fonts/KaTeX_Caligraphic-Bold.woff2",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_Caligraphic-Bold.woff2",
    },
    {
        "file": "fonts/KaTeX_Caligraphic-Regular.ttf",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_Caligraphic-Regular.ttf",
    },
    {
        "file": "fonts/KaTeX_Caligraphic-Regular.woff",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_Caligraphic-Regular.woff",
    },
    {
        "file": "fonts/KaTeX_Caligraphic-Regular.woff2",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_Caligraphic-Regular.woff2",
    },
    {
        "file": "fonts/KaTeX_Fraktur-Bold.ttf",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_Fraktur-Bold.ttf",
    },
    {
        "file": "fonts/KaTeX_Fraktur-Bold.woff",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_Fraktur-Bold.woff",
    },
    {
        "file": "fonts/KaTeX_Fraktur-Bold.woff2",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_Fraktur-Bold.woff2",
    },
    {
        "file": "fonts/KaTeX_Fraktur-Regular.ttf",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_Fraktur-Regular.ttf",
    },
    {
        "file": "fonts/KaTeX_Fraktur-Regular.woff",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_Fraktur-Regular.woff",
    },
    {
        "file": "fonts/KaTeX_Fraktur-Regular.woff2",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_Fraktur-Regular.woff2",
    },
    {
        "file": "fonts/KaTeX_Main-Bold.ttf",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_Main-Bold.ttf",
    },
    {
        "file": "fonts/KaTeX_Main-Bold.woff",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_Main-Bold.woff",
    },
    {
        "file": "fonts/KaTeX_Main-Bold.woff2",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_Main-Bold.woff2",
    },
    {
        "file": "fonts/KaTeX_Main-BoldItalic.ttf",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_Main-BoldItalic.ttf",
    },
    {
        "file": "fonts/KaTeX_Main-BoldItalic.woff",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_Main-BoldItalic.woff",
    },
    {
        "file": "fonts/KaTeX_Main-BoldItalic.woff2",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_Main-BoldItalic.woff2",
    },
    {
        "file": "fonts/KaTeX_Main-Italic.ttf",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_Main-Italic.ttf",
    },
    {
        "file": "fonts/KaTeX_Main-Italic.woff",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_Main-Italic.woff",
    },
    {
        "file": "fonts/KaTeX_Main-Italic.woff2",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_Main-Italic.woff2",
    },
    {
        "file": "fonts/KaTeX_Main-Regular.ttf",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_Main-Regular.ttf",
    },
    {
        "file": "fonts/KaTeX_Main-Regular.woff",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_Main-Regular.woff",
    },
    {
        "file": "fonts/KaTeX_Main-Regular.woff2",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_Main-Regular.woff2",
    },
    {
        "file": "fonts/KaTeX_Math-BoldItalic.ttf",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_Math-BoldItalic.ttf",
    },
    {
        "file": "fonts/KaTeX_Math-BoldItalic.woff",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_Math-BoldItalic.woff",
    },
    {
        "file": "fonts/KaTeX_Math-BoldItalic.woff2",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_Math-BoldItalic.woff2",
    },
    {
        "file": "fonts/KaTeX_Math-Italic.ttf",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_Math-Italic.ttf",
    },
    {
        "file": "fonts/KaTeX_Math-Italic.woff",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_Math-Italic.woff",
    },
    {
        "file": "fonts/KaTeX_Math-Italic.woff2",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_Math-Italic.woff2",
    },
    {
        "file": "fonts/KaTeX_SansSerif-Bold.ttf",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_SansSerif-Bold.ttf",
    },
    {
        "file": "fonts/KaTeX_SansSerif-Bold.woff",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_SansSerif-Bold.woff",
    },
    {
        "file": "fonts/KaTeX_SansSerif-Bold.woff2",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_SansSerif-Bold.woff2",
    },
    {
        "file": "fonts/KaTeX_SansSerif-Italic.ttf",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_SansSerif-Italic.ttf",
    },
    {
        "file": "fonts/KaTeX_SansSerif-Italic.woff",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_SansSerif-Italic.woff",
    },
    {
        "file": "fonts/KaTeX_SansSerif-Italic.woff2",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_SansSerif-Italic.woff2",
    },
    {
        "file": "fonts/KaTeX_SansSerif-Regular.ttf",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_SansSerif-Regular.ttf",
    },
    {
        "file": "fonts/KaTeX_SansSerif-Regular.woff",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_SansSerif-Regular.woff",
    },
    {
        "file": "fonts/KaTeX_SansSerif-Regular.woff2",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_SansSerif-Regular.woff2",
    },
    {
        "file": "fonts/KaTeX_Script-Regular.ttf",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_Script-Regular.ttf",
    },
    {
        "file": "fonts/KaTeX_Script-Regular.woff",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_Script-Regular.woff",
    },
    {
        "file": "fonts/KaTeX_Script-Regular.woff2",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_Script-Regular.woff2",
    },
    {
        "file": "fonts/KaTeX_Size1-Regular.ttf",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_Size1-Regular.ttf",
    },
    {
        "file": "fonts/KaTeX_Size1-Regular.woff",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_Size1-Regular.woff",
    },
    {
        "file": "fonts/KaTeX_Size1-Regular.woff2",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_Size1-Regular.woff2",
    },
    {
        "file": "fonts/KaTeX_Size2-Regular.ttf",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_Size2-Regular.ttf",
    },
    {
        "file": "fonts/KaTeX_Size2-Regular.woff",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_Size2-Regular.woff",
    },
    {
        "file": "fonts/KaTeX_Size2-Regular.woff2",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_Size2-Regular.woff2",
    },
    {
        "file": "fonts/KaTeX_Size3-Regular.ttf",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_Size3-Regular.ttf",
    },
    {
        "file": "fonts/KaTeX_Size3-Regular.woff",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_Size3-Regular.woff",
    },
    {
        "file": "fonts/KaTeX_Size3-Regular.woff2",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_Size3-Regular.woff2",
    },
    {
        "file": "fonts/KaTeX_Size4-Regular.ttf",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_Size4-Regular.ttf",
    },
    {
        "file": "fonts/KaTeX_Size4-Regular.woff",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_Size4-Regular.woff",
    },
    {
        "file": "fonts/KaTeX_Size4-Regular.woff2",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_Size4-Regular.woff2",
    },
    {
        "file": "fonts/KaTeX_Typewriter-Regular.ttf",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_Typewriter-Regular.ttf",
    },
    {
        "file": "fonts/KaTeX_Typewriter-Regular.woff",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_Typewriter-Regular.woff",
    },
    {
        "file": "fonts/KaTeX_Typewriter-Regular.woff2",
        "url": "https://cdn.jsdelivr.net/npm/katex@0.11.1/dist/fonts/KaTeX_Typewriter-Regular.woff2",
    },
    {
        "file": "micromark.bundle.js",
        "url": "https://esm.sh/v135/micromark@3.2.0/es2022/micromark.bundle.mjs",
    },
    {
        "file": "micromark-gfm.bundle.js",
        "url": "https://esm.sh/v135/micromark-extension-gfm@3.0.0/es2022/micromark-extension-gfm.bundle.mjs",
    }
]

def download_file(url, dest_path):
    print(f"Downloading {url} to {dest_path}")
    try:
        with urllib.request.urlopen(url) as response, open(dest_path, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
    except Exception as e:
        print(f"Failed to download {url}: {e}")

def main():
    # Ensure output folder exists
    if OUTPUT_FOLDER.exists():
        shutil.rmtree(OUTPUT_FOLDER)
    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
    (OUTPUT_FOLDER / "fonts").mkdir(exist_ok=True)

    # Download assets
    for dep in DEPS:
        dest_path = OUTPUT_FOLDER / dep["file"]
        download_file(dep["url"], dest_path)

    # Download jniLibs
    libs_query = "https://git.revolt.chat/api/v1/repos/android/final-markdown/releases/latest"
    print(f"Querying {libs_query}")
    try:
        with urllib.request.urlopen(libs_query) as response:
            data = json.loads(response.read().decode())
            zip_url = next((asset["browser_download_url"] for asset in data["assets"] if asset["name"] == "jniLibs.zip"), None)
            
            if zip_url:
                zip_path = PROJECT_ROOT / "jniLibs.zip"
                download_file(zip_url, zip_path)
                
                print(f"Extracting {zip_path} to {JNI_LIBS_FOLDER}")
                JNI_LIBS_FOLDER.mkdir(parents=True, exist_ok=True)
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(JNI_LIBS_FOLDER)
                
                os.remove(zip_path)
            else:
                print("jniLibs.zip not found in release assets")
    except Exception as e:
        print(f"Failed to download jniLibs: {e}")

if __name__ == "__main__":
    main()
