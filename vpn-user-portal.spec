%global composer_vendor         eduvpn
%global composer_project        vpn-user-portal
%global composer_namespace      SURFnet/VPN/Portal

%global github_owner            eduvpn
%global github_name             vpn-user-portal
%global github_commit           1fd4f6b10d956bf4427069322f06937f64cf5508
%global github_short            %(c=%{github_commit}; echo ${c:0:7})

Name:       vpn-user-portal
Version:    10.0.0
Release:    0.66%{?dist}
Summary:    VPN User Portal

Group:      Applications/Internet
License:    AGPLv3+

URL:        https://github.com/%{github_owner}/%{github_name}
Source0:    %{url}/archive/%{github_commit}/%{name}-%{version}-%{github_short}.tar.gz
Source1:    %{name}-httpd.conf

BuildArch:  noarch
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 

BuildRequires:  %{_bindir}/phpunit
BuildRequires:  php(language) >= 5.4.0
BuildRequires:  php-date
BuildRequires:  php-gettext
BuildRequires:  php-json
BuildRequires:  php-pcre
BuildRequires:  php-pdo
BuildRequires:  php-spl
BuildRequires:  vpn-lib-common
BuildRequires:  php-composer(fedora/autoloader)
BuildRequires:  php-composer(twig/twig)
BuildRequires:  php-composer(twig/extensions)
BuildRequires:  php-composer(bacon/bacon-qr-code)
BuildRequires:  php-composer(christian-riesen/otp)
BuildRequires:  php-composer(guzzlehttp/guzzle) >= 5.3.0
BuildRequires:  php-composer(guzzlehttp/guzzle) < 6.0.0
BuildRequires:  php-composer(fkooman/oauth2-client)

Requires:   httpd
Requires:   php(language) >= 5.4.0
Requires:   php-date
Requires:   php-gettext
Requires:   php-json
Requires:   php-mbstring
Requires:   php-pcre
Requires:   php-pdo
Requires:   php-spl
Requires:   vpn-lib-common
Requires:   php-composer(fedora/autoloader)
Requires:   php-composer(twig/twig)
Requires:   php-composer(twig/extensions)
Requires:   php-composer(bacon/bacon-qr-code)
Requires:   php-composer(christian-riesen/otp)
Requires:   php-composer(guzzlehttp/guzzle) >= 5.3.0
Requires:   php-composer(guzzlehttp/guzzle) < 6.0.0
Requires:   php-composer(fkooman/oauth2-client)

Requires(post): /usr/sbin/semanage
Requires(postun): /usr/sbin/semanage

%description
VPN User Portal.

%prep
%setup -qn %{github_name}-%{github_commit} 

sed -i "s|require_once sprintf('%s/vendor/autoload.php', dirname(__DIR__));|require_once '%{_datadir}/%{name}/src/%{composer_namespace}/autoload.php';|" bin/*
sed -i "s|require_once sprintf('%s/vendor/autoload.php', dirname(__DIR__));|require_once '%{_datadir}/%{name}/src/%{composer_namespace}/autoload.php';|" web/*.php
sed -i "s|dirname(__DIR__)|'%{_datadir}/%{name}'|" bin/*

%build
cat <<'AUTOLOAD' | tee src/autoload.php
<?php
require_once '%{_datadir}/php/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('SURFnet\\VPN\\Portal\\', __DIR__);
\Fedora\Autoloader\Dependencies::required(array(
    '%{_datadir}/php/Otp/autoload.php',
    '%{_datadir}/php/GuzzleHttp/autoload.php',
    '%{_datadir}/php/SURFnet/VPN/Common/autoload.php',
    '%{_datadir}/php/Twig/autoload.php',
    '%{_datadir}/php/Twig/Extensions/autoload.php',
    '%{_datadir}/php/BaconQrCode/autoload.php',
    '%{_datadir}/php/fkooman/OAuth/Client/autoload.php',
));
AUTOLOAD

%install
# Apache configuration
install -m 0644 -D -p %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf

# Application
mkdir -p %{buildroot}%{_datadir}/%{name}
cp -pr web views locale %{buildroot}%{_datadir}/%{name}
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

%check
phpunit --bootstrap=%{buildroot}/%{_datadir}/%{name}/src/%{composer_namespace}/autoload.php

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
%dir %attr(0750,root,apache) %{_sysconfdir}/%{name}/default
%config(noreplace) %{_sysconfdir}/%{name}/default/config.yaml
%{_bindir}/*
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
* Sun Nov 27 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.66
- rebuilt

* Fri Nov 25 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.65
- rebuilt

* Wed Nov 23 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.64
- rebuilt

* Tue Nov 22 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.63
- rebuilt

* Tue Nov 22 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.62
- rebuilt

* Tue Nov 22 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.61
- rebuilt

* Mon Nov 21 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.60
- rebuilt

* Mon Nov 21 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.59
- rebuilt

* Mon Nov 21 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.58
- rebuilt

* Sun Nov 20 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.57
- rebuilt

* Sun Nov 20 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.56
- rebuilt

* Sun Nov 20 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.55
- rebuilt

* Sun Nov 20 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.54
- rebuilt

* Sun Nov 20 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.53
- rebuilt

* Fri Nov 18 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.52
- rebuilt

* Fri Nov 18 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.51
- rebuilt

* Fri Nov 18 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.50
- rebuilt

* Fri Nov 18 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.49
- rebuilt

* Wed Nov 16 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.48
- rebuilt

* Tue Nov 15 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.47
- rebuilt

* Tue Nov 15 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.46
- rebuilt

* Tue Nov 15 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.45
- rebuilt

* Tue Nov 15 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.44
- rebuilt

* Tue Nov 15 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.43
- rebuilt

* Mon Nov 14 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.42
- rebuilt

* Sun Nov 13 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.41
- rebuilt

* Thu Nov 10 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.40
- rebuilt

* Thu Nov 10 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.39
- rebuilt

* Wed Nov 09 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.38
- rebuilt

* Wed Nov 09 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.37
- rebuilt

* Wed Nov 09 2016 François Kooman <fkooman@tuxed.net> - 10.0.0-0.36
- rebuilt
