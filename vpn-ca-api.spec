%global composer_vendor         SURFnet
%global composer_project        vpn-ca-api
%global composer_namespace      %{composer_vendor}/VPN/CA

%global github_owner            eduvpn
%global github_name             vpn-ca-api
%global github_commit           02fd750ee734fc4e1082bd094d426ff31c06030a
%global github_short            %(c=%{github_commit}; echo ${c:0:7})

Name:       vpn-ca-api
Version:    6.0.0
Release:    0.31%{?dist}
Summary:    Web service to manage VPN CAs

Group:      Applications/Internet
License:    AGPLv3+

URL:        https://github.com/%{github_owner}/%{github_name}
Source0:    %{url}/archive/%{github_commit}/%{name}-%{version}-%{github_short}.tar.gz
Source1:    %{name}-httpd.conf

BuildArch:  noarch
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 

BuildRequires:  php(language) >= 5.4.0
BuildRequires:  php-date
BuildRequires:  php-json
BuildRequires:  php-openssl
BuildRequires:  php-mbstring
BuildRequires:  php-pcre
BuildRequires:  php-spl
BuildRequires:  vpn-lib-common
BuildRequires:  php-composer(psr/log)
BuildRequires:  php-composer(fedora/autoloader)
BuildRequires:  %{_bindir}/phpunit

Requires:   httpd
Requires:   openvpn
Requires:   openssl

Requires:   php(language) >= 5.4.0
Requires:   php-date
Requires:   php-json
Requires:   php-mbstring
Requires:   php-openssl
Requires:   php-pcre
Requires:   php-spl
Requires:   vpn-lib-common
Requires:   php-composer(fedora/autoloader)
Requires:   php-composer(psr/log)

Requires(post): /usr/sbin/semanage
Requires(postun): /usr/sbin/semanage

%if 0%{?fedora} >= 24
Requires:   easy-rsa
%else
Provides:   bundled(easy-rsa) = 3.0.1
%endif

%description
VPN CA API.

%prep
%setup -qn %{github_name}-%{github_commit} 

sed -i "s|require_once sprintf('%s/vendor/autoload.php', dirname(__DIR__));|require_once '%{_datadir}/%{name}/src/%{composer_namespace}/autoload.php';|" bin/* web/*.php
sed -i "s|dirname(__DIR__)|'%{_datadir}/%{name}'|" bin/*

%if 0%{?fedora} >= 24
rm -rf easy-rsa
%endif

%build
cat <<'AUTOLOAD' | tee src/autoload.php
<?php
require_once '%{_datadir}/php/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('SURFnet\\VPN\\CA\\', __DIR__);
\Fedora\Autoloader\Dependencies::required(array(
    '%{_datadir}/php/Psr/Log/autoload.php',
    '%{_datadir}/php/SURFnet/VPN/Common/autoload.php',
));
AUTOLOAD

%install
# Apache configuration
install -m 0644 -D -p %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf

# Application
mkdir -p %{buildroot}%{_datadir}/%{name}
cp -pr web %{buildroot}%{_datadir}/%{name}
mkdir -p %{buildroot}%{_datadir}/%{name}/src/%{composer_namespace}
cp -pr src/* %{buildroot}%{_datadir}/%{name}/src/%{composer_namespace}

mkdir -p %{buildroot}%{_bindir}
cp -pr bin/* %{buildroot}%{_bindir}

# Config
mkdir -p %{buildroot}%{_sysconfdir}/%{name}/default
cp -pr config/config.yaml.example %{buildroot}%{_sysconfdir}/%{name}/default/config.yaml
ln -s ../../../etc/%{name} %{buildroot}%{_datadir}/%{name}/config

# Data
mkdir -p %{buildroot}%{_localstatedir}/lib/%{name}
ln -s ../../../var/lib/%{name} %{buildroot}%{_datadir}/%{name}/data

# Easy RSA
%if 0%{?fedora} >= 24
ln -s ../../../usr/share/easy-rsa/3 %{buildroot}%{_datadir}/%{name}/easy-rsa
%else 
cp -pr easy-rsa %{buildroot}%{_datadir}/%{name}
%endif 

%check
phpunit --bootstrap=%{buildroot}/%{_datadir}/%{name}/src/%{composer_namespace}/autoload.php

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
%dir %attr(0750,root,apache) %{_sysconfdir}/%{name}
%dir %attr(0750,root,apache) %{_sysconfdir}/%{name}/default
%config(noreplace) %{_sysconfdir}/%{name}/default/config.yaml
%{_bindir}/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/src
%{_datadir}/%{name}/web
%{_datadir}/%{name}/easy-rsa
%{_datadir}/%{name}/config
%{_datadir}/%{name}/data
%dir %attr(0700,apache,apache) %{_localstatedir}/lib/%{name}
%doc README.md composer.json config/config.yaml.example
%license LICENSE

%changelog
* Sun Nov 27 2016 François Kooman <fkooman@tuxed.net> - 6.0.0-0.31
- rebuilt

* Sun Nov 27 2016 François Kooman <fkooman@tuxed.net> - 6.0.0-0.30
- rebuilt

* Thu Nov 24 2016 François Kooman <fkooman@tuxed.net> - 6.0.0-0.29
- rebuilt

* Thu Nov 24 2016 François Kooman <fkooman@tuxed.net> - 6.0.0-0.28
- rebuilt

* Tue Nov 22 2016 François Kooman <fkooman@tuxed.net> - 6.0.0-0.27
- rebuilt

* Wed Nov 16 2016 François Kooman <fkooman@tuxed.net> - 6.0.0-0.26
- rebuilt

* Tue Nov 15 2016 François Kooman <fkooman@tuxed.net> - 6.0.0-0.25
- rebuilt

* Tue Nov 15 2016 François Kooman <fkooman@tuxed.net> - 6.0.0-0.24
- rebuilt

* Tue Nov 15 2016 François Kooman <fkooman@tuxed.net> - 6.0.0-0.23
- rebuilt

* Tue Nov 15 2016 François Kooman <fkooman@tuxed.net> - 6.0.0-0.22
- rebuilt

* Sun Nov 13 2016 François Kooman <fkooman@tuxed.net> - 6.0.0-0.21
- rebuilt

* Sun Nov 13 2016 François Kooman <fkooman@tuxed.net> - 6.0.0-0.20
- rebuilt

* Wed Nov 09 2016 François Kooman <fkooman@tuxed.net> - 6.0.0-0.19
- rebuilt

* Wed Nov 09 2016 François Kooman <fkooman@tuxed.net> - 6.0.0-0.18
- rebuilt
