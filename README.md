Casino
------

This is supposed to be the core of a Casino program that people can use to gamble (real 
money or fake, does it matter)?  Some of the attributes of the system:

* Multiplayer
* High-performance WebSocket server
* Chat
* Pluggable back-end

Running the Casino
==================

First, you have to set up your environment and run the server:

	cd Sites/Craps
	source bin/activate
	cd www
	source config.env
	python helloTornado.py
	
Next you can go to a Chrome browser and open the console:

	var s = new WebSocket('ws://127.0.0.1:8888/craps/CJ');
	s.onopen = function() { console.log('socket is opened'); }
	s.onclose = function() { console.log('socket is closed'); }
	s.onmessage = function(msg) { console.log(msg.data); }
	s.send('bet.pass 10');
	s.send('roll somestringhere');

