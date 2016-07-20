%global composer_vendor         fkooman
%global composer_project        vpn-server-api
%global composer_namespace      %{composer_vendor}/VPN/Server

%global github_owner            eduvpn
%global github_name             vpn-server-api
%global github_commit           1fcd2c17a10d273cec46fd104cda4c4cf489528f
%global github_short            %(c=%{github_commit}; echo ${c:0:7})
%if 0%{?rhel} == 5
%global with_tests              0%{?_with_tests:1}
%else
%global with_tests              0%{!?_without_tests:1}
%endif

Name:       vpn-server-api
Version:    8.2.2
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
BuildRequires:  php-composer(fkooman/io) >= 2.0.0
BuildRequires:  php-composer(fkooman/io) < 3.0.0
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
Requires:   php-composer(fkooman/io) >= 2.0.0
Requires:   php-composer(fkooman/io) < 3.0.0
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
cp -p config/acl.yaml.example ${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/acl.yaml
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
%config(noreplace) %attr(0440,openvpn,apache) %{_sysconfdir}/%{name}/acl.yaml
%{_bindir}/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/src
%{_datadir}/%{name}/web
%{_datadir}/%{name}/config
%dir %attr(0711,apache,apache) %{_localstatedir}/lib/%{name}
%doc README.md CHANGES.md composer.json config/config.yaml.example config/pools.yaml.example config/acl.yaml.example config/log.yaml.example
%license COPYING

%changelog
* Wed Jul 20 2016 François Kooman <fkooman@tuxed.net> - 8.2.2-1
- update to 8.2.2

* Fri Jul 15 2016 François Kooman <fkooman@tuxed.net> - 8.2.1-1
- update to 8.2.1
