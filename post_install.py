# post_install.py
import subprocess
import sys

def install_spacy_model(model_name):
    """Instala um modelo do spaCy."""
    subprocess.check_call([sys.executable, "-m", "spacy", "download", model_name])

if __name__ == "__main__":
    install_spacy_model("pt_core_news_sm")
