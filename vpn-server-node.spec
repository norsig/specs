%global composer_vendor         SURFnet
%global composer_project        vpn-server-node
%global composer_namespace      %{composer_vendor}/VPN/Node

%global github_owner            eduvpn
%global github_name             vpn-server-node
%global github_commit           f19e95a2e82d5fc514490c8fccf051fb877532f8
%global github_short            %(c=%{github_commit}; echo ${c:0:7})

Name:       vpn-server-node
Version:    1.0.0
Release:    0.16%{?dist}
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
BuildRequires:  php-composer(fedora/autoloader)
BuildRequires:  php-composer(eduvpn/common)
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
Requires:   php-composer(fedora/autoloader)
Requires:   php-composer(eduvpn/common)
Requires:   php-composer(psr/log)

Requires(post): policycoreutils-python
Requires(postun): policycoreutils-python

%description
OpenVPN node controller.

%prep
%setup -qn %{github_name}-%{github_commit} 

sed -i "s|require_once sprintf('%s/vendor/autoload.php', dirname(__DIR__));|require_once '%{_datadir}/%{name}/src/%{composer_namespace}/autoload.php';|" bin/*
sed -i "s|dirname(__DIR__)|'%{_datadir}/%{name}'|" bin/*

%build
cat <<'AUTOLOAD' | tee src/autoload.php
<?php
require_once '%{_datadir}/php/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('SURFnet\\VPN\\Node\\', __DIR__);
\Fedora\Autoloader\Dependencies::required(array(
    '%{_datadir}/php/Psr/Log/autoload.php',
    '%{_datadir}/php/SURFnet/VPN/Common/autoload.php',
));
AUTOLOAD
%install

# Application
mkdir -p %{buildroot}%{_datadir}/%{name}/src/%{composer_namespace}
cp -pr src/* %{buildroot}%{_datadir}/%{name}/src/%{composer_namespace}

mkdir -p %{buildroot}%{_sbindir}
(
cd bin
for f in `ls *`
do
    bf=`basename ${f} .php`
    cp -pr ${f} %{buildroot}%{_sbindir}/%{name}-${bf}
    chmod 0755 %{buildroot}%{_sbindir}/%{name}-${bf}
done
)

# Config
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
cp config/dh.pem %{buildroot}%{_sysconfdir}/%{name}
ln -s ../../../etc/%{name} %{buildroot}%{_datadir}/%{name}/config
ln -s ../../../etc/openvpn %{buildroot}%{_datadir}/%{name}/openvpn-config

%check
phpunit --bootstrap=%{buildroot}/%{_datadir}/%{name}/src/%{composer_namespace}/autoload.php

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/%{name}/dh.pem
%dir %attr(0750,root,openvpn) %{_sysconfdir}/%{name}
%{_sbindir}/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/src
%{_datadir}/%{name}/config
%{_datadir}/%{name}/openvpn-config
%doc README.md composer.json config/config.yaml.example config/firewall.yaml.example config/dh.pem
%license LICENSE

%changelog
* Wed Nov 09 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.16
- rebuilt
