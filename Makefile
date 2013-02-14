.PHONY: doc upload-doc

help:
	@echo "doc        Compile documentation in HTML"
	@echo "upload-doc Compile and upload documentation to github"

doc:
	make -C doc clean
	make -C doc html

upload-doc: doc
	@echo "Upload documentation on github"
	@ghp-import -p -m "Update documentation" doc/build/html/

