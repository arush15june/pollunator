cd docs/pollunator/
echo "[+] Building Optimized Build"
npm run build

echo "[+] Copying service worker"
cat src/service-worker.js >> build/service-worker.js

echo "[+] Copying built files into build directory"
cp -R build/ ../
