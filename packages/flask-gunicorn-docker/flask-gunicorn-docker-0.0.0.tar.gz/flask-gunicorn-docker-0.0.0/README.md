<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]
[![AWS Code Build][codebuild-shield]][codebuild-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://www.linkedin.com/company/kungfuai/">
    <img src="https://media-exp1.licdn.com/dms/image/C4E0BAQEgWgybqu6dDg/company-logo_200_200/0?e=1611187200&v=beta&t=svIQxQQYJJWDvApMPTxnS3w5v_XXMHQFAvtSxzWpy6E" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Flask + Gunicorn with Docker Example</h3>

  <p align="center">
    An example application for writing Flask applications
    <br />
    <a href="https://kungfuai.atlassian.net/wiki/spaces/AR/pages/829325363/Reference+Scalable+Web+Application+Architecture+in+AWS+with+ECS"><strong>Explore the docs »</strong></a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)

### Built With
* [Flask](https://flask.palletsprojects.com/en/1.1.x/)
* [Gunicorn](https://gunicorn.org/)
* [Docker](https://www.docker.com/)
* [Python 3.8](https://www.python.org/)



<!-- GETTING STARTED -->
## Getting Started

Make sure you install Docker and Docker-compose. This project is very simple - exists just to demonstrate
the code needed to run a flask app.

### Prerequisites
* Docker

### Installation

1. Clone the repo
```sh
git clone https://github.com/kungfuai/flask-gunicorn-docker.git
```
2. Run docker-compose
```sh
docker-compose up
```

<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/kungfuai/flask-gunicorn-docker/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Endurance Idehen - endurance.idehen@kungfu.ai

Project Link: [https://github.com/kungfuai/flask-gunicorn-docker.git](https://github.com/kungfuai/flask-gunicorn-docker.git)



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=flat-square
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=flat-square
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=flat-square
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=flat-square
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=flat-square
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/company/kungfuai/
[codebuild-shield]: https://codebuild.us-east-2.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiRFFON2l6NC9xTzRORFpHc1lJYS9GMjBBdE4wb3lNSGRNUnUrSFJYcnFEZGhrK0ZHZHdnRHY3V3RFWWNUcEFSWEtjSzNyNEdjWGdJQW9TYVhUZnR5bm1jPSIsIml2UGFyYW1ldGVyU3BlYyI6Ik5GZDhTQjRTREdkQmtKVkEiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=master
[codebuild-url]: https://us-east-2.console.aws.amazon.com/codesuite/codebuild/478665595712/projects/flask-gunicorn-docker/history?region=us-east-2&builds-meta=%7B%22f%22%3A%7B%22text%22%3A%22%22%7D%2C%22s%22%3A%7B%7D%2C%22n%22%3A20%2C%22i%22%3A0%7D
[product-screenshot]: images/screenshot.png