%global composer_vendor         fkooman
%global composer_project        vpn-server-api
%global composer_namespace      %{composer_vendor}/VPN/Server

%global github_owner            eduvpn
%global github_name             vpn-server-api
%global github_commit           b4b56fc9765187b3a79953633ead12864f250bf2
%global github_short            %(c=%{github_commit}; echo ${c:0:7})
%if 0%{?rhel} == 5
%global with_tests              0%{?_with_tests:1}
%else
%global with_tests              0%{!?_without_tests:1}
%endif

Name:       vpn-server-api
Version:    7.1.0
Release:    1%{?dist}
Summary:    VPN Server API

Group:      Applications/Internet
License:    ASL-2.0

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
BuildRequires:  php-date
BuildRequires:  php-filter
BuildRequires:  php-pcre
BuildRequires:  php-pdo
BuildRequires:  php-spl
BuildRequires:  php-standard
BuildRequires:  php-composer(fkooman/config) >= 1.0.0
BuildRequires:  php-composer(fkooman/config) < 2.0.0
BuildRequires:  php-composer(fkooman/http) >= 1.6.0
BuildRequires:  php-composer(fkooman/http) < 2.0.0
BuildRequires:  php-composer(fkooman/io) >= 1.2.0
BuildRequires:  php-composer(fkooman/io) < 2.0.0
BuildRequires:  php-composer(fkooman/json) >= 2.0.0
BuildRequires:  php-composer(fkooman/json) < 3.0.0
BuildRequires:  php-composer(fkooman/rest) >= 1.0.0
BuildRequires:  php-composer(fkooman/rest) < 2.0.0
BuildRequires:  php-composer(fkooman/rest-plugin-authentication) >= 2.0.0
BuildRequires:  php-composer(fkooman/rest-plugin-authentication) < 3.0.0
BuildRequires:  php-composer(fkooman/rest-plugin-authentication-bearer) >= 2.4.0
BuildRequires:  php-composer(fkooman/rest-plugin-authentication-bearer) < 3.0.0
BuildRequires:  php-composer(guzzlehttp/guzzle) >= 5.3
BuildRequires:  php-composer(guzzlehttp/guzzle) < 6.0
BuildRequires:  php-composer(monolog/monolog) >= 1.17
BuildRequires:  php-composer(monolog/monolog) < 2.0
BuildRequires:  php-composer(psr/log) >= 1.0.0
BuildRequires:  php-composer(psr/log) < 2.0.0
BuildRequires:  php-composer(paragonie/random_compat) >= 1.0.0
BuildRequires:  php-composer(paragonie/random_compat) < 2.0.0
BuildRequires:  php-composer(christian-riesen/otp) >= 1.0
BuildRequires:  php-composer(christian-riesen/otp) < 2.0
BuildRequires:  php-composer(christian-riesen/base32) >= 1.0
BuildRequires:  php-composer(christian-riesen/base32) < 2.0
BuildRequires:  php-composer(symfony/class-loader)
%endif

