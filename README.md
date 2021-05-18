# CAP-Levage

## infos QR code

librairie de base utilisé : https://github.com/mebjas/html5-qrcode/releases en V1.2.3

des modifs ont été faites, encadrées par les commentaires E-cosi dans les fichiers de base :
html5-qrcode.js
qrcode.js

Pour minimifier ces fichier, utiliser babel babel-minify et faire :
1) babel src/html5-qrcode.js -d transpiled
2) minify transpiled/html5-qrcode.js --out-file minified/html5-qrcode.min.js
3) minify transpiled/qrcode.js --out-file minified/qrcode.min.js
