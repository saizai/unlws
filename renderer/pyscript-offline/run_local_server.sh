if [ -x "$(command -v py)" ]; then
  py -m http.server -d ./public/
elif [ -x "$(command -v python3)" ]; then
  python3 -m http.server -d ./public/
elif [ -x "$(command -v python)" ]; then
  python -m http.server -d ./public/
else
  echo "install python or python3"
fi

