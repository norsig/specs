%global composer_vendor         SURFnet
%global composer_project        vpn-ca-api
%global composer_namespace      %{composer_vendor}/VPN/CA

%global github_owner            eduvpn
%global github_name             vpn-ca-api
%global github_commit           36b474de57ac390dee670dd33357d2876e136bbe
%global github_short            %(c=%{github_commit}; echo ${c:0:7})
%if 0%{?rhel} == 5
%global with_tests              0%{?_with_tests:1}
%else
%global with_tests              0%{!?_without_tests:1}
%endif

Name:       vpn-ca-api
Version:    6.0.0
Release:    0.10%{?dist}
Summary:    Web service to manage VPN CAs

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
BuildRequires:  php-json
BuildRequires:  php-openssl
BuildRequires:  php-mbstring
BuildRequires:  php-pcre
BuildRequires:  php-spl
BuildRequires:  php-composer(eduvpn/common)
BuildRequires:  php-composer(psr/log)
BuildRequires:  php-composer(symfony/class-loader)
%endif

Requires:   httpd
Requires:   easy-rsa
Requires:   openvpn

Requires:   php(language) >= 5.4.0
Requires:   php-date
Requires:   php-json
Requires:   php-mbstring
Requires:   php-openssl
Requires:   php-pcre
Requires:   php-spl
Requires:   php-composer(eduvpn/common)
Requires:   php-composer(psr/log)
Requires:   php-composer(symfony/class-loader)

Requires(post): policycoreutils-python
Requires(postun): policycoreutils-python

%description
VPN CA API.

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
cp -pr web src ${RPM_BUILD_ROOT}%{_datadir}/%{name}

mkdir -p ${RPM_BUILD_ROOT}%{_sbindir}
(
cd bin
for f in `ls *`
do
    bf=`basename ${f} .php`
    cp -pr ${f} ${RPM_BUILD_ROOT}%{_sbindir}/%{name}-${bf}
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

%postun
if [ $1 -eq 0 ] ; then  # final removal
semanage fcontext -d -t httpd_sys_rw_content_t '%{_localstatedir}/lib/%{name}(/.*)?' 2>/dev/null || :
fi

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%dir %attr(-,apache,apache) %{_sysconfdir}/%{name}
%{_sbindir}/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/src
%{_datadir}/%{name}/web
%{_datadir}/%{name}/config
%{_datadir}/%{name}/data
%dir %attr(0700,apache,apache) %{_localstatedir}/lib/%{name}
%doc README.md composer.json config/config.yaml.example
%license LICENSE

%changelog
* Fri Sep 30 2016 François Kooman <fkooman@tuxed.net> - 6.0.0-0.10
- update to 36b474de57ac390dee670dd33357d2876e136bbe
- fix bin scripts

* Mon Sep 26 2016 François Kooman <fkooman@tuxed.net> - 6.0.0-0.9
- update to 41d6789a94a8b0309fbdc7cc4e7aa00864eb041a

* Fri Sep 23 2016 François Kooman <fkooman@tuxed.net> - 6.0.0-0.8
- update to d5767e5b639ac9a4e8acc4a64d05a180957b6389

* Wed Sep 21 2016 François Kooman <fkooman@tuxed.net> - 6.0.0-0.7
- update to 4a3597038ac595ae4a92ba2d9a7bc3c28e18ff10

* Sun Sep 18 2016 François Kooman <fkooman@tuxed.net> - 6.0.0-0.6
- update to dce93bc4fe816383bd5db8bbb2bcababec2bbc9f

* Sun Sep 18 2016 François Kooman <fkooman@tuxed.net> - 6.0.0-0.5
- update to dce93bc4fe816383bd5db8bbb2bcababec2bbc9f

* Sun Sep 18 2016 François Kooman <fkooman@tuxed.net> - 6.0.0-0.4
- update to 34659be5921589429b53edb0e975e6412bc162b0

* Thu Sep 15 2016 François Kooman <fkooman@tuxed.net> - 6.0.0-0.3
- rebuilt

* Wed Sep 14 2016 François Kooman <fkooman@tuxed.net> - 6.0.0-0.2
- rebuilt

* Wed Sep 14 2016 François Kooman <fkooman@tuxed.net> - 6.0.0-0.1
- update to 6.0.0
