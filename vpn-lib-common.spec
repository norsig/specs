%global composer_namespace      SURFnet/VPN/Common

%global github_owner            eduvpn
%global github_name             vpn-lib-common
%global github_commit           f1c4d0e453b75613a942cd6711e2ee8a097b518a
%global github_short            %(c=%{github_commit}; echo ${c:0:7})

Name:       vpn-lib-common
Version:    1.0.7
Release:    2%{?dist}
Summary:    Common VPN library
Group:      System Environment/Libraries
License:    AGPLv3+
URL:        https://github.com/%{github_owner}/%{github_name}
Source0:    %{url}/archive/%{github_commit}/%{name}-%{version}-%{github_short}.tar.gz
BuildArch:  noarch

BuildRequires:  php(language) >= 5.4.0
BuildRequires:  php-curl
BuildRequires:  php-filter
BuildRequires:  php-hash
BuildRequires:  php-json
BuildRequires:  php-mbstring
BuildRequires:  php-pcre
BuildRequires:  php-session
BuildRequires:  php-spl
BuildRequires:  php-composer(fedora/autoloader)
BuildRequires:  php-composer(psr/log)
BuildRequires:  php-composer(symfony/polyfill)
BuildRequires:  php-composer(symfony/yaml)
BuildRequires:  php-composer(guzzlehttp/guzzle) >= 5.3.0
BuildRequires:  php-composer(guzzlehttp/guzzle) < 6.0.0
BuildRequires:  %{_bindir}/phpunit

Requires:   php(language) >= 5.4.0
Requires:   php-curl
Requires:   php-filter
Requires:   php-hash
Requires:   php-json
Requires:   php-mbstring
Requires:   php-pcre
Requires:   php-session
Requires:   php-spl
Requires:   php-composer(fedora/autoloader)
Requires:   php-composer(psr/log)
Requires:   php-composer(symfony/polyfill)
Requires:   php-composer(symfony/yaml)
Requires:   php-composer(guzzlehttp/guzzle) >= 5.3.0
Requires:   php-composer(guzzlehttp/guzzle) < 6.0.0

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
    '%{_datadir}/php/GuzzleHttp/autoload.php',
    '%{_datadir}/php/Symfony/Polyfill/autoload.php',
    '%{_datadir}/php/Symfony/Component/Yaml/autoload.php',
));
AUTOLOAD

%install
mkdir -p %{buildroot}%{_datadir}/%{name}/%{composer_namespace}
cp -pr src/* %{buildroot}%{_datadir}/%{name}/%{composer_namespace}

%check
phpunit --bootstrap=%{buildroot}/%{_datadir}/%{name}/%{composer_namespace}/autoload.php

%files
%dir %{_datadir}/%{name}/SURFnet
%dir %{_datadir}/%{name}/SURFnet/VPN
%{_datadir}/%{name}/%{composer_namespace}
%doc README.md composer.json CHANGES.md
%license LICENSE

%changelog
* Fri Nov 25 2016 François Kooman <fkooman@tuxed.net> - 1.0.7-2
- spec cleanups

* Sun Nov 20 2016 François Kooman <fkooman@tuxed.net> - 1.0.7-1
- update to 1.0.7

* Wed Nov 16 2016 François Kooman <fkooman@tuxed.net> - 1.0.6-1
- update to 1.0.6

* Tue Nov 15 2016 François Kooman <fkooman@tuxed.net> - 1.0.5-1
- update to 1.0.5

* Mon Nov 14 2016 François Kooman <fkooman@tuxed.net> - 1.0.4-1
- update to 1.0.4

* Thu Nov 10 2016 François Kooman <fkooman@tuxed.net> - 1.0.3-1
- update to 1.0.3

* Wed Nov 09 2016 François Kooman <fkooman@tuxed.net> - 1.0.2-2
- rebuilt

* Wed Nov 09 2016 François Kooman <fkooman@tuxed.net> - 1.0.2-1
- update to 1.0.2

* Wed Nov 09 2016 François Kooman <fkooman@tuxed.net> - 1.0.1-1
- update to 1.0.1
- using PSR-4 now
- include CHANGES.md in docs

* Wed Nov 09 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-3
- some fedora autoloader fixes

* Wed Nov 09 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-2
- use new fedora autoloader
- spec cleanup

* Tue Nov 08 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-1
- initial release