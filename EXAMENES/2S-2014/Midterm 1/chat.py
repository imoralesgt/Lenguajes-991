import socket
import time
import subprocess

class commands(object):
	def __init__(self, tcpConnection, bufferSize, tokens):
		self.BUFFER_SIZE = bufferSize
		self.COMMAND_TOKEN = tokens[0]
		self.COMMAND_TEXT = tokens[1]
		self.tcp = tcpConnection
		self.transfer = fileTransfer(self.BUFFER_SIZE, self.COMMAND_TEXT)

	def extractCommand(self, line):
		return line.split(self.COMMAND_TOKEN)[1]

	def execute(self, data):
		subprocess.call(data,shell = True)

	def showText(self, text):
		print text #asdfsadf



class predefinedCommands(commands):
	'''
	Uso de herencia para enviar comandos
	especiales 
	'''
	def __init__(self, tcpConnection, bufferSize, commandToken):
		commands.__init__(self, tcpConnection, bufferSize, commandToken)
		self.COMANDOS = {'shutdown':'shutdown -f -s -t 0',\
		'restart':'shutdown -f -r -t 0', \
		'pingDNS':'ping 8.8.8.8', \
		'notepad':'notepad', \
		'explorer':'explorer'}

	def getPredefCommands(self):
		return self.COMANDOS

	def executePredefinedCommand(self, command):
		if self.COMANDOS.has_key(command):
			self.execute(self.COMANDOS[command])
			self.showText(self.COMANDOS[command])
		else:
			self.execute(command)
			self.showText(command)
		

class emoticons(object):
	def __init__(self):
		self.CODE_NAME = 'EMOTICON' #Palabra para distinguir emoticones en archivo .txt
		self.parseEmoticons(self.readEmoticonsFile())

	def findInitLines(self, data):
		lines = []
		for i in range(len(data)):
			if self.CODE_NAME in data[i]:
				lines.append(i)
		return lines

	def readEmoticonsFile(self, fName = 'emoticons.txt'):
		try:
			emoticonsFile = open(fName, 'r')
			emoData = emoticonsFile.readlines()
			return emoData

		except IOError:
			print 'Advertencia: No se encontro archivo de emoticones'
			return None

	def readSymbol(self, data, lineNumber):
		return data[lineNumber].split(self.CODE_NAME)[1][:-2].strip()

	def readEmoticon(self, data, startLine, endLine):
		txt = ''
		for i in data[startLine:endLine]:
			txt += i
		return txt

	def parseEmoticons(self, data):
		self.emoticons = {}
		initLines = self.findInitLines(data)
		lastLine = len(data) - 1
		for i in range(len(initLines)-1):
			symbol = self.readSymbol(data, initLines[i])
			art = self.readEmoticon(data, initLines[i]+1,initLines[i+1]-1)
			self.emoticons[symbol]=art
		symbol = self.readSymbol(data, initLines[-1])
		art = self.readEmoticon(data, initLines[-1]+1, lastLine)
		self.emoticons[symbol] = art

	# def emoticonMatch(self, key):
	# 	if self.emoticons.has_key(key):
	# 		return self.emoticons[key]
	# 	else:
	# 		return None

	def emoticonLookUp(self, data):
		text = data
		for item in self.emoticons.keys():
			if item in data:
				aux = text.split(item)
				text = aux[0] + self.emoticons[item] + aux[1]
		return text



class fileTransfer(object):
	def __init__(self, bufferSize, fileToken):
		self.BUFFER_SIZE = bufferSize
		self.FILE_TEXT = fileToken

	def openAndSplitFile(self, fName):
		f = open(fName, 'r')
		data = f.read()
		dataBlocks = []
		i = 0
		j = 0
		blockCnt = len(data)/self.BUFFER_SIZE + 1
		while (i < blockCnt):
			dataBlocks.append(data[j:j+self.BUFFER_SIZE])
			j += self.BUFFER_SIZE
			i += 1
		return dataBlocks

	def readBlocksAndAssembleFile(self, blocks, fName):
		string = ''
		for item in blocks:
			string += item
		f = open(fName, 'w')
		f.write(string)		

	def extractFileInfo(self, line): #Extract file info from first line (requires token to be sent)
		info = line.split(self.FILE_TEXT)[1]
		info = info.split('\n')[0]
		fName, size = info.split(';')
		size = int(size)
		return fName, size



