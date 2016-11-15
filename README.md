# RPM 

This repository contains all RPM spec files for software that is not part 
of Fedora/EPEL, including dependencies and the VPN software itself.

The repository contains three additional scripts:

* `build.sh` to build the actual software, locally;
* `upload.sh` to upload it to a web server somewhere so COPR can access it;
* `copr.sh` to build it on COPR.

The resulting packages are available in the COPR repository at 
[https://copr.fedorainfracloud.org/coprs/fkooman/eduvpn-dev/](https://copr.fedorainfracloud.org/coprs/fkooman/eduvpn-dev/).

## Building

    $ sudo yum -y install epel-release
    $ sudo yum -y install fedora-packager
    $ rpmdev-setuptree

Now, you can build the packages, NOTE, do not specify `.spec`:

    $ sh build.sh php-fkooman-oauth2-client

Some of the packages will depend on other packages available in EPEL, or on 
packages in this repository, so you need to install/build those first.

After building all of them you can put them in a directory and run create_repo 
over it. 

**TBD**

## Upload

**OPTIONAL**

Simply uploads the source RPM somewhere:

    $ sh upload.sh php-fkooman-oauth2-client

## COPR

**OPTIONAL**

You need to have COPR setup, including the API key. 

    $ sh copr.sh php-fkooman-oauth2-client

