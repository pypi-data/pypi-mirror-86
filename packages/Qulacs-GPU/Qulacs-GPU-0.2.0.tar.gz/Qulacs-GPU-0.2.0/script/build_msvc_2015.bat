mkdir visualstudio
cd visualstudio
cmake -G "Visual Studio 14 2015 Win64" ..
cd ..
cmake --build ./visualstudio --target ALL_BUILD --config Release
cmake --build ./visualstudio --target python --config Release

