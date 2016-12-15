%global composer_namespace      SURFnet/VPN/Common

%global github_owner            eduvpn
%global github_name             vpn-lib-common
%global github_commit           7154138b4f8954ed6d81e75480c09f79d5e05099
%global github_short            %(c=%{github_commit}; echo ${c:0:7})

Name:       vpn-lib-common
Version:    1.0.0
Release:    0.17%{?dist}
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
