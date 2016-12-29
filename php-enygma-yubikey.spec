%global composer_namespace      Yubikey

%global github_owner            enygma
%global github_name             yubikey
%global github_commit           2a1b38754e94d8fa291f3747b237c492602229e3
%global github_short            %(c=%{github_commit}; echo ${c:0:7})

Name:       php-enygma-yubikey
Version:    3.2
Release:    1%{?dist}
Summary:    PHP library to interface with the Yubikey REST API
Group:      System Environment/Libraries
License:    MIT
URL:        https://github.com/%{github_owner}/%{github_name}
Source0:    %{url}/archive/%{github_commit}/%{name}-%{version}-%{github_short}.tar.gz
BuildArch:  noarch

BuildRequires:  php(language) >= 5.3.1
BuildRequires:  php-curl
BuildRequires:  php-filter
BuildRequires:  php-hash
BuildRequires:  php-openssl
BuildRequires:  php-pcre
BuildRequires:  php-spl
BuildRequires:  php-standard
BuildRequires:  php-xml
BuildRequires:  php-composer(fedora/autoloader)
BuildRequires:  %{_bindir}/phpunit

Requires:   php(language) >= 5.3.1
Requires:   php-curl
Requires:   php-filter
Requires:   php-hash
Requires:   php-openssl
Requires:   php-pcre
Requires:   php-spl
Requires:   php-standard
Requires:   php-xml
Requires:   php-composer(fedora/autoloader)

Provides:   php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
This library lets you easily interface with the Yubico REST API for 
validating the codes created by the Yubikey.

%prep
%setup -qn %{github_name}-%{github_commit}

%build
cat <<'AUTOLOAD' | tee src/%{composer_namespace}/autoload.php
<?php
require_once '%{_datadir}/php/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr0('Yubikey\\', dirname(__DIR__));
AUTOLOAD

%install
mkdir -p %{buildroot}%{_datadir}/php/%{composer_namespace}
cp -pr src/* %{buildroot}%{_datadir}/php

%check
phpunit tests --bootstrap=%{buildroot}/%{_datadir}/php/%{composer_namespace}/autoload.php

%files
%{_datadir}/php/%{composer_namespace}
%doc README.md composer.json
# LICENSE not really clear, https://github.com/enygma/yubikey/issues/23
#%%license LICENSE

%changelog
* Thu Dec 29 2016 François Kooman <fkooman@tuxed.net> - 3.2-1
- initial build
