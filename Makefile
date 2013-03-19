all: man pipe ssh

man:
	zip -j9 --filesync man.alfredworkflow  net.isometry.alfred.man/*.{plist,png,py}

pipe:
	zip -j9 --filesync pipe.alfredworkflow net.isometry.alfred.pipe/*.{plist,png}

ssh:
	zip -j9 --filesync ssh.alfredworkflow  net.isometry.alfred.ssh/*.{plist,png,py}

