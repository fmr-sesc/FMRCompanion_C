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
  <a href="https://github.com/github_username/repo_name">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
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
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This project contains all required code for the inhouse FMRCompanion computer to assist the main PX4 flightcontroller. The companion is capable All code is written in python and ready to be implemented on a RasPi 5 according to the getting started section. 

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

1. Installing git
  ```sh
  cd
  sudo apt update
  sudo apt install git -y
  git config --global user.name "FMRCompanion"
  git config --global user.email "none"
   ```
2. Create folder and clone repository
  ```sh
  cd
  git init FMRCompanion
  cd FMRCompanion
  git remote add origin https://github.com/Mathis-Werner/FMRCompanion.git
  git pull origin main
  git checkout main
  git branch -D master
   ```
3. Install miniconda
  ```sh
  cd Downloads # Navigate to downloads folder
  wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh
  bash Miniconda3-latest-Linux-aarch64.sh  # Install
  ```
Enter --> Ctrl+X to open and accept licence, enter again to accept default folder. **After installation type yes to enable conda by default!** 
4. Create new conda enviroment
  ```sh
  cd
  cd FMRCompanion
  conda create --name FMRCompanion python=3.9
  conda activate FMRCompanion

  # **At this point install all required packages defined in the section below**

  conda config --set auto_activate_base false 
  echo "conda activate FMRCompanion" >> ~/.bashrc # Set FMRCompanion as default enviroment
  source ~/.bashrc
  ```
5. Enable I2C 
  ```sh
  sudo raspi-config
  ```
  Interface Options --> I2C --> Enable
6. Install I2C tools
  ```sh
  sudo apt install -y i2c-tools
  ```
7. Configure ethernet for mavlink communication
  Get available networks
  ```sh
  cd
  nmcli con show
  ```
  The string in the collum Name, highlighted in the image below can variy and is refered to as "NetworkName" in the following code.
<br />
<div align="center">
  <a href="https://github.com/Mathis-Werner/FMRCompanion">
    <img src="images/SetUpNetwork.png" alt="SetUpRasPi" width="800" height="150">
  </a>
</div>


### Setup in QGroundcontrol

1. Get a free API Key at [https://example.com](https://example.com)
2. Clone the repo
   ```sh
   git clone https://github.com/github_username/repo_name.git
   ```
3. Install NPM packages
   ```sh
   npm install
   ```
4. Enter your API in `config.js`
   ```js
   const API_KEY = 'ENTER YOUR API';
   ```
5. Change git remote url to avoid accidental pushes to base project
   ```sh
   git remote set-url origin github_username/repo_name
   git remote -v # confirm the changes
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3
    - [ ] Nested Feature

See the [open issues](https://github.com/github_username/repo_name/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Top contributors:

<a href="https://github.com/github_username/repo_name/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=github_username/repo_name" alt="contrib.rocks image" />
</a>



<!-- LICENSE -->
## License

Distributed under the project_license. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Your Name - [@twitter_handle](https://twitter.com/twitter_handle) - email@email_client.com

Project Link: [https://github.com/github_username/repo_name](https://github.com/github_username/repo_name)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* []()
* []()
* []()

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
