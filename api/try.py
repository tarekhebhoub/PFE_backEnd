import requests
import time

headers={"Authorization":"Token a27847b2200e8a7a58cb5ff69a8029e4f9e95acb"}

pos=[{"latitude":36.712808216933084,"longitude":3.184351686111056},{"latitude":36.712873729061315, "longitude":3.182441333883301},
	{"latitude":36.71341468163747,  "longitude":3.182441333883301},{"latitude":36.71383925344438, "longitude":3.182397885731398},
	{"latitude":36.714180566571436, "longitude":3.1824404631504795},{"latitude":36.71446726842012,  "longitude":3.18208281287966},
	{"latitude":36.71455600926507, "longitude": 3.1820232044841807},{"latitude":36.71429661270007, "longitude": 3.181256811046709},
	{"latitude":36.714105477828575,  "longitude":3.1808991607758887},{"latitude":36.71397577889288,"longitude": 3.180030581507503 }
]
i=0
while True:
	data=pos[i]
	i+=1
	if i>=len(pos):
		i=0
	r = requests.put('http://localhost:8000/pos_user/',hedata=data)
	time.sleep(2)


