%global composer_vendor         SURFnet
%global composer_project        vpn-server-node
%global composer_namespace      %{composer_vendor}/VPN/Node

%global github_owner            eduvpn
%global github_name             vpn-server-node
%global github_commit           5e2dccbbe2e59d2f905b1f0f1d35e79074d3ca1f
%global github_short            %(c=%{github_commit}; echo ${c:0:7})
%if 0%{?rhel} == 5
%global with_tests              0%{?_with_tests:1}
%else
%global with_tests              0%{!?_without_tests:1}
%endif

Name:       vpn-server-node
Version:    1.0.0
Release:    0.1%{?dist}
Summary:    OpenVPN node controller

Group:      Applications/Internet
License:    AGPLv3+

URL:        https://github.com/%{github_owner}/%{github_name}
Source0:    %{url}/archive/%{github_commit}/%{name}-%{version}-%{github_short}.tar.gz
Source1:    %{name}-autoload.php

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
BuildRequires:  php-composer(symfony/class-loader)
%endif

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
Requires:   php-composer(eduvpn/common)
Requires:   php-composer(psr/log)
Requires:   php-composer(symfony/class-loader)

Requires(post): policycoreutils-python
Requires(postun): policycoreutils-python

%description
OpenVPN node controller.

%prep
%setup -qn %{github_name}-%{github_commit} 
cp %{SOURCE1} src/%{composer_namespace}/autoload.php

sed -i "s|require_once sprintf('%s/vendor/autoload.php', dirname(__DIR__));|require_once '%{_datadir}/%{name}/src/%{composer_namespace}/autoload.php';|" bin/*
sed -i "s|dirname(__DIR__)|'%{_datadir}/%{name}'|" bin/*

%build

%install

# Application
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/%{name}
cp -pr src ${RPM_BUILD_ROOT}%{_datadir}/%{name}

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

%if %{with_tests} 
%check
%{_bindir}/phpab --output tests/bootstrap.php tests
echo 'require "%{buildroot}%{_datadir}/%{name}/src/%{composer_namespace}/autoload.php";' >> tests/bootstrap.php
%{_bindir}/phpunit \
    --bootstrap tests/bootstrap.php
%endif

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/%{name}/dh.pem
%dir %attr(0750,root,openvpn) %{_sysconfdir}/%{name}
%{_sbindir}/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/src
%{_datadir}/%{name}/config
%{_datadir}/%{name}/openvpn-config
%doc README.md composer.json config/config.yaml.example config/firewall.yaml.example
%license LICENSE

%changelog
* Mon Oct 17 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.1
- initial package
