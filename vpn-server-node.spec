%global composer_vendor         SURFnet
%global composer_project        vpn-server-node
%global composer_namespace      %{composer_vendor}/VPN/Node

%global github_owner            eduvpn
%global github_name             vpn-server-node
%global github_commit           4daf00ecd921ebaeb0513fb3ba7e5d5f995a76b5
%global github_short            %(c=%{github_commit}; echo ${c:0:7})

Name:       vpn-server-node
Version:    1.0.0
Release:    0.30%{?dist}
Summary:    OpenVPN node controller

Group:      Applications/Internet
License:    AGPLv3+

URL:        https://github.com/%{github_owner}/%{github_name}
Source0:    %{url}/archive/%{github_commit}/%{name}-%{version}-%{github_short}.tar.gz

BuildArch:  noarch
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 

BuildRequires:  %{_bindir}/phpunit
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
BuildRequires:  vpn-lib-common
BuildRequires:  php-composer(fedora/autoloader)
BuildRequires:  php-composer(psr/log)

Requires:   openvpn
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
Requires:   vpn-lib-common
Requires:   php-composer(fedora/autoloader)
Requires:   php-composer(psr/log)

Requires(post): policycoreutils-python
Requires(postun): policycoreutils-python

%description
OpenVPN node controller.

%prep
%setup -qn %{github_name}-%{github_commit} 

sed -i "s|require_once sprintf('%s/vendor/autoload.php', dirname(__DIR__));|require_once '%{_datadir}/%{name}/src/%{composer_namespace}/autoload.php';|" bin/* libexec/*
sed -i "s|dirname(__DIR__)|'%{_datadir}/%{name}'|" bin/* libexec/*

%build
cat <<'AUTOLOAD' | tee src/autoload.php
<?php
require_once '%{_datadir}/php/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('SURFnet\\VPN\\Node\\', __DIR__);
\Fedora\Autoloader\Dependencies::required(array(
    '%{_datadir}/php/Psr/Log/autoload.php',
    '%{_datadir}/vpn-lib-common/SURFnet/VPN/Common/autoload.php',
));
AUTOLOAD

%install
# Application
mkdir -p %{buildroot}%{_datadir}/%{name}/src/%{composer_namespace}
cp -pr src/* %{buildroot}%{_datadir}/%{name}/src/%{composer_namespace}

mkdir -p %{buildroot}%{_bindir}
cp -pr bin/* %{buildroot}%{_bindir}

mkdir -p %{buildroot}%{_libexecdir}
cp -pr libexec/* %{buildroot}%{_libexecdir}

# Config
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
cp -pr config/dh.pem %{buildroot}%{_sysconfdir}/%{name}
cp -pr config/firewall.yaml.example %{buildroot}%{_sysconfdir}/%{name}/firewall.yaml
mkdir -p %{buildroot}%{_sysconfdir}/%{name}/default
cp -pr config/config.yaml.example %{buildroot}%{_sysconfdir}/%{name}/default/config.yaml

ln -s ../../../etc/%{name} %{buildroot}%{_datadir}/%{name}/config
ln -s ../../../etc/openvpn %{buildroot}%{_datadir}/%{name}/openvpn-config

%check
phpunit --bootstrap=%{buildroot}/%{_datadir}/%{name}/src/%{composer_namespace}/autoload.php

%files
%defattr(-,root,root,-)
%dir %attr(0750,root,openvpn) %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/dh.pem
%config(noreplace) %{_sysconfdir}/%{name}/firewall.yaml
%dir %attr(0750,root,openvpn) %{_sysconfdir}/%{name}/default
%config(noreplace) %{_sysconfdir}/%{name}/default/config.yaml
%{_bindir}/*
%{_libexecdir}/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/src
%{_datadir}/%{name}/config
%{_datadir}/%{name}/openvpn-config
%doc README.md composer.json config/config.yaml.example config/firewall.yaml.example config/dh.pem
%license LICENSE

%changelog
* Fri Nov 25 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.30
- rebuilt

* Tue Nov 22 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.29
- rebuilt

* Sun Nov 20 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.28
- rebuilt

* Fri Nov 18 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.27
- rebuilt

* Fri Nov 18 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.26
- rebuilt

* Thu Nov 17 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.25
- rebuilt

* Wed Nov 16 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.24
- rebuilt

* Tue Nov 15 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.23
- rebuilt

* Tue Nov 15 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.22
- rebuilt

* Mon Nov 14 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.21
- rebuilt

* Mon Nov 14 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.20
- rebuilt

* Sun Nov 13 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.19
- rebuilt

* Fri Nov 11 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.18
- rebuilt

* Wed Nov 09 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.17
- rebuilt

* Wed Nov 09 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.16
- rebuilt
