%global composer_vendor         eduvpn
%global composer_project        vpn-admin-portal
%global composer_namespace      SURFnet/VPN/Admin

%global github_owner            eduvpn
%global github_name             vpn-admin-portal
%global github_commit           19674d0fd23277d3705e8373fa90e16743ac4b0a
%global github_short            %(c=%{github_commit}; echo ${c:0:7})

Name:       vpn-admin-portal
Version:    10.0.0
Release:    0.4%{?dist}
Summary:    VPN Admin Portal

Group:      Applications/Internet
License:    AGPLv3+

URL:        https://github.com/%{github_owner}/%{github_name}
Source0:    %{url}/archive/%{github_commit}/%{name}-%{version}-%{github_short}.tar.gz
Source1:    %{name}-autoload.php
Source2:    %{name}-httpd.conf

BuildArch:  noarch
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 

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
    cp -pr ${f} ${RPM_BUILD_ROOT}%{_sbindir}/%{name}-${f}
done
)

# Config
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}
ln -s ../../../etc/%{name} ${RPM_BUILD_ROOT}%{_datadir}/%{name}/config

# Data
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/lib/%{name}
ln -s ../../../var/lib/%{name} ${RPM_BUILD_ROOT}%{_datadir}/%{name}/data

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
%dir %attr(-,apache,apache) %{_sysconfdir}/%{name}
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
* Fri Sep 23 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.4
- fix data dir

* Fri Sep 23 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.3
- update to 19674d0fd23277d3705e8373fa90e16743ac4b0a

* Wed Sep 21 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.2
- update to 13503b2477dea9d21356d77adfbe248b3482b214

* Tue Sep 20 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.1
- update to 7502b4c61d830373b4bdbd13dd4ba4a0e64ea2e1
