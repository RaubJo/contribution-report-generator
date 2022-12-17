
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
