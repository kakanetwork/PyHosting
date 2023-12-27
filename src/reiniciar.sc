
#!/bin/bash
echo -n "----- Rodou : " >>/projetoasa/src/LogRestart 

date >>/projetoasa/src/LogRestart
rndc reload >>/projetoasa/src/LogRestart
apachectl restart >>/projetoasa/src/LogRestart
service named restart >>/projetoasa/src/LogRestart
