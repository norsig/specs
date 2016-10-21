%global composer_vendor         eduvpn
%global composer_project        vpn-admin-portal
%global composer_namespace      SURFnet/VPN/Admin

%global github_owner            eduvpn
%global github_name             vpn-admin-portal
%global github_commit           cec398c0a07f7b73e90c2581ad80568e283b4027
%global github_short            %(c=%{github_commit}; echo ${c:0:7})
%if 0%{?rhel} == 5
%global with_tests              0%{?_with_tests:1}
%else
%global with_tests              0%{!?_without_tests:1}
%endif

Name:       vpn-admin-portal
Version:    10.0.0
Release:    0.25%{?dist}
Summary:    VPN Admin Portal

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
BuildRequires:  php-spl
BuildRequires:  php-composer(eduvpn/common)
BuildRequires:  php-composer(twig/twig)
BuildRequires:  php-composer(guzzlehttp/guzzle) >= 5.3.0
BuildRequires:  php-composer(guzzlehttp/guzzle) < 6.0.0
BuildRequires:  php-composer(symfony/class-loader)
%endif

Requires:   httpd
Requires:   php(language) >= 5.4.0
Requires:   php-date
Requires:   php-spl
Requires:   php-composer(eduvpn/common)
Requires:   php-composer(twig/twig)
Requires:   php-composer(guzzlehttp/guzzle) >= 5.3.0
Requires:   php-composer(guzzlehttp/guzzle) < 6.0.0
Requires:   php-composer(symfony/class-loader)

%description
VPN Admin Portal.

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
cp -pr web views src ${RPM_BUILD_ROOT}%{_datadir}/%{name}

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
%{_datadir}/%{name}/src
%{_datadir}/%{name}/web
%{_datadir}/%{name}/data
%{_datadir}/%{name}/views
%{_datadir}/%{name}/config
%dir %attr(0700,apache,apache) %{_localstatedir}/lib/%{name}
%doc README.md CHANGES.md composer.json config/config.yaml.example
%license LICENSE

%changelog
* Fri Oct 21 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.25
- rebuilt

* Fri Oct 21 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.24
- rebuilt

* Thu Oct 20 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.23
- rebuilt

* Tue Oct 18 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.22
- rebuilt

* Mon Oct 17 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.21
- rebuilt

* Fri Oct 14 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.20
- rebuilt

* Thu Oct 13 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.19
- rebuilt

* Wed Oct 12 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.18
- rebuilt

* Tue Oct 11 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.17
- rebuilt

* Fri Oct 07 2016 François <fkooman@tuxed.net> - 10.0.0-0.16
- rebuilt

* Fri Oct 07 2016 François <fkooman@tuxed.net> - 10.0.0-0.15
- rebuilt

* Fri Oct 07 2016 François <fkooman@tuxed.net> - 10.0.0-0.14
- rebuilt

* Thu Oct 06 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.13
- update to 2d1ef2490d01086a63ebcb46dba96d6910d63a81

* Thu Oct 06 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.12
- update to 21d77fb19e4b7bd5912fe743b3fe26e50aafb5ed

* Tue Oct 04 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.11
- update to 2672290ccda5bcf984c6460d88c2311856300e1c

* Sun Oct 02 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.10
- rebuilt

* Fri Sep 30 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.9
- update to bd436f545217b773659866b0f00be070b8125ed8
- fix bin scripts

* Thu Sep 29 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.8
- update to 7bb628dc9366b7c70b9a645b346795cdb5c1db52

* Wed Sep 28 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.7
- update to 51d9dd7d746fc02886126c63dc7437736b851383

* Tue Sep 27 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.6
- update to 9bc13f6ca3fe235095ebe5f7ca78d220ed9e42a4
- enable tests

* Mon Sep 26 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.5
- update to d57cd7168584c2932a6007af1299797b34ff638f

* Fri Sep 23 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.4
- fix data dir

* Fri Sep 23 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.3
- update to 19674d0fd23277d3705e8373fa90e16743ac4b0a

* Wed Sep 21 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.2
- update to 13503b2477dea9d21356d77adfbe248b3482b214

* Tue Sep 20 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.1
- update to 7502b4c61d830373b4bdbd13dd4ba4a0e64ea2e1
