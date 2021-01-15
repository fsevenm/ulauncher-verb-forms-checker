# Ulauncher Verb Forms Checker

> Forming conjugations made easy.

## Screenshots
![media1](preview.gif)

## Requirements
Technical:
* [ulauncher](https://ulauncher.io/)
* Python >= 2.7

Other:
* [Linguatools Conjugations' Rapid API](https://rapidapi.com/petapro/api/linguatools-conjugations)

## Install

Open ulauncher preferences window -> extensions -> add extension and paste the following url:

```https://github.com/fsevenm/ulauncher-verb-forms-checker```
 

## Development

```shell script
git clone https://github.com/fsevenm/ulauncher-wordc
ln -s <clone_location> ~/.local/share/ulauncher/extensions/ulauncher-verb-forms-checker
```

To start debugging the extension, run these debugging script:
```shell script
# run in different Terminal tab
ulauncher --no-extensions --dev -v
# run in different Terminal tab, you need to change PYTHONPATH value based on your local python config, change the USERNAME to yours
VERBOSE=1 ULAUNCHER_WS_API=ws://127.0.0.1:5054/ulauncher-verb-forms-checker PYTHONPATH=/usr/lib/python3/dist-packages /usr/bin/python3 /home/USERNAME/.local/share/ulauncher/extensions/ulauncher-verb-forms-checker/main.py
```

When you made any changes to `main.py` or the other assets, you need to re-run debugging scripts above.

## License 

MIT @ Ayub Aswad