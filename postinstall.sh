#/bin/sh
python -c "import nltk;nltk.download('punkt')"
rm /root/nltk_data/tokenizers/punkt.zip

# Install manually to avoid invalid python version warning from pip
git clone --depth 1 https://github.com/xtekky/gpt4free.git
cd gpt4free
pip install -r requirements.txt
mv gpt4free /usr/local/lib/python3.9/site-packages
wget https://github.com/FlorianREGAZ/Python-Tls-Client/raw/master/tls_client/dependencies/tls-client-x86.so  -P /usr/local/lib/python3.9/site-packages/tls_client/dependencies/
wget https://github.com/FlorianREGAZ/Python-Tls-Client/raw/master/tls_client/dependencies/tls-client-arm64.so  -P /usr/local/lib/python3.9/site-packages/tls_client/dependencies/
