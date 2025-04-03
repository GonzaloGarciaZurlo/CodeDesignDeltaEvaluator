""" script to install goplantuml """
import subprocess


def install_goplantuml():
    """
    Install goplantuml if not already installed.
    """
    try:
        # Check if goplantuml is already installed
        subprocess.run(["goplantuml", "-h"],
                       check=True,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
        print("✅ goplantuml is already installed.")
    except FileNotFoundError:
        try:
            # check if go is installed
            subprocess.run(["go", "version"],
                           check=True,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
        except FileNotFoundError:
            print("🚀 Installing go...")
            subprocess.run([
                "wget",
                "https://git.io/go-installer.sh && bash go-installer.sh"
            ],
                           check=True)
            print("✅ go installed successfully.")
        print("🚀 Installing goplantuml...")
        subprocess.run([
            "go", "install",
            "github.com/jfeliu007/goplantuml/cmd/goplantuml@latest"
        ],
                       check=True)
        print("✅ goplantuml installed successfully.")


if __name__ == "__main__":
    install_goplantuml()
