
* Run
On a system with nix flakes enabled
``` console
nix run github:raubjo/contribution-report-generator
``` 
Without nix flakes enabled
``` console
nix run --experimental-features 'nix-command flakes' github:raubjo/contribution-report-generator
```
Or
clone the repo and run main.py from cli

Calling wkhtmltopdf from pdfkit doesn't allow wkhtmltopdf to get the logo.png or other image files. To work around this I base64 encoded them and pasted the result into the template.html file.
