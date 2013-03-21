all: man pipe ssh trailer

man:
	zip -j9 --filesync man.alfredworkflow  net.isometry.alfred.man/*.{plist,png,py}

pipe:
	zip -j9 --filesync pipe.alfredworkflow net.isometry.alfred.pipe/*.{plist,png,py}

ssh:
	zip -j9 --filesync ssh.alfredworkflow  net.isometry.alfred.ssh/*.{plist,png,py}

trailer:
	zip -j9 --filesync trailer.alfredworkflow  net.isometry.alfred.trailer/*.{egg,plist,png,py}

