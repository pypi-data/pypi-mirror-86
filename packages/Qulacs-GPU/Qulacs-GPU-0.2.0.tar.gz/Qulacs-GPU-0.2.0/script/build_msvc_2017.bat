mkdir visualstudio
cd visualstudio
cmake -G "Visual Studio 15 2017" -A "x64" ..
cd ..
cmake --build ./visualstudio --target ALL_BUILD --config Release
cmake --build ./visualstudio --target python --config Release

