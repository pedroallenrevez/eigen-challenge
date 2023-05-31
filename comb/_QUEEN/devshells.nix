let
  l = nixpkgs.lib // builtins;

  inherit (inputs) nixpkgs;
  inherit (inputs.std) std lib;
  inherit (cell) nixago;

  withCategory = category: attrset: attrset // {inherit category;};

  python = "python310";
in
  l.mapAttrs (_: lib.dev.mkShell) {
    default = {...}: {
      name = "EigenNLP";
      nixago = [
        # off-the-shelve from `std`
        (lib.cfg.conform {data = {inherit (inputs) cells;};})
        lib.cfg.lefthook
        # modified from the local Cell
        std.nixago.treefmt
        std.nixago.editorconfig
      ];
      imports = [];
      packages = with nixpkgs; [
        zlib # needed by spacy
        poetry
      ];
      env = [
        {
          name = "LD_LIBRARY_PATH";
          #value = ''${nixpkgs.stdenv.cc.cc.lib}/lib/'';
          # Link to libstc++ libraries, and zlib libraries
          value = ''${nixpkgs.stdenv.cc.cc.lib}/lib/:${nixpkgs.zlib}/lib/:$LD_LIBRARY_PATH'';
        }
      ];
      commands = [
        (withCategory "hexagon" {
          name = "clean-pycache";
          help = "Clean all pyacache pyc and pyo";
          command = ''
            find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf
          '';
        })
      ];
    };
  }
