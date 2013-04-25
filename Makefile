all: man pipe ssh terminology trailer

man:
	zip -j9 --filesync man.alfredworkflow  net.isometry.alfred.man/*.{plist,png,py}

pipe:
	zip -j9 --filesync pipe.alfredworkflow net.isometry.alfred.pipe/*.{json,plist,png,py}

ssh:
	zip -j9 --filesync ssh.alfredworkflow  net.isometry.alfred.ssh/*.{plist,png,py}

terminology:
	zip -j9 --filesync terminology.alfredworkflow  net.isometry.alfred.terminology/*.{plist,png,py}

trailer:
	zip -j9 --filesync trailer.alfredworkflow  net.isometry.alfred.trailer/*.{egg,plist,png,py}

