<a id="readme-top"></a>
<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Mathis-Werner/FMRCompanion">
    <img src="images/FMR-logo-blue.jpg" alt="Logo" width="200" height="200">
  </a>

<h3 align="center">FMRCompanion</h3>
</div>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#Setting up the RasPi">Setting up the RasPi</a></li>
        <li><a href="#Setup in QGroundcontrol">Setup in QGroundcontrol</a></li>
      </ul>
    </li>
    <li><a href="#Code Overview">Code Overview</a></li>
    <li><a href="#general workflow">General Workflow</a></li>
    <li><a href="#Required python packages">Required python packages</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This project contains all required code for the inhouse FMRCompanion computer to assist the main PX4 flightcontroller. All code is written in python and ready to be implemented on a RasPi 5 according to the getting started section. **Before developing new functionalitys for the RasPi or including new mavlink messages carefully read the General Workflow section below**

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

This section gives a quick rundown on how to setup a brand new RasPi download the repository and install all required software. The second part of the section explains the setup process required on the flightcontroller using qgroundcontrol to enable the mavlink communication between flightcontroller and Pi over ethernet using mavlink

### Setting up the RasPi

#### Flashing RASPBERRY PI OS
Download and install RasPi imager and setup according to this [guide](https://www.raspberrypi.com/documentation/computers/getting-started.html). Connect SD card to PC and select the model according to your RasPi version (only tested with RasPi 5 although others should work as well) and RASPBERRY PI OS (64-BIT) as the opperating system. During setup ensure that both host name and user name highlighted in the image below are set to FMRCompanion, otherwise paths defind in the code wont initialise correctly. Setup Wifi according to your WiFi credentials (eduroam does not work).

<br />
<div align="center">
  <a href="https://github.com/Mathis-Werner/FMRCompanion">
    <img src="images/SetUpRasPi.png" alt="SetUpRasPi" width="800" height="400">
  </a>
</div>

#### Installing the repository and dependencys on the RasPi

Start the flashed RasPi and open a terminal either using SSH which has to be [setup](https://randomnerdtutorials.com/raspberry-pi-remote-ssh-vs-code/) in VSCode and on the Pi accordingly, or by connecting a monitor and keyboard to the RasPi. (Hotkey to open terminal is Ctrl+Alt+T) The rest of the following setup is done in the opened terminal on the RasPi.

1. **Installing git**
  ```sh
  cd
  sudo apt update
  sudo apt install git -y
  git config --global user.name "FMRCompanion"
  git config --global user.email "none"
   ```

2. **Create folder and clone repository**
  ```sh
  cd
  git init FMRCompanion
  cd FMRCompanion
  git remote add origin https://github.com/Mathis-Werner/FMRCompanion.git
  git pull origin main
  git checkout main
  git branch -D master
   ```
Update FMR-pymavlink submodule
  ```sh
  git submodule update --init --recursive
  ```

3. **Install miniconda**
  ```sh
  cd Downloads # Navigate to downloads folder
  wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh
  bash Miniconda3-latest-Linux-aarch64.sh  # Install
  ```
Enter --> Ctrl+X to open and accept licence, enter again to accept default folder. **After installation type yes to enable conda by default!** 

4. **Create new conda enviroment**
  ```sh
  cd
  cd FMRCompanion
  conda create --name FMRCompanion python=3.9
  conda activate FMRCompanion

  # At this point install all required packages defined in the section below for example:
  # pip install smbus2

  conda config --set auto_activate_base false 
  echo "conda activate FMRCompanion" >> ~/.bashrc # Set FMRCompanion as default enviroment
  source ~/.bashrc
  ```

5. **Enable I2C** 
  ```sh
  sudo raspi-config
  ```
  Interface Options --> I2C --> Enable.

6. **Install I2C tools**
  ```sh
  sudo apt install -y i2c-tools
  ```

7. **Configure ethernet for mavlink communication**<br />
  Get available networks
  ```sh
  cd
  nmcli con show
  ```
  The string in the collum Name, highlighted in the image below corresponding to the TYPE ethernet can variy and is refered to as NetworkName in the following code.
  <br />
  <div align="center">
    <a href="https://github.com/Mathis-Werner/FMRCompanion">
      <img src="images/SetUpNetwork.png" alt="SetUpRasPi" width="800" height="150">
    </a>
  </div>

  Set static ip in the network:
  
  ```sh
  nmcli con modify "NetworkName" ipv4.addresses 192.168.0.1/24 
  nmcli con modify "NetworkName" ipv4.gateway 192.168.0.254 
  nmcli con modify "NetworkName" ipv4.dns 8.8.8.8 
  nmcli con modify "NetworkName" ipv4.method manual
  ```
  Restart NetworkManager:
  ```sh
  nmcli con down "NetworkName" && nmcli con up "NetworkName"
  ```
  Ensure NetworkManager starts on boot:
  ```
  sudo systemctl enable NetworkManager
  sudo systemctl restart NetworkManager
  ```

8. **Enable the autostart of the main.py script on bootup**<br />
  Create launcher.sh in home directory which will be used to define everything happening on boot:
  ```sh
  cd
  nano launcher.sh
  ```
  Open launcher.sh using nano:
  ```sh
  sudo nano launcher.sh
  ```
  In the file add the following code:
  ```
  #!/bin/sh
  # launcher.sh
  # Script to define execution on boot

  cd 
  cd ~/FMRCompanion
  sudo ~/FMRCompanion/miniconda3/envs/FMRCompanion/pin/python main.py #Runs main.py using the FMRCompanion conda enviroment
  cd
  ```
  Ctrl+X --> Y --> Enter to save

### Setup in QGroundcontrol

1. **Flash the flightcontroller with the desired firmware**
2. **Connect the flightcontroller to QGroundcontrol on a PC**
3. **Go to parameters set and update the following parameters**
  * MAV_2_Config = Ethernet (1000) (Declare Mavlink port 2 as Ethernet)
  * MAV_2_Mode = Onboard (Transmit default on board parameter set)
  * MAV_2_REMOTE_PRT = 14540 (Set port for companion computer)
  * MAV_2_UDP_PRT = 14540 (Set port for companion computer)
4. **Setup the ethernet network**<br />
  In QGroundcontrol click on QGroundcontrol symbol --> Analyze Tools --> MAVLink Console and enter (note that the configuration is stored on the microsd card so if the corresponding "net.cfg" file is deletede the setup has to be repeated):
  ```sh
  echo DEVICE=eth0 > /fs/microsd/net.cfg
  echo BOOTPROTO=static >> /fs/microsd/net.cfg
  echo IPADDR=192.168.0.4 >> /fs/microsd/net.cfg 
  echo NETMASK=255.255.255.0 >>/fs/microsd/net.cfg
  echo ROUTER=192.168.0.254 >>/fs/microsd/net.cfg
  echo DNS=192.168.0.254 >>/fs/microsd/net.cfg
  netman update -i eth0
  ```
Reboot the flightcontroller

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- Code Overview -->
## Code Overview

``` sh
/FMRCompanion
│── main.py  # Main Script
│── /tools   # Add all self developed classes to run with main here
│   │── __init__.py 
│   │── logger.py  # Contains the Logger class used to write csv
│   │── uavtracker.py  # Contains the UAVTracker class used to handle mavlink communication with px4 using pymavlink
│   │── initCompanion.py # All functions to run on script start should be included here e.g. USB-Drive detection
│── /peripherals   # Add all sensors/external hardware here
│   │── __init__.py
│   │── hcla02x5eb.py # Contains the HCLA02X5EB pressure sensor class
│   │── tca9548a.py # Contains the 
│── /threads # Includes functions to be started in thread
│   │── __init__.py
│   │── sensorReadout.py # Thread setting up the sensors and multiplexer and writing measured data to the loggers buffer
│── /tests # Folder to included scripts for testing purposes
│── /pymavlink # Submodule linked to custom FMR-pymavlink repo
```
### Logger Class Overview

#### Description
The logger is used to store all data to a external USB stick. It is designed to be used in a way where all recorded data is first loaded into a buffer using the log_data() function so that all recorded data at a time step can be written to the .csv at the same time labled by the current datetime. The logger will automatically try to detect a USB drive connected to the pi to use for storing the data. If desired the directory can explicitly specified during intialisation by for example:

```python
logger = Logger("/media/FMRCompanion/NameOfYourStick")
```

#### Functions
* create_csv(): Creates a new csv file with the naming convention "Sensor_log{Current Date/Time}" which will then be filled with data by write_data_to_csv()
* log_data(data_lable, value): Loads data into the data_buffer with data_lable used later when writing the data to the file in the header and the value in the row corresponding to the of writing
* write_data_to_csv(): Writes all data stored in the buffer by using log_data() to the csv file automatically creating a new row with the current timestamp and creating new headers when a new data_lable was created using log_data()

#### Example

```python
logger = Logger() # Creates logger object automatically detecting attached drives
logger.create_csv() # Creates a .csv on the drive in which to store all data
data_sensor_a = read_sensor_a() # Read data from sensor
logger.log_data("Sensor_A", data_sensor_a) # Store data in buffer
data_sensor_b = read_sensor_b()
logger.log_data("Sensor_B", data_sensor_b) # Store data in buffer
logger.write_data_to_csv() # Writes all data stored in the buffer into csv
```

### UAVtracker Class Overview

#### Description
The uavtracker class is setup to both initialise a communication with the attached flightcontroller using the mavlink protocoll and handle all data transfer between RasPi and flgihtcontroller. For this the FMR-custom pymavlink repository is used. The Flightcontroller streams a default message set defined by the ONBOARD profile where new messages can be requested using the request_message() function. Recieving and sending mavlink messages using pymavlink is setup as asynchronus functions to avoid code blocking.

#### Functions
* run(): Main loop used to establish a connection to the flight controller and starting the asynchronous execution of all coroutines defined in the asyncio.gather() functions
* request_message(ID, sample_time): Function to request a certain mavlink message from the common message set defined by the ID, at a sampling time given by sample_time (s)
* wait_conn(): Function sending a pinging the flightcontroller until a response is recieved to trigger the flightcontroller to stream over mavlink
* run_in_thread(): Auxillary function to enable threading of asyncio functions
* get_mavlink_message(msg_type): Allows to listen to a specific message type for example 'HEARTHBEAT' and return message once recieved. Note that this function is blocking and should be used carefully
* message_receiver(): Asynchronous coroutine which listens to incomming mavlink traffic and updates class attributes based on recieved data. **This is the place to include new data which should be recieved from the flightcontroller**
* message_dispatcher(): Asynchronous coroutine which sends mavlink messages to the flightcontroller at a sampling frequency defined by the mav_send_sample_time class attribute **This is the place to add data which should be send to the flightcontroller (note that message must be included in the common message definitions according to the readme in the pymavlink submodule)**

#### Example
With the following example a communication with the flightcontroller can be initialised in a seperate thread with the drone.run_in_thread function continously updating the object attributes based on the values read from the flightcontroller.
```python
drone = UAVTracker(gps_sample_time = 0.05, mav_send_sample_time = 0.02) # Create UAVTracker object
updateDroneThread = threading.Thread(target=drone.run_in_thread, daemon=True) # Create thread for UAVTracker object
updateDroneThread.start() # Start thread
```

#### Further Reading

[Mavlink messaging and interaction with uORB](https://docs.px4.io/main/en/middleware/mavlink.html)
[Outdated yet interesting pymavlink doc](https://www.ardusub.com/developers/pymavlink.html)
[Up to date pymavlink doc](https://mavlink.io/en/mavgen_python/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GENERAL WORKFLOW -->
## General Workflow

This section gives a guidline to the development of new features on the RasPi and in the PX4 Firmware. The project is based around multiple github repositorys which are linked using submodules and have to be updated accordingly in all repositorys once changes are made.

### RasPi

The structure of the FMRCompanion codebase follows clean coding principals, isolating independend functionalitys as much as possible in order to reduce dependencys and enabling modular development. When developing new features it should be concidered first where the feature belongs according to the folder structure presented above. 
If for example a new sensor is implemented and should be logged all code required for recieving data from the sensor should be written in a corresponding class in the /peripherals folder. This class can then be initialised in the /threads/sensorReadout function so that the sensor measuring and logging is handled in the corresponding thread. To give another example if some functionality has to be executed only once on startup for example a beeper making a noise once when the script has started it should be included in the function tools/initCompanion. 
As a general guidline the main.py script should be kept as clean as possible only initialising the threads used for sensorReadout and UAV communication and keeping them alive in a simple while Loop. When setting up the RasPi according to the instructions above, updating the code can be done by simply updating the github repo and pulling the changes on the RasPi.

### Github

For seamless integration of new functionalitys concerning mavlink both the PX4 firmware and the companion utilize the same FMR-mavlink and FMR-pymavlink github repo as a submodule as show in the shematic below.

```sh
PX4-Firmware/
├── src/
│   └── modules/
│       └── mavlink/              
│           ├── mavlink/          ← submodule: FMR-mavLink
│               └── pymavlink/    ← submodule: FMR-pymavlink (via FMR-mavlink)
│

FMRCompanion/
└── pymavlink/                ← submodule: FMR-pymavlink (directly used by FMRCompanion)
```

As a result of this both the RasPi and the flightcontroller work with the same mavlink codebase which is curcial when implementing new mavlink messages or dialects. When updating any given repository which is a submodule of another repository both have to be update accodringly so that all components work with the same codebase. If for example a new mavlink message was created according to the next section in the /mavlink repository and the corresponding common.py was moved to the pymavlink submodule we need to start at the lowest level and first commit the changes in the pymavlink submodule:

```sh
cd pymavlink # go into pymavlink folder (this can vary based on your folder structure)
git commit -am "Some commit message"
git push
```

Now in the mavlink repo which is referencing the pymavlink repository the updated commit has to be included:

```sh
cd .. # Jump one level up from pymavlink into mavlink folder (this can vary based on your folder structure)
git add pymavlink # Add new pymavlink folder which will update the referenced commit hash to correspond to newest pymavlink version
git commit -am "Some commit message"
git push
```

Which has to be done again so that the PX4-Firmwar references the correct version of the mavlink repo:

```sh
cd PX4-Firmware # Go into main PX4-Firmware folder (this can vary based on your folder structure)
git add src/modules/mavlink/mavlink # Reference correct location of the mavlink submodule
git commit -am "Some commit message"
```

After this is done all submodule references are updated accordingly referencing the newest version of the submodules. 

### PX4 Firmware

This section explains how to include new uORB topics in the firmware create a new mavlink message and set it up so that the recieved data updated the created uORB topic and generate the corresponding python code so that the RasPi can send the newly created mavlink message. (All shell script examples start from ~/) It is assumed that the FMR-PX4-Autopilot repository was cloned accordingly and all submodules are checked out at the corresponding branches. When running git submodule update --init --recursive the submodules are checked out in a detached head stead which is not what we want. To fix this navigate to the corresponding submodule for example mavlink and checkout the right branch:

```sh
cd FMR-PX4-Firmware/src/modules/mavlink/mavlink
git checkout v1.14.3-FMR-mavlink
cd pymavlink
git checkout v1.14.3-FMR-pymavlink
```

#### Including new uORB Topic

Navigate to the right folder FMR-PX4-Firmware/msg and copy a existing message renaming it in camel case as desired for this example the new message is called FmrMav. Open the message and fill with desired fields for example:

```sh
uint64 timestamp # time since system start (microseconds)
float64 sensor_1
float64 sensor_2
float64 sensor_3
float64 sensor_4
float64 sensor_5
```

Again in the folder FMR-PX4-Firmware/msg find and open CMakeLists and include the message (after line 224) again in camel case with the appropiate data type e.g.: FmrMav.msg. The message is now included in the firmware folder but only appears in the build after running make.

#### Including new Mavlink Message

Navigate to the folder FMR-PX4-Autopilot\src\modules\mavlink\mavlink\message_definitions\v1.0 which is included in the mavlink submodule and open common.xml which is the mavlink dialect used by the pixhawk and includes open message ID's for custom messages. After line 6362 there is space for custom messages with the available ID's 181-229 (every message must have a unique id). There create a message and add the desired fields for this example we create the message FMR_SENSORS with five available sensor fields:

```c
<message id="180" name="FMR_SENSORS">
      <description>Message to include custom sensor values send by Companion computer.</description>
      <field type="float" name="sens_1">Sensor 1 value.</field>
      <field type="float" name="sens_2">Sensor 2 value.</field>
      <field type="float" name="sens_3">Sensor 3 value.</field>
      <field type="float" name="sens_4">Sensor 4 value.</field>
      <field type="float" name="sens_5">Sensor 5 value.</field>
</message>
```

Now the firmware has to be build from the wsl terminal in the FMR-PX4-Firmware folder so that all required header and sourscode files for the following section are generated from the new message definition:

```sh
make px4_fmu-v6x_fixedwing
```

#### Update Pymavlink

Since we have included a custom message in the common dialect this now needs to be included in the pymavlink firmware. For this we first build the custom dialect python file from in the mavlink repo FMR-PX4-Autopilot\src\modules\mavlink\mavlink:

```sh
python3 -m pymavlink.tools.mavgen --lang=Python3 --wire-protocol=1.0 --output=common message_definitions/v1.0/common.xml
```

The output file "common.py" is now located in the same folder and has to be copied to FMR-PX4-Autopilot\src\modules\mavlink\mavlink\pymavlink\dialects\v10 to be included in the pymavlink submodule.

#### Subscribing uORB topic to Mavlink Message

Although the flightcontroller is now capable of recieving the new mavlink message we can only use the included data when it is published by a uORB topic which is explained in this section. As a example we do now publish the uORB message FmrMav with data recieved from the mavlink stream FMR_SENSORS defined above. (Of course both have to be included before the build using make for this to work) Be paticulary carefull to always take note of the change in naming convention of both the uORB topic and the mavlink message and the propper indentation of the included lines according to the rest of the code. Navigate to Open FMR-PX4-Autopilot\src\modules\mavlink\mavlink_receiver.h header file (Note that this is no longer in the mavlink submodule which is one layer depper) and include the uORB topic FmrMav after line 112 (take note of the naming conversion from camel case for the uORB topic to snake case):

```c
#include <uORB/topics/fmr_mav.h>
```

Add function signature for a function that handles the incomming mavlink message after line 204:

```c
void handle_message_fmr_sensors(mavlink_message_t *msg);
```

and add a uORB publisher:

```c
uORB::Publication<fmr_mav_s>   _fmr_mav_pub{ORB_ID(fmr_mav)};
```

Now open FMR-PX4-Autopilot\src\modules\mavlink\mavlink_receiver.cpp c-code file and add function after line 3060 (here take note of the difference in sensor_1 which is a parameter of the uORB topic and sens_1 which is a parameter send in the mavlink stream):

```c
MavlinkReceiver::handle_message_fmr_sensors(mavlink_message_t *msg)

{
    mavlink_fmr_sensors_t fmr_mav_mavlink;
    mavlink_msg_fmr_sensors_decode(msg, &fmr_mav_mavlink);

    fmr_mav_s fmr_mav{};

    fmr_mav.timestamp = hrt_absolute_time();
    fmr_mav.sensor_1 = (float)fmr_mav_mavlink.sens_1;
    fmr_mav.sensor_2 = (float)fmr_mav_mavlink.sens_2;
    fmr_mav.sensor_3 = (float)fmr_mav_mavlink.sens_3;
    fmr_mav.sensor_4 = (float)fmr_mav_mavlink.sens_4;
    fmr_mav.sensor_5 = (float)fmr_mav_mavlink.sens_5;

    _fmr_mav_pub.publish(fmr_mav);

}
```

Here "mavlink_fmr_sensors_t" and "mavlink_msg_fmr_sensors_decode" are functions from the generated mavlink_msg_fmr_sensors.h file in build/px4_fmu-v6x_fixedwing/mavlink/common/mavlink_msg_fmr_sensors.h. Finaly add the message handler after line 276:

```c
    case MAVLINK_MSG_ID_TEST_MSG:

        handle_message_test_msg(msg);

        break;
```

Now rebuild the firware which should now apply the recieved mavlink messages to the uORB topic.

<!-- Required python packages -->
## Required python packages

* smbus2
* asyncio

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- LICENSE -->
## License

Distributed under the project_license. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Mathis Werner - wer.mathis@gmail.com

Project Link: [https://github.com/Mathis-Werner/FMRCompanion](https://github.com/Mathis-Werner/FMRCompanion)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo_name.svg?style=for-the-badge
[contributors-url]: https://github.com/github_username/repo_name/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/github_username/repo_name.svg?style=for-the-badge
[forks-url]: https://github.com/github_username/repo_name/network/members
[stars-shield]: https://img.shields.io/github/stars/github_username/repo_name.svg?style=for-the-badge
[stars-url]: https://github.com/github_username/repo_name/stargazers
[issues-shield]: https://img.shields.io/github/issues/github_username/repo_name.svg?style=for-the-badge
[issues-url]: https://github.com/github_username/repo_name/issues
[license-shield]: https://img.shields.io/github/license/github_username/repo_name.svg?style=for-the-badge
[license-url]: https://github.com/github_username/repo_name/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
