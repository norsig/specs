%global composer_vendor         SURFnet
%global composer_project        vpn-server-api
%global composer_namespace      %{composer_vendor}/VPN/Server

%global github_owner            eduvpn
%global github_name             vpn-server-api
%global github_commit           170fef7e6f386838598db810c1329476be13a942
%global github_short            %(c=%{github_commit}; echo ${c:0:7})
%if 0%{?rhel} == 5
%global with_tests              0%{?_with_tests:1}
%else
%global with_tests              0%{!?_without_tests:1}
%endif

Name:       vpn-server-api
Version:    9.0.0
Release:    0.32%{?dist}
Summary:    Web service to control OpenVPN processes

Group:      Applications/Internet
License:    AGPLv3+

URL:        https://github.com/%{github_owner}/%{github_name}
Source0:    %{url}/archive/%{github_commit}/%{name}-%{version}-%{github_short}.tar.gz
Source1:    %{name}-autoload.php
Source2:    %{name}-httpd.conf

BuildArch:  noarch
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 

%if %{with_tests}
BuildRequires:  %{_bindir}/phpunit
BuildRequires:  %{_bindir}/phpab
BuildRequires:  php(language) >= 5.4.0
BuildRequires:  php-curl
BuildRequires:  php-date
BuildRequires:  php-filter
BuildRequires:  php-mbstring
BuildRequires:  php-json
BuildRequires:  php-pcre
BuildRequires:  php-pdo
BuildRequires:  php-spl
BuildRequires:  php-standard
BuildRequires:  php-composer(eduvpn/common)
BuildRequires:  php-composer(psr/log)
BuildRequires:  php-composer(christian-riesen/otp)
BuildRequires:  php-composer(guzzlehttp/guzzle) >= 5.3.0
BuildRequires:  php-composer(guzzlehttp/guzzle) < 6.0.0
BuildRequires:  php-composer(symfony/class-loader)
%endif

Requires:   openvpn
Requires:   httpd
Requires:   php(language) >= 5.4.0
Requires:   php-curl
Requires:   php-date
Requires:   php-filter
Requires:   php-mbstring
Requires:   php-json
Requires:   php-pcre
Requires:   php-pdo
Requires:   php-spl
Requires:   php-standard
Requires:   php-composer(eduvpn/common)
Requires:   php-composer(psr/log)
Requires:   php-composer(christian-riesen/otp)
Requires:   php-composer(guzzlehttp/guzzle) >= 5.3.0
Requires:   php-composer(guzzlehttp/guzzle) < 6.0.0
Requires:   php-composer(symfony/class-loader)

Requires(post): policycoreutils-python
Requires(postun): policycoreutils-python

%description
VPN Server API.

%prep
%setup -qn %{github_name}-%{github_commit} 
cp %{SOURCE1} src/%{composer_namespace}/autoload.php