Requires:   openvpn
Requires:   httpd
Requires:   php(language) >= 5.4.0
Requires:   php-date
Requires:   php-filter
Requires:   php-pcre
Requires:   php-pdo
Requires:   php-spl
Requires:   php-standard
Requires:   php-composer(fkooman/config) >= 1.0.0
Requires:   php-composer(fkooman/config) < 2.0.0
Requires:   php-composer(fkooman/http) >= 1.6.0
Requires:   php-composer(fkooman/http) < 2.0.0
Requires:   php-composer(fkooman/io) >= 1.2.0
Requires:   php-composer(fkooman/io) < 2.0.0
Requires:   php-composer(fkooman/json) >= 2.0.0
Requires:   php-composer(fkooman/json) < 3.0.0
Requires:   php-composer(fkooman/rest) >= 1.0.0
Requires:   php-composer(fkooman/rest) < 2.0.0
Requires:   php-composer(fkooman/rest-plugin-authentication) >= 2.0.0
Requires:   php-composer(fkooman/rest-plugin-authentication) < 3.0.0
Requires:   php-composer(fkooman/rest-plugin-authentication-bearer) >= 2.4.0
Requires:   php-composer(fkooman/rest-plugin-authentication-bearer) < 3.0.0
Requires:   php-composer(guzzlehttp/guzzle) >= 5.3
Requires:   php-composer(guzzlehttp/guzzle) < 6.0
Requires:   php-composer(monolog/monolog) >= 1.17
Requires:   php-composer(monolog/monolog) < 2.0
Requires:   php-composer(psr/log) >= 1.0.0
Requires:   php-composer(psr/log) < 2.0.0
Requires:   php-composer(paragonie/random_compat) >= 1.0.0
Requires:   php-composer(paragonie/random_compat) < 2.0.0
Requires:   php-composer(christian-riesen/otp) >= 1.0
Requires:   php-composer(christian-riesen/otp) < 2.0
Requires:   php-composer(christian-riesen/base32) >= 1.0
Requires:   php-composer(christian-riesen/base32) < 2.0
Requires:   php-composer(symfony/class-loader)

Requires(post): policycoreutils-python
Requires(postun): policycoreutils-python

