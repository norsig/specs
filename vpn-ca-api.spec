%global composer_vendor         fkooman
%global composer_project        vpn-ca-api
%global composer_namespace      %{composer_vendor}/VPN/CA

%global github_owner            eduvpn
%global github_name             vpn-ca-api
%global github_commit           d8416d555877b01a3cbc9f36255fb2e93d991753
%global github_short            %(c=%{github_commit}; echo ${c:0:7})
%if 0%{?rhel} == 5
%global with_tests              0%{?_with_tests:1}
%else
%global with_tests              0%{!?_without_tests:1}
%endif

Name:       vpn-ca-api
Version:    5.1.0
Release:    1%{?dist}
Summary:    VPN CA API

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
BuildRequires:  php(language) >= 5.4
BuildRequires:  php-date
BuildRequires:  php-pcre
BuildRequires:  php-spl
BuildRequires:  php-openssl
BuildRequires:  php-composer(fkooman/config) >= 1.0.0
BuildRequires:  php-composer(fkooman/config) < 2.0.0
BuildRequires:  php-composer(fkooman/http) >= 1.0.0
BuildRequires:  php-composer(fkooman/http) < 2.0.0
BuildRequires:  php-composer(fkooman/rest) >= 1.0.0
BuildRequires:  php-composer(fkooman/rest) < 2.0.0
BuildRequires:  php-composer(fkooman/rest-plugin-authentication) >= 2.0.0
BuildRequires:  php-composer(fkooman/rest-plugin-authentication) < 3.0.0
BuildRequires:  php-composer(fkooman/rest-plugin-authentication-bearer) >= 2.2.0
BuildRequires:  php-composer(fkooman/rest-plugin-authentication-bearer) < 3.0.0
BuildRequires:  php-composer(monolog/monolog) >= 1.17
BuildRequires:  php-composer(monolog/monolog) < 2.0
BuildRequires:  php-composer(psr/log) >= 1.0.0
BuildRequires:  php-composer(psr/log) < 2.0.0
BuildRequires:  php-composer(symfony/class-loader)
%endif

Requires:   httpd
Requires:   easy-rsa >= 3.0.0
Requires:   easy-rsa < 4.0.0
Requires:   openvpn
Requires:   php(language) >= 5.4
Requires:   php-date
Requires:   php-pcre
Requires:   php-spl
Requires:   php-openssl
Requires:   php-composer(fkooman/config) >= 1.0.0
Requires:   php-composer(fkooman/config) < 2.0.0
Requires:   php-composer(fkooman/http) >= 1.0.0
Requires:   php-composer(fkooman/http) < 2.0.0
Requires:   php-composer(fkooman/rest) >= 1.0.0
Requires:   php-composer(fkooman/rest) < 2.0.0
Requires:   php-composer(fkooman/rest-plugin-authentication) >= 2.0.0
Requires:   php-composer(fkooman/rest-plugin-authentication) < 3.0.0
Requires:   php-composer(fkooman/rest-plugin-authentication-bearer) >= 2.2.0
Requires:   php-composer(fkooman/rest-plugin-authentication-bearer) < 3.0.0
Requires:   php-composer(monolog/monolog) >= 1.17
Requires:   php-composer(monolog/monolog) < 2.0
Requires:   php-composer(psr/log) >= 1.0.0
Requires:   php-composer(psr/log) < 2.0.0
Requires:   php-composer(symfony/class-loader)

Requires(post): policycoreutils-python
Requires(postun): policycoreutils-python

%description
VPN CA API.

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
%config(noreplace) %attr(0600,apache,apache) %{_sysconfdir}/%{name}/config.yaml
%{_bindir}/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/src
%{_datadir}/%{name}/web
%{_datadir}/%{name}/config
%dir %attr(0700,apache,apache) %{_localstatedir}/lib/%{name}
%doc README.md CHANGES.md composer.json config/config.yaml.example
%license COPYING

%changelog
* Fri Mar 04 2016 François Kooman <fkooman@tuxed.net> - 5.1.0-1
- update to 5.1.0

