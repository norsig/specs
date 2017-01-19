%global composer_vendor         eduvpn
%global composer_project        vpn-user-portal
%global composer_namespace      SURFnet/VPN/Portal

%global github_owner            eduvpn
%global github_name             vpn-user-portal
%global github_commit           7e60c3f761c2a005aab4d75667c72a2918e47723
%global github_short            %(c=%{github_commit}; echo ${c:0:7})

Name:       vpn-user-portal
Version:    1.0.0
Release:    0.62%{?dist}
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
BuildRequires:  php-filter
BuildRequires:  php-gettext
BuildRequires:  php-hash
BuildRequires:  php-json
BuildRequires:  php-mbstring
BuildRequires:  php-pcre
BuildRequires:  php-pdo
BuildRequires:  php-spl
BuildRequires:  vpn-lib-common
BuildRequires:  php-composer(fedora/autoloader)
BuildRequires:  php-composer(twig/twig) < 2
BuildRequires:  php-composer(twig/extensions)
BuildRequires:  php-composer(bacon/bacon-qr-code)
BuildRequires:  php-composer(fkooman/oauth2-client)
BuildRequires:  php-composer(symfony/polyfill-php56)
BuildRequires:  php-composer(symfony/polyfill-php70)

Requires:   php(language) >= 5.4.0
# the scripts in bin/ require the PHP CLI
Requires:   php-cli
Requires:   php-date
Requires:   php-filter
Requires:   php-gettext
Requires:   php-hash
Requires:   php-json
Requires:   php-mbstring
Requires:   php-pcre
Requires:   php-pdo
Requires:   php-spl
Requires:   vpn-lib-common
Requires:   php-composer(fedora/autoloader)
Requires:   php-composer(twig/twig) < 2
Requires:   php-composer(twig/extensions)
Requires:   php-composer(bacon/bacon-qr-code)
Requires:   php-composer(fkooman/oauth2-client)
Requires:   php-composer(symfony/polyfill-php56)
Requires:   php-composer(symfony/polyfill-php70)

%if 0%{?fedora} >= 24
Requires:   httpd-filesystem
%else
# EL7 does not have httpd-filesystem
Requires:   httpd
%endif

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
    '%{_datadir}/php/SURFnet/VPN/Common/autoload.php',
    '%{_datadir}/php/Twig/autoload.php',
    '%{_datadir}/php/Twig/Extensions/autoload.php',
    '%{_datadir}/php/Symfony/Polyfill/autoload.php',
    '%{_datadir}/php/BaconQrCode/autoload.php',
    '%{_datadir}/php/fkooman/OAuth/Client/autoload.php',
));
AUTOLOAD

%install
install -m 0644 -D -p %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf

mkdir -p %{buildroot}%{_datadir}/%{name}
cp -pr web views locale %{buildroot}%{_datadir}/%{name}
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

mkdir -p %{buildroot}%{_sysconfdir}/%{name}/default
cp -pr config/config.php.example %{buildroot}%{_sysconfdir}/%{name}/default/config.php
ln -s ../../../etc/%{name} %{buildroot}%{_datadir}/%{name}/config

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
%config(noreplace) %{_sysconfdir}/%{name}/default/config.php
%{_bindir}/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/src
%{_datadir}/%{name}/data
%{_datadir}/%{name}/web
%{_datadir}/%{name}/views
%{_datadir}/%{name}/config
%{_datadir}/%{name}/locale
%dir %attr(0700,apache,apache) %{_localstatedir}/lib/%{name}
%doc README.md CHANGES.md composer.json config/config.php.example
%license LICENSE

%changelog
* Thu Jan 19 2017 François Kooman <fkooman@tuxed.net> - 1.0.0-0.62
- rebuilt

* Thu Jan 19 2017 François Kooman <fkooman@tuxed.net> - 1.0.0-0.61
- rebuilt

* Thu Jan 19 2017 François Kooman <fkooman@tuxed.net> - 1.0.0-0.60
- rebuilt

* Thu Jan 19 2017 François Kooman <fkooman@tuxed.net> - 1.0.0-0.59
- rebuilt

* Wed Jan 18 2017 François Kooman <fkooman@tuxed.net> - 1.0.0-0.58
- rebuilt

* Wed Jan 18 2017 François Kooman <fkooman@tuxed.net> - 1.0.0-0.57
- rebuilt

* Tue Jan 17 2017 François Kooman <fkooman@tuxed.net> - 1.0.0-0.56
- rebuilt

* Tue Jan 17 2017 François Kooman <fkooman@tuxed.net> - 1.0.0-0.55
- rebuilt

* Sun Jan 08 2017 François Kooman <fkooman@tuxed.net> - 1.0.0-0.54
- rebuilt

* Thu Jan 05 2017 François Kooman <fkooman@tuxed.net> - 1.0.0-0.53
- rebuilt

* Wed Jan 04 2017 François Kooman <fkooman@tuxed.net> - 1.0.0-0.52
- rebuilt

* Wed Jan 04 2017 François Kooman <fkooman@tuxed.net> - 1.0.0-0.51
- rebuilt

* Wed Jan 04 2017 François Kooman <fkooman@tuxed.net> - 1.0.0-0.50
- rebuilt

* Wed Jan 04 2017 François Kooman <fkooman@tuxed.net> - 1.0.0-0.49
- rebuilt

* Tue Jan 03 2017 François Kooman <fkooman@tuxed.net> - 1.0.0-0.48
- rebuilt

* Tue Jan 03 2017 François Kooman <fkooman@tuxed.net> - 1.0.0-0.47
- rebuilt

* Tue Jan 03 2017 François Kooman <fkooman@tuxed.net> - 1.0.0-0.46
- rebuilt

* Tue Jan 03 2017 François Kooman <fkooman@tuxed.net> - 1.0.0-0.45
- rebuilt

* Wed Dec 28 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.44
- rebuilt

* Wed Dec 28 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.43
- rebuilt

* Mon Dec 19 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.42
- rebuilt

* Fri Dec 16 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.41
- rebuilt

* Fri Dec 16 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.40
- rebuilt

* Fri Dec 16 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.39
- rebuilt

* Thu Dec 15 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.38
- rebuilt
