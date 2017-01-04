%global composer_namespace      SURFnet/VPN/Common

%global github_owner            eduvpn
%global github_name             vpn-lib-common
%global github_commit           6da31dcfacb27c94c115735e934f46e0d5bfb771
%global github_short            %(c=%{github_commit}; echo ${c:0:7})

Name:       vpn-lib-common
Version:    1.0.0
Release:    0.25%{?dist}
Summary:    Common VPN library
Group:      System Environment/Libraries
License:    AGPLv3+
URL:        https://github.com/%{github_owner}/%{github_name}
Source0:    %{url}/archive/%{github_commit}/%{name}-%{version}-%{github_short}.tar.gz
BuildArch:  noarch

BuildRequires:  php(language) >= 5.4.0
BuildRequires:  php-curl
BuildRequires:  php-date
BuildRequires:  php-filter
BuildRequires:  php-hash
BuildRequires:  php-json
BuildRequires:  php-mbstring
BuildRequires:  php-pcre
BuildRequires:  php-session
BuildRequires:  php-spl
BuildRequires:  php-composer(fedora/autoloader)
BuildRequires:  php-composer(psr/log)
BuildRequires:  php-composer(symfony/polyfill-php55)
BuildRequires:  php-composer(symfony/polyfill-php56)
BuildRequires:  php-composer(symfony/polyfill-php70)
BuildRequires:  %{_bindir}/phpunit

Requires:   php(language) >= 5.4.0
Requires:   php-curl
Requires:   php-date
Requires:   php-filter
Requires:   php-hash
Requires:   php-json
Requires:   php-mbstring
Requires:   php-pcre
Requires:   php-session
Requires:   php-spl
Requires:   php-composer(fedora/autoloader)
Requires:   php-composer(psr/log)
Requires:   php-composer(symfony/polyfill-php55)
Requires:   php-composer(symfony/polyfill-php56)
Requires:   php-composer(symfony/polyfill-php70)

%description
Common VPN library.

%prep
%setup -qn %{github_name}-%{github_commit}

%build
cat <<'AUTOLOAD' | tee src/autoload.php
<?php
require_once '%{_datadir}/php/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('SURFnet\\VPN\\Common\\', __DIR__);
\Fedora\Autoloader\Dependencies::required(array(
    '%{_datadir}/php/Psr/Log/autoload.php',
    '%{_datadir}/php/Symfony/Polyfill/autoload.php',
));
AUTOLOAD

%install
mkdir -p %{buildroot}%{_datadir}/php/%{composer_namespace}
cp -pr src/* %{buildroot}%{_datadir}/php/%{composer_namespace}

%check
phpunit --bootstrap=%{buildroot}/%{_datadir}/php/%{composer_namespace}/autoload.php

%files
%dir %{_datadir}/php/SURFnet
%dir %{_datadir}/php/SURFnet/VPN
%{_datadir}/php/%{composer_namespace}
%doc README.md composer.json CHANGES.md
%license LICENSE

%changelog
* Wed Jan 04 2017 François Kooman <fkooman@tuxed.net> - 1.0.0-0.25
- rebuilt

* Wed Jan 04 2017 François Kooman <fkooman@tuxed.net> - 1.0.0-0.24
- rebuilt

* Wed Jan 04 2017 François Kooman <fkooman@tuxed.net> - 1.0.0-0.23
- rebuilt

* Tue Jan 03 2017 François Kooman <fkooman@tuxed.net> - 1.0.0-0.22
- rebuilt

* Tue Jan 03 2017 François Kooman <fkooman@tuxed.net> - 1.0.0-0.21
- rebuilt

* Tue Jan 03 2017 François Kooman <fkooman@tuxed.net> - 1.0.0-0.20
- rebuilt

* Tue Jan 03 2017 François Kooman <fkooman@tuxed.net> - 1.0.0-0.19
- rebuilt

* Thu Dec 15 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.18
- rebuilt

* Thu Dec 15 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.17
- rebuilt

* Tue Dec 13 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.16
- rebuilt

* Tue Dec 13 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.15
- rebuilt

* Mon Dec 12 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.14
- rebuilt

* Mon Dec 12 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.13
- rebuilt

* Wed Dec 07 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.12
- rebuilt

* Tue Dec 06 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.11
- rebuilt

* Tue Dec 06 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.10
- rebuilt

* Mon Dec 05 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.9
- rebuilt

* Sun Dec 04 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.8
- rebuilt

* Sat Dec 03 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.7
- rebuilt

* Fri Dec 02 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.6
- rebuilt

* Fri Dec 02 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.5
- rebuilt

* Fri Dec 02 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.4
- rebuilt

* Thu Dec 01 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.3
- rebuilt

* Thu Dec 01 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.2
- rebuilt

* Thu Dec 01 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.1
- rebuilt
