{
  description = "Flake environment for Eigen challenge";
  inputs.std.url = "github:divnix/std";
  inputs.std.inputs.nixpkgs.follows = "nixpkgs";
  #inputs.nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
  inputs.nixpkgs.url = "github:nixos/nixpkgs";

  inputs.poetry2nix = {
    url = "github:nix-community/poetry2nix";
    inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs = {
    std,
    self,
    ...
  } @ inputs:
    std.growOn {
      inherit inputs;
      cellsFrom = ./comb;
      # debug = ["cells" "x86_64-linux"];
      cellBlocks = with std.blockTypes; [
        # devshells can be entered
        (devshells "devshells")
      ];
      nixpkgsConfig = {
        allowUnfree = true;
      };
    }
    # soil
    {
      devShells = std.harvest self ["_QUEEN" "devshells"];
      # overlay = inputs.nixpkgs.lib.composeManyExtensions [
      #   inputs.poetry2nix.overlay
      #   (final: prev: {
      #     # The application
      #     myapp = prev.poetry2nix.mkPoetryApplication {
      #       projectDir = ./.;
      #     };
      #   })
      # ];
      packages.x86_64-linux = {
        eigen = inputs.poetry2nix.legacyPackages.x86_64-linux.mkPoetryApplication { projectDir = self; };
        default = self.packages.x86_64-linux.eigen;
      };
    };

}