sed -i "s|require_once sprintf('%s/vendor/autoload.php', dirname(__DIR__));|require_once '%{_datadir}/%{name}/src/%{composer_namespace}/autoload.php';|" bin/*
sed -i "s|require_once sprintf('%s/vendor/autoload.php', dirname(__DIR__));|require_once '%{_datadir}/%{name}/src/%{composer_namespace}/autoload.php';|" web/*.php
sed -i "s|dirname(__DIR__)|'%{_datadir}/%{name}'|" bin/*

%build

%install
# Apache configuration
install -m 0644 -D -p %{SOURCE2} ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf.d/%{name}.conf

# Application
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/%{name}
cp -pr web src ${RPM_BUILD_ROOT}%{_datadir}/%{name}

mkdir -p ${RPM_BUILD_ROOT}%{_sbindir}
(
cd bin
for f in `ls *`
do
    bf=`basename ${f} .php`
    cp -pr ${f} ${RPM_BUILD_ROOT}%{_sbindir}/%{name}-${bf}
    chmod 0755 ${RPM_BUILD_ROOT}%{_sbindir}/%{name}-${bf}
done
)

# Config
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}
cp config/dh.pem ${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}
ln -s ../../../etc/%{name} ${RPM_BUILD_ROOT}%{_datadir}/%{name}/config
ln -s ../../../etc/openvpn ${RPM_BUILD_ROOT}%{_datadir}/%{name}/openvpn-config

# Data
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/lib/%{name}
ln -s ../../../var/lib/%{name} ${RPM_BUILD_ROOT}%{_datadir}/%{name}/data
ln -s ../../../var/lib/openvpn ${RPM_BUILD_ROOT}%{_datadir}/%{name}/openvpn-data

%if %{with_tests} 
%check
%{_bindir}/phpab --output tests/bootstrap.php tests
echo 'require "%{buildroot}%{_datadir}/%{name}/src/%{composer_namespace}/autoload.php";' >> tests/bootstrap.php
%{_bindir}/phpunit \
    --bootstrap tests/bootstrap.php
%endif

%post
semanage fcontext -a -t httpd_sys_rw_content_t '%{_localstatedir}/lib/%{name}(/.*)?' 2>/dev/null || :
restorecon -R %{_localstatedir}/lib/%{name} || :

%postun
if [ $1 -eq 0 ] ; then  # final removal
semanage fcontext -d -t httpd_sys_rw_content_t '%{_localstatedir}/lib/%{name}(/.*)?' 2>/dev/null || :
fi

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%config(noreplace) %{_sysconfdir}/%{name}/dh.pem
%dir %attr(-,apache,openvpn) %{_sysconfdir}/%{name}
%{_sbindir}/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/src
%{_datadir}/%{name}/web
%{_datadir}/%{name}/config
%{_datadir}/%{name}/openvpn-config
%{_datadir}/%{name}/data
%{_datadir}/%{name}/openvpn-data
%dir %attr(0710,apache,apache) %{_localstatedir}/lib/%{name}
%doc README.md composer.json config/config.yaml.example
%license LICENSE

%changelog
* Fri Oct 14 2016 François Kooman <fkooman@tuxed.net> - 9.0.0-0.32
- rebuilt

* Tue Oct 11 2016 François Kooman <fkooman@tuxed.net> - 9.0.0-0.31
- rebuilt

* Tue Oct 11 2016 François Kooman <fkooman@tuxed.net> - 9.0.0-0.30
- rebuilt

* Tue Oct 11 2016 François Kooman <fkooman@tuxed.net> - 9.0.0-0.29
- rebuilt

* Tue Oct 11 2016 François Kooman <fkooman@tuxed.net> - 9.0.0-0.28
- rebuilt

* Tue Oct 11 2016 François Kooman <fkooman@tuxed.net> - 9.0.0-0.27
- rebuilt

* Mon Oct 10 2016 François Kooman <fkooman@tuxed.net> - 9.0.0-0.26
- rebuilt

* Mon Oct 10 2016 François Kooman <fkooman@tuxed.net> - 9.0.0-0.25
- rebuilt

* Mon Oct 10 2016 François Kooman <fkooman@tuxed.net> - 9.0.0-0.24
- rebuilt

* Fri Oct 07 2016 François <fkooman@tuxed.net> - 9.0.0-0.23
- rebuilt

* Fri Oct 07 2016 François <fkooman@tuxed.net> - 9.0.0-0.22
- rebuilt

* Thu Oct 06 2016 François Kooman <fkooman@tuxed.net> - 9.0.0-0.21
- update to 56418cd136ae6f4c9aa203ef63ff50506a0e5bc0

* Thu Oct 06 2016 François Kooman <fkooman@tuxed.net> - 9.0.0-0.20
- update to c3cd4be356a44213f1f78702f42c84e7b8a2bed9

* Wed Oct 05 2016 François Kooman <fkooman@tuxed.net> - 9.0.0-0.19
- update to e0a7c0479ef02cd71800260f2c9197c6a680ef86

* Tue Oct 04 2016 François Kooman <fkooman@tuxed.net> - 9.0.0-0.18
- update to 08fec99cdc44ace9bf0ec8dfe7a9c69f51fdb673

* Sun Oct 02 2016 François Kooman <fkooman@tuxed.net> - 9.0.0-0.17
- update to 65058f6be19d884dbd67a9f368daa847ae529aa3

* Sun Oct 02 2016 François Kooman <fkooman@tuxed.net> - 9.0.0-0.16
- rebuilt

* Sun Oct 02 2016 François Kooman <fkooman@tuxed.net> - 9.0.0-0.15
- update to 747ec8eb18787c5bab904b7941c0558d53e7b75a

* Fri Sep 30 2016 François Kooman <fkooman@tuxed.net> - 9.0.0-0.14
- update to 90e7d4df14e1856d4a942e542134c0ef890584bd
- fix bin scripts

* Fri Sep 30 2016 François Kooman <fkooman@tuxed.net> - 9.0.0-0.13
- update to ef1e4a1415727731035512c0eaf1994b5916f28e

* Thu Sep 29 2016 François Kooman <fkooman@tuxed.net> - 9.0.0-0.12
- forgot Guzzle in autoloader

* Thu Sep 29 2016 François Kooman <fkooman@tuxed.net> - 9.0.0-0.11
- update to bdda5d5bc78ab5050a076c98d80a276c1a4563e3

* Mon Sep 26 2016 François Kooman <fkooman@tuxed.net> - 9.0.0-0.10
- update to 27271f288683e33d5c4491567250e52df7441b1a

* Fri Sep 23 2016 François Kooman <fkooman@tuxed.net> - 9.0.0-0.9
- update to 08075c98880e5a24c01b3a8e1891aebbd3d21904

* Fri Sep 23 2016 François Kooman <fkooman@tuxed.net> - 9.0.0-0.8
- update to c30bd06f5becb8b416a95bad13baeb67ffc077c7

* Wed Sep 21 2016 François Kooman <fkooman@tuxed.net> - 9.0.0-0.7
- update to 8c1a576671f6ff8d20d024ed47a1c2c1dcc66a74

* Sun Sep 18 2016 François Kooman <fkooman@tuxed.net> - 9.0.0-0.6
- update to 1670b267f5d61e147fe6a36bcfb11c4fc5f89547

* Thu Sep 15 2016 François Kooman <fkooman@tuxed.net> - 9.0.0-0.5
- update to e4df403481a1da210c68464189b3c116dc6be0f9

* Thu Sep 15 2016 François Kooman <fkooman@tuxed.net> - 9.0.0-0.4
- update to d305585924e11e755be324b1801e28c82105c2c7

* Thu Sep 15 2016 François Kooman <fkooman@tuxed.net> - 9.0.0-0.3
- update to 753cd0c6411f1413b9366e6db6114bd8434bf405

* Wed Sep 14 2016 François Kooman <fkooman@tuxed.net> - 9.0.0-0.2
- rebuilt

* Wed Sep 14 2016 François Kooman <fkooman@tuxed.net> - 9.0.0-0.1
- update to 9.0.0
