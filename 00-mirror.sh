# eg DOMAIN=https://www.instantdb.com/docs
DOMAIN="${1}"
wget --mirror --convert-links --adjust-extension --page-requisites --no-parent --include-directories=/docs "${DOMAIN}"