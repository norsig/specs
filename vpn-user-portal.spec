%global composer_vendor         eduvpn
%global composer_project        vpn-user-portal
%global composer_namespace      SURFnet/VPN/Portal

%global github_owner            eduvpn
%global github_name             vpn-user-portal
%global github_commit           78fe9b9512b8582f3779f4cd2d316fa4e3ede4d5
%global github_short            %(c=%{github_commit}; echo ${c:0:7})
%if 0%{?rhel} == 5
%global with_tests              0%{?_with_tests:1}
%else
%global with_tests              0%{!?_without_tests:1}
%endif

Name:       vpn-user-portal
Version:    10.0.0
Release:    0.26%{?dist}
Summary:    VPN User Portal

Group:      Applications/Internet
License:    AGPLv3+

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
BuildRequires:  php-gettext
BuildRequires:  php-json
BuildRequires:  php-pcre
BuildRequires:  php-pdo
BuildRequires:  php-spl
BuildRequires:  php-composer(eduvpn/common)
BuildRequires:  php-composer(twig/twig)
BuildRequires:  php-composer(twig/extensions)
BuildRequires:  php-composer(bacon/bacon-qr-code)
BuildRequires:  php-composer(christian-riesen/otp)
BuildRequires:  php-composer(guzzlehttp/guzzle) >= 5.3.0
BuildRequires:  php-composer(guzzlehttp/guzzle) < 6.0.0
BuildRequires:  php-composer(fkooman/oauth2-client)
BuildRequires:  php-composer(symfony/class-loader)
%endif

Requires:   httpd
Requires:   php(language) >= 5.4.0
Requires:   php-date
Requires:   php-gettext
Requires:   php-json
Requires:   php-mbstring
Requires:   php-pcre
Requires:   php-pdo
Requires:   php-spl
Requires:   php-composer(eduvpn/common)
Requires:   php-composer(twig/twig)
Requires:   php-composer(twig/extensions)
Requires:   php-composer(bacon/bacon-qr-code)
Requires:   php-composer(christian-riesen/otp)
Requires:   php-composer(guzzlehttp/guzzle) >= 5.3.0
Requires:   php-composer(guzzlehttp/guzzle) < 6.0.0
Requires:   php-composer(fkooman/oauth2-client)
Requires:   php-composer(symfony/class-loader)

Requires(post): policycoreutils-python
Requires(postun): policycoreutils-python

%description
VPN User Portal.

%prep
%setup -qn %{github_name}-%{github_commit} 
cp %{SOURCE1} src/%{composer_namespace}/autoload.php

sed -i "s|require_once sprintf('%s/vendor/autoload.php', dirname(__DIR__));|require_once '%{_datadir}/%{name}/src/%{composer_namespace}/autoload.php';|" bin/*
sed -i "s|require_once sprintf('%s/vendor/autoload.php', dirname(__DIR__));|require_once '%{_datadir}/%{name}/src/%{composer_namespace}/autoload.php';|" web/*.php
sed -i "s|dirname(__DIR__)|'%{_datadir}/%{name}'|" bin/*

%build

%install
# Apache configuration
install -m 0644 -D -p %{SOURCE2} ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf.d/%{name}.conf

# Application
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/%{name}
cp -pr web views locale src ${RPM_BUILD_ROOT}%{_datadir}/%{name}

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
ln -s ../../../etc/%{name} ${RPM_BUILD_ROOT}%{_datadir}/%{name}/config

# Data
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/lib/%{name}
ln -s ../../../var/lib/%{name} ${RPM_BUILD_ROOT}%{_datadir}/%{name}/data

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

# remove template cache if it is there
rm -rf %{_localstatedir}/lib/%{name}/*/tpl/* >/dev/null 2>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then  # final removal
semanage fcontext -d -t httpd_sys_rw_content_t '%{_localstatedir}/lib/%{name}(/.*)?' 2>/dev/null || :
fi

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%dir %attr(0750,root,apache) %{_sysconfdir}/%{name}
%{_sbindir}/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/src
%{_datadir}/%{name}/data
%{_datadir}/%{name}/web
%{_datadir}/%{name}/views
%{_datadir}/%{name}/config
%{_datadir}/%{name}/locale
%dir %attr(0700,apache,apache) %{_localstatedir}/lib/%{name}
%doc README.md CHANGES.md composer.json config/config.yaml.example
%license LICENSE

%changelog
* Tue Oct 18 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.26
- rebuilt

* Tue Oct 18 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.25
- rebuilt

* Mon Oct 17 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.24
- rebuilt

* Fri Oct 14 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.23
- rebuilt

* Thu Oct 13 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.22
- rebuilt

* Wed Oct 12 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.21
- rebuilt

* Fri Oct 07 2016 François <fkooman@tuxed.net> - 10.0.0-0.20
- rebuilt

* Fri Oct 07 2016 François <fkooman@tuxed.net> - 10.0.0-0.19
- rebuilt

* Fri Oct 07 2016 François <fkooman@tuxed.net> - 10.0.0-0.18
- rebuilt

* Thu Oct 06 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.17
- update to bdf4f19a475b52264cfecfe26b450f6d92cb2dce

* Thu Oct 06 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.16
- update to 9c3267d827c82ca81bc5a1231e6a36624b4153b5

* Tue Oct 04 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.15
- update to 84ad26329dd28fad0e64185b5633acbec3ad7899

* Sun Oct 02 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.14
- rebuilt

* Fri Sep 30 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.13
- update to 3e4fd2be3a2e8dad0041da0c5c11b869e7dccc38
- fix bin scripts

* Fri Sep 30 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.12
- update to 0608dae0525527071a844db57d03bdf19523aacd

* Fri Sep 30 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.11
- update to cd7c90c00c593c56f128584e63dd0940cc82ca33

* Fri Sep 30 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.10
- update to bfd367e7946fc39108d92a4c7fedfb62727fbedf

* Thu Sep 29 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.9
- update to cd7e8b583326e7dc87e1bc1571144b89b19793a8

* Thu Sep 29 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.8
- update to caebb085a2c4e1cf25edbcc0944209aae4a9a47e

* Thu Sep 29 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.7
- update to 840f7dfe887e535570b85e7141a866c469f3b9fd

* Wed Sep 28 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.6
- update to f80249ee0442a849d7c44e30cbb5fdf63961c925

* Mon Sep 26 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.5
- update to 1ed11c976fa60ab94ee6547e3a387fa04df4c22f

* Fri Sep 23 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.4
- fix data dir

* Fri Sep 23 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.3
- update to 37e1ca0b0e118d581ab52d8ac98177a0ab254b62

* Fri Sep 23 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.2
- update to e0e145f88c96003eb15a6ef75f9e5b84e370b81c

* Wed Sep 21 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.1
- update to 521cf1e973842061b42d4c1dc47c0e68efcd0c1c

* Tue Aug 02 2016 François Kooman <fkooman@tuxed.net> - 9.4.4-1
- update to 9.4.4

* Wed Jul 27 2016 François Kooman <fkooman@tuxed.net> - 9.4.3-1
- update to 9.4.3

* Wed Jul 27 2016 François Kooman <fkooman@tuxed.net> - 9.4.2-1
- update to 9.4.2

* Tue Jul 26 2016 François Kooman <fkooman@tuxed.net> - 9.4.1-1
- update to 9.4.1

* Tue Jul 26 2016 François Kooman <fkooman@tuxed.net> - 9.4.0-1
- update to 9.4.0
