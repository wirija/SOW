## Postal Library for address parsing 


## THIS SHIT IS NOT WORKING -- SO USING DEEPARSE
Remember to install 
https://github.com/openvenues/pypostal

### Installation instruction - Mac
git clone https://github.com/openvenues/libpostal
cd libpostal
./bootstrap.sh
./configure --datadir=[...some dir with a few GB of space...]
make
sudo make install

#### On Linux it's probably a good idea to run
sudo ldconfig

pip install postal

### Installation instruction - Windows
Install msys2 and launch a shell using the MSYS2 MingW 64-bit start menu option, not the usual MSYS2 MSYS option. This is important because we don't want our libpostal.dll to link to msys-2.0.dll (Python seems to hang if you load this DLL).

Then:

pacman -S autoconf automake curl git make libtool gcc mingw-w64-x86_64-gcc
git clone https://github.com/openvenues/libpostal
cd libpostal
cp -rf windows/* ./
./bootstrap.sh
./configure --datadir=[...some dir with a few GB of space...]
make
make install
mkdir headers && cp -r /usr/include/libpostal/ headers/