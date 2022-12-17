{ mkShell
, jdk8
, python39
, pkgs
, ...
}:

let
  # CHANGEME define the list of Python packages to pull from nixpkgs
  python-env = python39.withPackages (pp: with pp; [
    virtualenv
    pip
    pdfkit
    tkinter
  ]);
in
mkShell {
  # CHANGEME add other requirements
  buildInputs = [
    pkgs.wkhtmltopdf
    pkgs.puppeteer-cli
  ]
    # injects the Python base
    ++ [ python-env ];

  NIX_PYTHONPATH = "${python-env}/${python-env.sitePackages}";

  shellHook = ''
    if [[ ! -d .venv ]]; then
      echo "No virtual env found at ./.venv, creating a new virtual env linked to the Python site defined with Nix"
      ${python-env}/bin/python -m venv .venv
      cp ${builtins.toString ./sitecustomize.py} .venv/lib/python*/site-packages/
    fi
    source .venv/bin/activate
    pip install -r requirements.txt
    echo "Nix development shell loaded."
  '';
}
