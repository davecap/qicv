OUTPUT = ./static/css/style.css
OUTPUT_MIN = ./static/css/style.min.css
#OUTPUT_RESPONSIVE = ./static/css/style-responsive.css
#OUTPUT_RESPONSIVE_MIN = ./static/css/style-responsive.min.css

BOOTSTRAP_LESS = ./static/less/bootstrap.less
#BOOTSTRAP_RESPONSIVE_LESS = ./static/less/responsive.less
LESS_COMPRESSOR ?= `which lessc`
WATCHR ?= `which watchr`

all:
	lessc ${BOOTSTRAP_LESS} > ${OUTPUT}
	lessc --compress ${BOOTSTRAP_LESS} > ${OUTPUT_MIN}
	#lessc ${BOOTSTRAP_RESPONSIVE_LESS} > ${OUTPUT_RESPONSIVE}
	#lessc --compress ${BOOTSTRAP_RESPONSIVE_LESS} > ${OUTPUT_RESPONSIVE_MIN}
	# uglifyjs -nc bootstrap/js/bootstrap.js > bootstrap/js/bootstrap.min.js

watch:
	echo "Watching less files..."; \
	watchr -e "watch('static/less/.*\.less') { system 'make' }"


.PHONY: watch all
