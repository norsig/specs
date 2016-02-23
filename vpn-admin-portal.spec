%global composer_vendor         fkooman
%global composer_project        vpn-admin-portal
%global composer_namespace      %{composer_vendor}/VPN/AdminPortal

%global github_owner            eduVPN
%global github_name             vpn-admin-portal
%global github_commit           a54d04679a9eb56e2e13b4bfab809a1f33f5ffef
%global github_short            %(c=%{github_commit}; echo ${c:0:7})

Name:       vpn-admin-portal
Version:    3.3.2
Release:    1%{?dist}
Summary:    VPN Admin Portal

Group:      Applications/Internet
License:    ASL-2.0

URL:        https://github.com/%{github_owner}/%{github_name}
Source0:    %{url}/archive/%{github_commit}/%{name}-%{version}-%{github_short}.tar.gz
Source1:    %{name}-autoload.php
Source2:    %{name}-httpd.conf

BuildArch:  noarch
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 

Requires:   httpd
Requires:   php(language) >= 5.4
Requires:   php-date
Requires:   php-spl
Requires:   php-composer(fkooman/config) >= 1.0.0
Requires:   php-composer(fkooman/config) < 2.0.0
Requires:   php-composer(fkooman/http) >= 1.0.0
Requires:   php-composer(fkooman/http) < 2.0.0
Requires:   php-composer(fkooman/rest) >= 1.0.0
Requires:   php-composer(fkooman/rest) < 2.0.0
Requires:   php-composer(fkooman/rest-plugin-authentication) >= 2.0.0
Requires:   php-composer(fkooman/rest-plugin-authentication) < 3.0.0
Requires:   php-composer(fkooman/rest-plugin-authentication-form) >= 3.0.1
Requires:   php-composer(fkooman/rest-plugin-authentication-form) < 4.0.0
Requires:   php-composer(fkooman/rest-plugin-authentication-mellon) >= 2.0.0
Requires:   php-composer(fkooman/rest-plugin-authentication-mellon) < 3.0.0
Requires:   php-composer(fkooman/tpl-twig) >= 1.2.0
Requires:   php-composer(fkooman/tpl-twig) < 2.0.0
Requires:   php-composer(guzzlehttp/guzzle) >= 5.3
Requires:   php-composer(guzzlehttp/guzzle) < 6.0
Requires:   php-pear(pear.twig-project.org/Twig) >= 1.18
Requires:   php-pear(pear.twig-project.org/Twig) < 2.0
Requires:   php-composer(symfony/class-loader)

%description
Manage OpenVPN connections and configurations. Connects to vpn-user-portal 
and vpn-server-api.

%prep
%setup -qn %{github_name}-%{github_commit} 
cp %{SOURCE1} src/%{composer_namespace}/autoload.php

sed -i "s|require_once dirname(__DIR__).'/vendor/autoload.php';|require_once '%{_datadir}/%{name}/src/%{composer_namespace}/autoload.php';|" web/*.php

%build

%install
# Apache configuration
install -m 0644 -D -p %{SOURCE2} ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf.d/%{name}.conf

# Application
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/%{name}
cp -pr web views src ${RPM_BUILD_ROOT}%{_datadir}/%{name}

# Config
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}
cp -p config/config.yaml.example ${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/config.yaml
ln -s ../../../etc/%{name} ${RPM_BUILD_ROOT}%{_datadir}/%{name}/config

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%dir %attr(-,apache,apache) %{_sysconfdir}/%{name}
%config(noreplace) %attr(0600,apache,apache) %{_sysconfdir}/%{name}/config.yaml
%{_datadir}/%{name}/src
%{_datadir}/%{name}/web
%{_datadir}/%{name}/views
%{_datadir}/%{name}/config
%doc README.md CHANGES.md composer.json config/config.yaml.example
%license COPYING

%changelog
* Tue Feb 23 2016 François Kooman <fkooman@tuxed.net> - 3.3.2-1
- update to 3.3.2

* Sat Feb 20 2016 François Kooman <fkooman@tuxed.net> - 3.3.1-1
- update to 3.3.1

* Thu Feb 18 2016 François Kooman <fkooman@tuxed.net> - 3.3.0-1
- update to 3.3.0

* Mon Feb 15 2016 François Kooman <fkooman@tuxed.net> - 3.2.0-2
- update commit

* Mon Feb 15 2016 François Kooman <fkooman@tuxed.net> - 3.2.0-1
- update to 3.2.0

* Wed Feb 03 2016 François Kooman <fkooman@tuxed.net> - 3.1.3-1
- update to 3.1.3

* Wed Jan 27 2016 François Kooman <fkooman@tuxed.net> - 3.1.2-1
- update to 3.1.2

* Wed Jan 20 2016 François Kooman <fkooman@tuxed.net> - 3.1.1-1
- update to 3.1.1

* Mon Jan 18 2016 François Kooman <fkooman@tuxed.net> - 3.1.0-1
- update to 3.1.0

* Wed Jan 13 2016 François Kooman <fkooman@tuxed.net> - 3.0.5-1
- update to 3.0.5

* Wed Jan 13 2016 François Kooman <fkooman@tuxed.net> - 3.0.4-1
- update to 3.0.4

* Tue Jan 12 2016 François Kooman <fkooman@tuxed.net> - 3.0.3-1
- update to 3.0.3

* Tue Jan 12 2016 François Kooman <fkooman@tuxed.net> - 3.0.2-1
- update to 3.0.2

* Sat Jan 09 2016 François Kooman <fkooman@tuxed.net> - 3.0.1-1
- update to 3.0.1

* Tue Jan 05 2016 François Kooman <fkooman@tuxed.net> - 3.0.0-1
- update to 3.0.0

* Tue Dec 22 2015 François Kooman <fkooman@tuxed.net> - 2.1.0-1
- update to 2.1.0

* Mon Dec 21 2015 François Kooman <fkooman@tuxed.net> - 2.0.4-1
- update to 2.0.4

* Thu Dec 17 2015 François Kooman <fkooman@tuxed.net> - 2.0.3-1
- update to 2.0.3

* Thu Dec 17 2015 François Kooman <fkooman@tuxed.net> - 2.0.2-1
- update to 2.0.2

* Thu Dec 17 2015 François Kooman <fkooman@tuxed.net> - 2.0.1-1
- update to 2.0.1

* Wed Dec 16 2015 François Kooman <fkooman@tuxed.net> - 2.0.0-1
- update to 2.0.0

* Tue Dec 15 2015 François Kooman <fkooman@tuxed.net> - 1.0.3-1
- update to 1.0.3

* Mon Dec 14 2015 François Kooman <fkooman@tuxed.net> - 1.0.2-1
- update to 1.0.2

* Fri Dec 11 2015 François Kooman <fkooman@tuxed.net> - 1.0.1-2
- fix autoloader

* Fri Dec 11 2015 François Kooman <fkooman@tuxed.net> - 1.0.1-1
- update to 1.0.1

* Fri Dec 11 2015 François Kooman <fkooman@tuxed.net> - 1.0.0-1
- initial release
