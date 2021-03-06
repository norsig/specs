%global composer_vendor         fkooman
%global composer_project        oauth2-server
%global composer_namespace      %{composer_vendor}/OAuth/Server

%global github_owner            fkooman
%global github_name             php-oauth2-server
%global github_commit           06b8ad7409ef25774399117155dcea6a45609556
%global github_short            %(c=%{github_commit}; echo ${c:0:7})

Name:       php-%{composer_vendor}-%{composer_project}
Version:    1.0.0
Release:    0.14%{?dist}
Summary:    Very simple OAuth 2.0 server

Group:      System Environment/Libraries
License:    AGPLv3+

URL:        https://github.com/%{github_owner}/%{github_name}
Source0:    %{url}/archive/%{github_commit}/%{name}-%{version}-%{github_short}.tar.gz

BuildArch:  noarch

BuildRequires:  php(language) >= 5.4.0
BuildRequires:  php-libsodium
BuildRequires:  php-date
BuildRequires:  php-hash
BuildRequires:  php-json
BuildRequires:  php-pcre
BuildRequires:  php-pdo
BuildRequires:  php-standard
BuildRequires:  php-composer(fedora/autoloader)
BuildRequires:  %{_bindir}/phpunit

Requires:   php(language) >= 5.4.0
Requires:   php-libsodium
Requires:   php-date
Requires:   php-hash
Requires:   php-json
Requires:   php-pcre
Requires:   php-pdo
Requires:   php-standard
Requires:   php-composer(fedora/autoloader)

Provides:   php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
This is a very simple OAuth 2.0 server for integration in your own 
application. It has minimal dependencies, but still tries to be secure. 
The main purpose is to be compatible with PHP 5.4.

%prep
%setup -qn %{github_name}-%{github_commit} 

%build
cat <<'AUTOLOAD' | tee src/autoload.php
<?php
require_once '%{_datadir}/php/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('fkooman\\OAuth\\Server\\', __DIR__);
AUTOLOAD

%install
mkdir -p %{buildroot}%{_datadir}/php/%{composer_namespace}
cp -pr src/* %{buildroot}%{_datadir}/php/%{composer_namespace}

%check
phpunit --bootstrap=%{buildroot}/%{_datadir}/php/%{composer_namespace}/autoload.php

%files
%dir %{_datadir}/php/fkooman
%dir %{_datadir}/php/fkooman/OAuth
%{_datadir}/php/%{composer_namespace}
%doc README.md CHANGES.md composer.json
%license LICENSE

%changelog
* Wed Jan 25 2017 François Kooman <fkooman@tuxed.net> - 1.0.0-0.14
- rebuilt

* Wed Jan 25 2017 François Kooman <fkooman@tuxed.net> - 1.0.0-0.13
- rebuilt

* Wed Jan 25 2017 François Kooman <fkooman@tuxed.net> - 1.0.0-0.12
- rebuilt

* Wed Jan 25 2017 François Kooman <fkooman@tuxed.net> - 1.0.0-0.11
- rebuilt

* Wed Jan 25 2017 François Kooman <fkooman@tuxed.net> - 1.0.0-0.10
- rebuilt

* Mon Jan 23 2017 François Kooman <fkooman@tuxed.net> - 1.0.0-0.9
- rebuilt

* Mon Jan 23 2017 François Kooman <fkooman@tuxed.net> - 1.0.0-0.8
- rebuilt

* Mon Jan 23 2017 François Kooman <fkooman@tuxed.net> - 1.0.0-0.7
- rebuilt

* Mon Jan 23 2017 François Kooman <fkooman@tuxed.net> - 1.0.0-0.6
- rebuilt

* Mon Jan 23 2017 François Kooman <fkooman@tuxed.net> - 1.0.0-0.5
- rebuilt

* Sun Jan 22 2017 François Kooman <fkooman@tuxed.net> - 1.0.0-0.4
- rebuilt

* Fri Jan 20 2017 François Kooman <fkooman@tuxed.net> - 1.0.0-0.3
- rebuilt

* Fri Jan 20 2017 François Kooman <fkooman@tuxed.net> - 1.0.0-0.2
- rebuilt

* Fri Jan 20 2017 François Kooman <fkooman@tuxed.net> - 1.0.0-0.1
- initial package
