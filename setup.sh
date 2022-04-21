mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
\n\
[theme]
primaryColor = '#a3268c'\n\
backgroundColor = '#631a56'\n\
secondaryBackgroundColor = '#a3268c'\n\
textColor = '#ffffff'\n\
font = 'sans serif'\n\
" > ~/.streamlit/config.toml