%description
VPN Server API.

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
cp -p config/pools.yaml.example ${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/pools.yaml
cp -p config/log.yaml.example ${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/log.yaml
ln -s ../../../etc/%{name} ${RPM_BUILD_ROOT}%{_datadir}/%{name}/config

# Data
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/lib/%{name}

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
%dir %attr(-,apache,apache) %{_sysconfdir}/%{name}
%config(noreplace) %attr(0440,apache,apache) %{_sysconfdir}/%{name}/config.yaml
%config(noreplace) %attr(0440,openvpn,apache) %{_sysconfdir}/%{name}/pools.yaml
%config(noreplace) %attr(0440,openvpn,apache) %{_sysconfdir}/%{name}/log.yaml
%{_bindir}/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/src
%{_datadir}/%{name}/web
%{_datadir}/%{name}/config
%dir %attr(0711,apache,apache) %{_localstatedir}/lib/%{name}
%doc README.md CHANGES.md composer.json config/config.yaml.example config/pools.yaml.example config/log.yaml.example
%license COPYING

%changelog
* Thu May 19 2016 François Kooman <fkooman@tuxed.net> - 7.1.0-1
- update to 7.1.0

* Thu May 19 2016 François Kooman <fkooman@tuxed.net> - 7.0.2-1
- update to 7.0.2

* Wed May 18 2016 François Kooman <fkooman@tuxed.net> - 7.0.1-1
- update to 7.0.1

* Wed May 18 2016 François Kooman <fkooman@tuxed.net> - 7.0.0-1
- update to 7.0.0

* Wed May 11 2016 François Kooman <fkooman@tuxed.net> - 6.0.3-1
- update to 6.0.3

* Wed May 11 2016 François Kooman <fkooman@tuxed.net> - 6.0.2-1
- update to 6.0.2

* Tue May 10 2016 François Kooman <fkooman@tuxed.net> - 6.0.1-1
- update to 6.0.1

* Fri May 06 2016 François Kooman <fkooman@tuxed.net> - 6.0.0-1
- update to 6.0.0

* Wed Apr 27 2016 François Kooman <fkooman@tuxed.net> - 5.0.2-1
- update to 5.0.2

* Wed Apr 27 2016 François Kooman <fkooman@tuxed.net> - 5.0.1-1
- update to 5.0.1

* Wed Apr 27 2016 François Kooman <fkooman@tuxed.net> - 5.0.0-1
- update to 5.0.0

* Wed Apr 20 2016 François Kooman <fkooman@tuxed.net> - 4.0.6-1
- update to 4.0.6

* Wed Apr 20 2016 François Kooman <fkooman@tuxed.net> - 4.0.5-1
- update to 4.0.5

* Tue Apr 19 2016 François Kooman <fkooman@tuxed.net> - 4.0.4-1
- update to 4.0.4

* Fri Apr 15 2016 François Kooman <fkooman@tuxed.net> - 4.0.3-1
- update to 4.0.3

* Wed Apr 13 2016 François Kooman <fkooman@tuxed.net> - 4.0.2-1
- update to 4.0.2

* Wed Apr 13 2016 François Kooman <fkooman@tuxed.net> - 4.0.1-1
- update to 4.0.1

* Wed Apr 13 2016 François Kooman <fkooman@tuxed.net> - 4.0.0-1
- update to 4.0.0

* Fri Apr 08 2016 François Kooman <fkooman@tuxed.net> - 3.4.4-1
- update to 3.4.4

* Fri Apr 01 2016 François Kooman <fkooman@tuxed.net> - 3.4.3-1
- update to 3.4.3

* Fri Mar 25 2016 François Kooman <fkooman@tuxed.net> - 3.4.2-1
- update to 3.4.2

* Thu Mar 24 2016 François Kooman <fkooman@tuxed.net> - 3.4.1-1
- update to 3.4.1
- remove fkooman/io dependency

* Tue Mar 15 2016 François Kooman <fkooman@tuxed.net> - 3.4.0-1
- update to 3.4.0

* Mon Mar 14 2016 François Kooman <fkooman@tuxed.net> - 3.3.0-1
- update to 3.3.0

* Mon Mar 07 2016 François Kooman <fkooman@tuxed.net> - 3.2.0-1
- update to 3.2.0

* Fri Mar 04 2016 François Kooman <fkooman@tuxed.net> - 3.1.1-1
- update to 3.1.1

* Fri Mar 04 2016 François Kooman <fkooman@tuxed.net> - 3.1.0-1
- update to 3.1.0

* Thu Mar 03 2016 François Kooman <fkooman@tuxed.net> - 3.0.0-1
- update to 3.0.0

* Mon Feb 29 2016 François Kooman <fkooman@tuxed.net> - 2.5.3-1
- update to 2.5.3

* Thu Feb 25 2016 François Kooman <fkooman@tuxed.net> - 2.5.2-1
- update to 2.5.2

* Thu Feb 25 2016 François Kooman <fkooman@tuxed.net> - 2.5.1-1
- update to 2.5.1

* Wed Feb 24 2016 François Kooman <fkooman@tuxed.net> - 2.5.0-1
- update to 2.5.0

* Mon Feb 22 2016 François Kooman <fkooman@tuxed.net> - 2.4.2-1
- update to 2.4.2

* Mon Feb 22 2016 François Kooman <fkooman@tuxed.net> - 2.4.1-1
- update to 2.4.1

* Mon Feb 22 2016 François Kooman <fkooman@tuxed.net> - 2.4.0-3
- add some missing dependencies

* Mon Feb 22 2016 François Kooman <fkooman@tuxed.net> - 2.4.0-2
- run unit tests during build

* Mon Feb 22 2016 François Kooman <fkooman@tuxed.net> - 2.4.0-1
- update to 2.4.0

* Sat Feb 20 2016 François Kooman <fkooman@tuxed.net> - 2.3.1-1
- update to 2.3.1

* Fri Feb 19 2016 François Kooman <fkooman@tuxed.net> - 2.3.0-1
- update to 2.3.0

* Thu Feb 18 2016 François Kooman <fkooman@tuxed.net> - 2.2.1-1
- update to 2.2.1

* Thu Feb 18 2016 François Kooman <fkooman@tuxed.net> - 2.2.0-1
- update to 2.2.0

* Wed Jan 20 2016 François Kooman <fkooman@tuxed.net> - 2.1.2-2
- fix file permissions for the client.yaml file on installation

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
