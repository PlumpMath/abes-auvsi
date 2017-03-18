sudo docker run -it auvsisuas/interop-client

#In container
sudo apt-get install git
# Input : Y
git clone https://github.com/phoenix1796/abes-auvsi.git

cd abes-auvsi

python gst.py --url http://172.17.0.1:8000 --username testuser --password testpass --spoofTelem True

# Open Browser and goto : http://127.0.0.1:8000
# Login with 'testadmin' 'testpass'
# In top right corner goto : System > Edit Data
# Click on +Add in front of Mission clock events
# and add the Team on Clock event for testuser
#Click blue save button in right


# Goto to System > Edit Data
# Click on +Add in front of Takeoff or landing events
# and add the Uas in air event for testuser
#Click blue save button in right

# goto http://127.0.0.1:8000 and select mission 1 and then see

# Created by Abhishek Chopra

