


sudo chmod 666 /dev/ttyACM0

nohup roscore &>/dev/null &

nohup roslaunch mavros px4.launch fcu_url:=/dev/ttyACM0:921600 gcs_url:=udp://@172.32.65.174 &>/dev/null &

nohup roslaunch realsense2_camera rs_t265.launch &>/dev/null &

nohup rosrun tf2_ros static_transform_publisher 0 0 0 -1.57 0 0 camera_odom_frame local_origin &>/dev/null &

rosrun arion send_odometry


SYS_HAS_MAG

CBRK_IO_SAFETY
CBRK_USB_CHK
CAL_MAG_EN1

sudo chmod 666 /dev/ttyTHS1

nohup roslaunch mavros px4.launch fcu_url:=/dev/ttyTHS1:921600 gcs_url:=udp://@172.32.65.174 &>/dev/null &
sudo chmod 666 /dev/ttyTHS1
nohup roslaunch arion rs_odom_px4.launch &>/dev/null &
NOW=`date +%d-%m-%Y_%I-%M-%S`
nohup roslaunch arion recorder.launch now:=$NOW & 

docker rm mavros  
docker run --name mavros -v /Users/az02290/arion/data:/mnt/files:rw -it px4io/px4-dev-ros-melodic 
cd /mnt/files
 mkdir images
pip install jsonlines
source /opt/ros/melodic/setup.bash
python export_images.py ./camera-10-10-2019_12-58-05.bag ./images /arion/image_compressed --i
python export_rc_in.py ./rc-10-10-2019_10-10-51.bag ./rc /mavros/rc/in


rover_pos_control stop
nohup roslaunch mavros px4.launch fcu_url:=/dev/ttyTHS1:921600 gcs_url:=udp://@192.168.1.48 &>/dev/null &
