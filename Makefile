all:
	zip -j9 --filesync man.alfredworkflow  net.isometry.alfred.man/*.{plist,png,py}
	zip -j9 --filesync pipe.alfredworkflow net.isometry.alfred.pipe/*.{plist,png}
	zip -j9 --filesync ssh.alfredworkflow  net.isometry.alfred.ssh/*.{plist,png,py}