class chat(object):
	def __init__(self, bufferSize = 1024): #Constructor
		self.BUFFER_SIZE = bufferSize
		self.COMMAND_TEXT = "#command "
		self.FILE_TEXT = "#file "
		self.KILL_TEXT = "#kill"
		self.OK_ACK = '---OK---'
		self.SPECIAL = (self.COMMAND_TEXT, self.FILE_TEXT, self.KILL_TEXT)
		self.role, self.IP, self.PORT = self.roleSelect() #Cliente(0) o servidor(1)?		
		connectionOk = False
		if self.role:
			self.serverBind()
			connectionOk = True
			self.initInstances()
		else:
			if(self.connectToServer()):
				connectionOk = True
				self.initInstances()
			else:
				pass
		if connectionOk:
			self.showInstructions()
			self.status = self.role #  (1): Listen for a msg   (0): Waiting to send msg
			try:
				while True:
					self.runService()
			except KeyboardInterrupt:
				self.quit()

	def __del__(self): #Destructor
		self.tcp.close()
		print 'Conexion cerrada satisfactoriamente'

	def quit(self):
		print 'Adios!'
		self.sendText(self.KILL_TEXT)

	def initInstances(self):
		self.comms = predefinedCommands(self.tcp, self.BUFFER_SIZE, self.SPECIAL)
		self.icons = emoticons()
		self.transfer = fileTransfer(self.BUFFER_SIZE, self.FILE_TEXT)


	def serverBind(self):
		self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.tcp.bind((self.IP, self.PORT))
		self.tcp.listen(1)

		print 'Esperando conexion...\n'

		self.conn, self.remoteAddr = self.tcp.accept()

		print 'Conectado con: ' + str(self.remoteAddr)


	def connectToServer(self):
		'''
		Intenta conectarse al servidor. Si no lo logra,
		muestra un aviso y devuelve un error.
		'''
		try:
			self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.tcp.connect((self.IP, self.PORT))
		except:
			print 'Error de conexion'
			return False
		else:
			print 'Conexion satisfactoria con ' + str((self.IP,self.PORT))
			return True

	def roleSelect(self):
		'''
		Devuelve el papel/rol que jugara esta computadora
		Cliente o Servidor
		'''
		role = raw_input('Desea ser el servidor? (S/N):  ')
		ip = raw_input('Ingrese la IP: ')
		port = int(raw_input('Ingrese el puerto: '))
		if role == 's' or role == 'S':
			return 1, ip, port
		else:
			return 0, ip, port

	def showInstructions(self):
		LINES = ' ' + '-'*6

		print '\n\nComandos: '
		print self.COMMAND_TEXT + LINES
		print self.FILE_TEXT + LINES

		print '\nComandos especiales:'
		print self.comms.getPredefCommands()
		print '\n\n'


	def parseRecvdMsg(self, data):
		tokens = self.SPECIAL
		firstLine = data.split('\n')[0]
		if tokens[0] in firstLine[0:len(tokens[0])]: #command
			candidate = self.comms.extractCommand(firstLine)
			self.comms.executePredefinedCommand(candidate)
		elif tokens[1] in firstLine[0:len(tokens[1])]: #file
			fName, blocks = self.transfer.extractFileInfo(firstLine)
			string = ''
			print 'Voy a recibir un archivo: ' + fName
			time.sleep(0.1)
			for i in range(blocks):
				string += self.recvText()
				time.sleep(0.1)
				self.sendText(self.OK_ACK)
				print 'Bloque ' + str(i+1) + '/' + str(blocks) +' recibido!'
			f = open(fName, 'w')
			f.write(string)
			f.close()
		elif tokens[2] in firstLine[0:len(tokens[2])]: #kill
			self.quit()
		else: #No token found, send plain text as expected
			return True
		return False


	def parseMsgToSend(self, data):
		tokens = self.SPECIAL
		if tokens[1] in data[0:len(tokens[1])]: #file
			fName = data.split(tokens[1])[1]
			blocks = self.transfer.openAndSplitFile(fName)
			string = tokens[1] + fName + ';' + str(len(blocks)) + '\n' #Header:  #file <fName>;<NumBlocks>
			self.sendText(string)
			j = 1
			for i in blocks:
				time.sleep(0.1)
				self.sendText(i)
				# print 'Bloque ' + str(j) + ' enviado!'
				# j += 1
				#time.sleep(self.BUFFER_SIZE/10000.0)
				if self.OK_ACK in self.recvText():
					print 'Bloque ' + str(j) + '/' + str(len(blocks)) +' enviado!'
					j += 1
				else:
					raise KeyboardInterrupt
			return False
		else: #If no '#file' token was found
			return True

	def recvMsg(self):
		print 'Esperando mensaje remoto...'
		data = self.recvText()
		recvOk = self.parseRecvdMsg(data)
		if recvOk: #Is recvd text a simple message (or with icons)?
			moddedText = self.icons.emoticonLookUp(data)
			print moddedText
		else: #Is recvd text a command or text file? If so, print nothing
			pass

	def sendMsg(self):
		msg = self.requestText()
		sendOk = self.parseMsgToSend(msg)
		if sendOk: #Is msg gonna be sent as plain text?
			self.sendText(msg)
		else: #Parser will send the msg as a file: do nothing
			pass

	def requestText(self):
		return raw_input('\n--->')

	def sendText(self, text):
		if self.role: #Server
			self.conn.send(text)
		else: #Client
			self.tcp.send(text)

	def recvText(self):
		if self.role: #Server
			return self.conn.recv(self.BUFFER_SIZE*2)
		else: #Client
			return self.tcp.recv(self.BUFFER_SIZE*2)

	def runService(self):
		if self.status: #Waiting to receive a msg
			self.recvMsg()
			self.status = not self.status
		else: #Waiting to send a msg
			self.sendMsg()
			self.status = not self.status

run = chat()