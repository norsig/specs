%global composer_vendor         SURFnet
%global composer_project        vpn-server-api
%global composer_namespace      %{composer_vendor}/VPN/Server

%global github_owner            eduvpn
%global github_name             vpn-server-api
%global github_commit           2b11e840608a1ace86e0d6c3e690a7857caefd54
%global github_short            %(c=%{github_commit}; echo ${c:0:7})

Name:       vpn-server-api
Version:    1.0.0
Release:    0.35%{?dist}
Summary:    Web service to control OpenVPN processes

Group:      Applications/Internet
License:    AGPLv3+

URL:        https://github.com/%{github_owner}/%{github_name}
Source0:    %{url}/archive/%{github_commit}/%{name}-%{version}-%{github_short}.tar.gz
Source1:    %{name}-httpd.conf
Source2:    %{name}.cron
BuildArch:  noarch
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 

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
BuildRequires:  %{_bindir}/phpunit
BuildRequires:  vpn-lib-common
BuildRequires:  php-composer(fedora/autoloader)
BuildRequires:  php-composer(psr/log)
BuildRequires:  php-composer(christian-riesen/otp)
BuildRequires:  php-composer(guzzlehttp/guzzle) >= 5.3.0
BuildRequires:  php-composer(guzzlehttp/guzzle) < 6.0.0

Requires:   crontabs
Requires:   openvpn
Requires:   httpd
Requires:   openssl

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
Requires:   php-composer(christian-riesen/otp)
Requires:   php-composer(guzzlehttp/guzzle) >= 5.3.0
Requires:   php-composer(guzzlehttp/guzzle) < 6.0.0

Requires(post): /usr/sbin/semanage
Requires(postun): /usr/sbin/semanage

%if 0%{?fedora} >= 24
Requires:   easy-rsa
%else
Provides:   bundled(easy-rsa) = 3.0.1
%endif

%description
VPN Server API.

%prep
%setup -qn %{github_name}-%{github_commit} 

sed -i "s|require_once sprintf('%s/vendor/autoload.php', dirname(__DIR__));|require_once '%{_datadir}/%{name}/src/%{composer_namespace}/autoload.php';|" bin/*
sed -i "s|require_once sprintf('%s/vendor/autoload.php', dirname(__DIR__));|require_once '%{_datadir}/%{name}/src/%{composer_namespace}/autoload.php';|" web/*.php
sed -i "s|dirname(__DIR__)|'%{_datadir}/%{name}'|" bin/*

%if 0%{?fedora} >= 24
rm -rf easy-rsa
%endif

%build
cat <<'AUTOLOAD' | tee src/autoload.php
<?php
require_once '%{_datadir}/php/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('SURFnet\\VPN\\Server\\', __DIR__);
\Fedora\Autoloader\Dependencies::required(array(
    '%{_datadir}/php/Otp/autoload.php',
    '%{_datadir}/php/Psr/Log/autoload.php',
    '%{_datadir}/php/GuzzleHttp/autoload.php',
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
(
cd bin
for phpFileName in $(ls *)
do
    binFileName=$(basename ${phpFileName} .php)
    cp -pr ${phpFileName} %{buildroot}%{_bindir}/%{name}-${binFileName}
    chmod 0755 %{buildroot}%{_bindir}/%{name}-${binFileName}
done
)

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

# Cron
mkdir -p %{buildroot}%{_sysconfdir}/cron.d
%{__install} -p -D -m 0640 %{SOURCE2} %{buildroot}%{_sysconfdir}/cron.d/%{name}

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
%config(noreplace) %{_sysconfdir}/cron.d/%{name}
%{_bindir}/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/src
%{_datadir}/%{name}/web
%{_datadir}/%{name}/easy-rsa
%{_datadir}/%{name}/config
%{_datadir}/%{name}/data
%dir %attr(0700,apache,apache) %{_localstatedir}/lib/%{name}
%doc README.md composer.json config/config.yaml.example CHANGES.md
%license LICENSE

%changelog
* Thu Dec 15 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.35
- rebuilt

* Thu Dec 15 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.34
- rebuilt

* Tue Dec 13 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.33
- rebuilt

* Tue Dec 13 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.32
- rebuilt

* Tue Dec 13 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.31
- rebuilt

* Tue Dec 13 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.30
- rebuilt

* Tue Dec 13 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.29
- rebuilt

* Mon Dec 12 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.28
- rebuilt

* Mon Dec 12 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.27
- rebuilt

* Wed Dec 07 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.26
- rebuilt

* Tue Dec 06 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.25
- rebuilt

* Tue Dec 06 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.24
- rebuilt

* Tue Dec 06 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.23
- rebuilt

* Tue Dec 06 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.22
- rebuilt

* Tue Dec 06 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.21
- rebuilt

* Mon Dec 05 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.20
- rebuilt

* Mon Dec 05 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.19
- rebuilt

* Mon Dec 05 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.18
- rebuilt

* Sun Dec 04 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.17
- rebuilt

* Sun Dec 04 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.16
- rebuilt

* Sun Dec 04 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.15
- rebuilt

* Sun Dec 04 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.14
- rebuilt

* Sat Dec 03 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.13
- rebuilt

* Sat Dec 03 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.12
- rebuilt

* Sat Dec 03 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.11
- rebuilt

* Fri Dec 02 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.10
- rebuilt

* Fri Dec 02 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.9
- rebuilt

* Fri Dec 02 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.8
- rebuilt

* Thu Dec 01 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.7
- rebuilt

* Thu Dec 01 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.6
- rebuilt

* Thu Dec 01 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.5
- rebuilt

* Thu Dec 01 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.4
- rebuilt

* Thu Dec 01 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.3
- rebuilt

* Thu Dec 01 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.2
- rebuilt

* Thu Dec 01 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.1
- rebuilt