* Thu Mar 03 2016 François Kooman <fkooman@tuxed.net> - 5.0.0-1
- update to 5.0.0
- rename to vpn-ca-api

* Thu Feb 25 2016 François Kooman <fkooman@tuxed.net> - 4.4.2-1
- update to 4.4.2

* Thu Feb 25 2016 François Kooman <fkooman@tuxed.net> - 4.4.1-1
- update to 4.4.1

* Wed Feb 24 2016 François Kooman <fkooman@tuxed.net> - 4.4.0-1
- update to 4.4.0

* Mon Feb 22 2016 François Kooman <fkooman@tuxed.net> - 4.3.1-1
- update to 4.3.1
- run tests on build

* Thu Feb 18 2016 François Kooman <fkooman@tuxed.net> - 4.3.0-1
- update to 4.3.0

* Mon Feb 15 2016 François Kooman <fkooman@tuxed.net> - 4.2.3-1
- update to 4.2.3

* Mon Feb 15 2016 François Kooman <fkooman@tuxed.net> - 4.2.2-1
- update to 4.2.2

* Sat Feb 13 2016 François Kooman <fkooman@tuxed.net> - 4.2.1-1
- update to 4.2.1

* Wed Feb 10 2016 François Kooman <fkooman@tuxed.net> - 4.2.0-1
- update to 4.2.0

* Wed Feb 03 2016 François Kooman <fkooman@tuxed.net> - 4.1.0-1
- update to 4.1.0
- update easy-rsa version dependency >= 3.0.0

* Thu Jan 21 2016 François Kooman <fkooman@tuxed.net> - 4.0.4-1
- update to 4.0.4

* Thu Jan 14 2016 François Kooman <fkooman@tuxed.net> - 4.0.3-1
- update to 4.0.3

* Wed Jan 13 2016 François Kooman <fkooman@tuxed.net> - 4.0.2-2
- require Monolog

* Wed Jan 13 2016 François Kooman <fkooman@tuxed.net> - 4.0.2-1
- update to 4.0.2

* Tue Jan 05 2016 François Kooman <fkooman@tuxed.net> - 4.0.1-1
- update to 4.0.1

* Tue Jan 05 2016 François Kooman <fkooman@tuxed.net> - 4.0.0-1
- update to 4.0.0

* Wed Dec 23 2015 François Kooman <fkooman@tuxed.net> - 3.0.4-1
- update to 3.0.4

* Mon Dec 21 2015 François Kooman <fkooman@tuxed.net> - 3.0.3-1
- update to 3.0.3

* Wed Dec 16 2015 François Kooman <fkooman@tuxed.net> - 3.0.2-1
- update to 3.0.2

* Fri Dec 11 2015 François Kooman <fkooman@tuxed.net> - 3.0.1-1
- update to 3.0.1

* Fri Dec 11 2015 François Kooman <fkooman@tuxed.net> - 3.0.0-2
- fix autoloader

* Fri Dec 11 2015 François Kooman <fkooman@tuxed.net> - 3.0.0-1
- update to 3.0.0

* Sun Nov 29 2015 François Kooman <fkooman@tuxed.net> - 2.0.0-1
- update to 2.0.0

* Tue Sep 22 2015 François Kooman <fkooman@tuxed.net> - 1.0.3-2
- fix the path in bin scripts
- update tag

* Tue Sep 22 2015 François Kooman <fkooman@tuxed.net> - 1.0.3-1
- update to 1.0.3

* Mon Sep 21 2015 François Kooman <fkooman@tuxed.net> - 1.0.2-3
- fix autoloader path

* Mon Sep 21 2015 François Kooman <fkooman@tuxed.net> - 1.0.2-2
- use new style autoloader, major rework on spec

* Mon Aug 10 2015 François Kooman <fkooman@tuxed.net> - 1.0.2-1
- update to 1.0.2

* Mon Aug 10 2015 François Kooman <fkooman@tuxed.net> - 1.0.1-1
- update to 1.0.1

* Mon Jul 20 2015 François Kooman <fkooman@tuxed.net> - 1.0.0-1
- initial release
