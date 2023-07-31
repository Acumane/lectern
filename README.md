<div align="center"> 

# :open_book: **Lectern**

<center>Listen to PDFs with natural TTS and read-along text prompts</center>

### Motivation

Microsoft Edge's built-in "Read Aloud" feature is second to none but was inexplicably pulled from Linux builds in 2022. Lectern lets me listen to PDFs with Microsoft's natural voice engine independent from the browser.

</div>
	
### Features
- Convert a range of PDF pages to quality speech
- Configuration file for changing voice, speed, and other settings
- Cuts out (most) headers, footers, captions, titles, and other text fragments
- Concurrent page processing
- Saves pages as `.mp3`s
- Prints words as they're spoken (includes punctuation)
- Pause, resume, skip pages, and quit
- Bionic reading 

> :warning: **Disclaimer**
This program is minimally viable as of `0.2.0`, though a few bugs persist as minor annoyances. Check [issues](https://github.com/Acumane/lectern/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc+label%3Abug) to avoid or work around them.


### Installation
```
cd <~/somewhere/convenient>
git clone https://github.com/Acumane/lectern
cd lectern

# install dependencies
pip install -r requirements.txt
```
Done!

### Quickstart
```
python main.py <path/to/pdf> <first>-<last pg #>
```
- Use page #s given by a PDF reader to inform your range
- A single page is also valid.

**Configuration**
- A template config is provided in [`lec.conf`](https://github.com/Acumane/lectern/blob/main/lec.conf). For a list of available voices, run `edge-tts --list-voices`
