%global composer_vendor         fkooman
%global composer_project        vpn-server-api
%global composer_namespace      %{composer_vendor}/VPN/Server

%global github_owner            eduVPN
%global github_name             vpn-server-api
%global github_commit           e2c7fef68b4b3d4f4937bb1372e2f18a146e602d
%global github_short            %(c=%{github_commit}; echo ${c:0:7})

Name:       vpn-server-api
Version:    2.1.2
Release:    1%{?dist}
Summary:    REST service to control OpenVPN instances  

Group:      Applications/Internet
License:    ASL-2.0

URL:        https://github.com/%{github_owner}/%{github_name}
Source0:    %{url}/archive/%{github_commit}/%{name}-%{version}-%{github_short}.tar.gz
Source1:    %{name}-autoload.php
Source2:    %{name}-httpd.conf

BuildArch:  noarch
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 

Requires:   openvpn
Requires:   httpd
Requires:   php(language) >= 5.4
Requires:   php-pcre
Requires:   php-spl
Requires:   php-composer(fkooman/http) >= 1.0.0
Requires:   php-composer(fkooman/http) < 2.0.0
Requires:   php-composer(fkooman/config) >= 1.0.0
Requires:   php-composer(fkooman/config) < 2.0.0
Requires:   php-composer(fkooman/rest) >= 1.0.0
Requires:   php-composer(fkooman/rest) < 2.0.0
Requires:   php-composer(fkooman/io) >= 1.0.0
Requires:   php-composer(fkooman/io) < 2.0.0
Requires:   php-composer(fkooman/rest-plugin-authentication) >= 2.0.0
Requires:   php-composer(fkooman/rest-plugin-authentication) < 3.0.0
Requires:   php-composer(fkooman/rest-plugin-authentication-basic) >= 2.0.0
Requires:   php-composer(fkooman/rest-plugin-authentication-basic) < 3.0.0
Requires:   php-composer(monolog/monolog) >= 1.17
Requires:   php-composer(monolog/monolog) < 2.0
Requires:   php-composer(guzzlehttp/guzzle) >= 5.3
Requires:   php-composer(guzzlehttp/guzzle) < 6.0
Requires:   php-composer(symfony/class-loader)

Requires(post): policycoreutils-python
Requires(postun): policycoreutils-python

%description
This service runs on the OpenVPN instances to control their behavior.

%prep
%setup -qn %{github_name}-%{github_commit} 
cp %{SOURCE1} src/%{composer_namespace}/autoload.php

sed -i "s|require_once dirname(__DIR__).'/vendor/autoload.php';|require_once '%{_datadir}/%{name}/src/%{composer_namespace}/autoload.php';|" bin/*
sed -i "s|require_once dirname(__DIR__).'/vendor/autoload.php';|require_once '%{_datadir}/%{name}/src/%{composer_namespace}/autoload.php';|" web/*.php
sed -i "s|dirname(__DIR__)|'%{_datadir}/%{name}'|" bin/*

%build

%install
# Apache configuration
install -m 0644 -D -p %{SOURCE2} ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf.d/%{name}.conf

# Application
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/%{name}
cp -pr web src ${RPM_BUILD_ROOT}%{_datadir}/%{name}

mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
(
cd bin
for f in `ls *`
do
    cp -pr ${f} ${RPM_BUILD_ROOT}%{_bindir}/%{name}-${f}
done
)

# Config
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}
cp -p config/config.yaml.example ${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/config.yaml
cp -p config/log.yaml.example ${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/log.yaml

ln -s ../../../etc/%{name} ${RPM_BUILD_ROOT}%{_datadir}/%{name}/config

# Data
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/lib/%{name}

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
%dir %attr(-,apache,apache) %{_sysconfdir}/%{name}
%config(noreplace) %attr(0600,apache,apache) %{_sysconfdir}/%{name}/config.yaml
%config(noreplace) %attr(0600,openvpn,openvpn) %{_sysconfdir}/%{name}/log.yaml
%{_bindir}/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/src
%{_datadir}/%{name}/web
%{_datadir}/%{name}/config
%dir %attr(0711,apache,apache) %{_localstatedir}/lib/%{name}
%doc README.md CHANGES.md composer.json config/config.yaml.example
%license COPYING

%changelog
* Wed Jan 20 2016 François Kooman <fkooman@tuxed.net> - 2.1.2-1
- update to 2.1.2

* Mon Jan 18 2016 François Kooman <fkooman@tuxed.net> - 2.1.1-1
- update to 2.1.1

* Mon Jan 18 2016 François Kooman <fkooman@tuxed.net> - 2.1.0-1
- update to 2.1.0

* Mon Jan 11 2016 François Kooman <fkooman@tuxed.net> - 2.0.2-1
- update to 2.0.2
- add client-connect and client-disconnect scripts

* Mon Jan 11 2016 François Kooman <fkooman@tuxed.net> - 2.0.1-1
- update to 2.0.1

* Tue Jan 05 2016 François Kooman <fkooman@tuxed.net> - 2.0.0-1
- update to 2.0.0

* Tue Dec 22 2015 François Kooman <fkooman@tuxed.net> - 1.1.0-1
- update to 1.1.0

* Wed Dec 16 2015 François Kooman <fkooman@tuxed.net> - 1.0.1-1
- update to 1.0.1

* Fri Dec 11 2015 François Kooman <fkooman@tuxed.net> - 1.0.0-4
- give access to libdir

* Fri Dec 11 2015 François Kooman <fkooman@tuxed.net> - 1.0.0-3
- fix autoloader

* Fri Dec 11 2015 François Kooman <fkooman@tuxed.net> - 1.0.0-2
- fix socket-raw requirement, update autoloader

* Fri Dec 11 2015 François Kooman <fkooman@tuxed.net> - 1.0.0-1
- initial release
