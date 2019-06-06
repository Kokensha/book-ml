# 04-02節のコマンドリスト
書籍の内容を読み合わせながら、実行してください。


```
$ sudo raspi-config

$ df -h

$ sudo apt-get update
$ sudo apt-get upgrade
$ sudo rpi-update
$ sudo reboot now

$ sudo nano /etc/dphys-swapfile
$ sudo /etc/init.d/dphys-swapfile stop
$ sudo /etc/init.d/dphys-swapfile start

$ free -m

$ sudo apt-get install build-essential cmake pkg-config
$ sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
$ sudo apt-get install libavcodec-dev libavformat-dev libswscaledev libv4l-dev
$ sudo apt-get install libxvidcore-dev libx264-dev
$ sudo apt-get install libgtk2.0-dev libgtk-3-dev
$ sudo apt-get install libatlas-base-dev gfortran
$ sudo apt-get install python2.7-dev python3-dev

$ cd

$ mkdir workspace
$ cd workspace

$ wget -O opencv.zip https://github.com/opencv/opencv/archive/3.4.4.zip
$ unzip opencv.zip

$ wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/3.4.4.zip
$ unzip opencv_contrib.zip

$ cd opencv-3.4.4/
$ mkdir build
$ cd build

$ cmake -D CMAKE_BUILD_TYPE=RELEASE \
-D CMAKE_INSTALL_PREFIX=/usr/local \
-D INSTALL_C_EXAMPLES=OFF \
-D INSTALL_PYTHON_EXAMPLES=ON \
-D OPENCV_EXTRA_MODULES_PATH=~/workspace/opencv_contrib-3.4.4/modules \
-D BUILD_EXAMPLES=ON \
-D ENABLE_NEON=ON ..

$ sudo make -j4

$ sudo make install
$ sudo ldconfig

$ cd /usr/local/python/cv2/python-3.5
$ sudo cp cv2.cpython-35m-arm-linux-gnueabihf.so cv2.so
$ cd /usr/local/lib/python3.5/dist-packages
$ sudo ln -s /usr/local/python/cv2/python-3.5/cv2.so cv2.so

$ sudo nano /etc/dphys-swapfile

$ sudo /etc/init.d/dphys-swapfile stop
$ sudo /etc/init.d/dphys-swapfile start
$ free -m

$ sudo pip3 install picamera
$ sudo raspi-config
$ raspistill -o test.jpg
```

