#Dont change anything without informing us
if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/Codeflix-Bots/Hokage.git /Hokage
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /Hokage
fi
cd /Hokage
pip3 install -U -r requirements.txt
echo "sᴛᴀʀᴛɪɴɢHokage ʙᴏᴛ...."
python3 bot.py
