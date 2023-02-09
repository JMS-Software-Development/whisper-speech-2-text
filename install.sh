# Install Stable Diffusion
git submodule update --init --recursive
cp webui-user.sh stable-diffusion-webui/webui-user.sh
cd stable-diffusion-webui
./webui.sh

# install additional dependencies
cd ..
source ./venv/bin/activate
pip install diffusers

# install whisper (zorg dat venv actief is)
cd backend
pip install -r requirements.txt



# TAR MAKEN EN UPLOADEN
# tar -czvf project.tar.gz . #maak tar
# scp -r project.tar.gz usergpu@185.4.148.142:~/ 
# tar -xvf project.tar.gz #uitpakken

