# Drakkenheim PDF art extractor

This script will extract the artwork from the PDF that may be interesting for
use in a VTT.

Simply run the script and provide it with a path to the PDF. It will take a while, but once done
you should hopefully have a collection of everything you want in order to make tokens and prepare
screens in your VTT of choice. It should hopefully be useful for you at an actual table as well.

Note that this script is built so that one can easily add parts, sacrificing efficiency to do so.
I'm also an embedded systems engineer, not a python developer, feel free to submit pull requests if
you can improve it while maintaining the simplicity of the image table.

## Requirements

- Linux, BSD or MacOS
- ImageMagick, this is a staple program and exists in any package manager.
- Poppler, this should also exist in any package manager.
- MacOS users may need to install something like Homebrew (https://brew.sh) in order to install the requirements.
