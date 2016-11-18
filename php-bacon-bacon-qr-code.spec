%global composer_vendor         bacon
%global composer_project        bacon-qr-code
%global composer_namespace      BaconQrCode

%global github_owner            Bacon
%global github_name             BaconQrCode
%global github_commit           031a2ce68c5794064b49d11775b2daf45c96e21c
%global github_short            %(c=%{github_commit}; echo ${c:0:7})

Name:       php-%{composer_vendor}-%{composer_project}
Version:    1.0.1
Release:    2%{?dist}
Summary:    QR Code Generator for PHP 

Group:      System Environment/Libraries
License:    BSD-2-Clause

URL:        https://github.com/%{github_owner}/%{github_name}
Source0:    %{url}/archive/%{github_commit}/%{name}-%{version}-%{github_short}.tar.gz

BuildArch:  noarch
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 

BuildRequires:  php(language) >= 5.3.3
BuildRequires:  php-gd
BuildRequires:  php-iconv
BuildRequires:  %{_bindir}/phpunit
BuildRequires:  php-composer(fedora/autoloader)

Requires:   php(language) >= 5.3.3
Requires:   php-gd
Requires:   php-iconv
Requires:   php-composer(fedora/autoloader)

Provides:   php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
BaconQrCode is a QR code generator for PHP.

%prep
%setup -qn %{github_name}-%{github_commit} 

%build
cat <<'AUTOLOAD' | tee src/%{composer_namespace}/autoload.php
<?php
require_once '%{_datadir}/php/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr0('BaconQrCode\\', dirname(__DIR__));
AUTOLOAD

%install
rm -rf %{buildroot} 
mkdir -p %{buildroot}%{_datadir}/php
cp -pr src/* %{buildroot}%{_datadir}/php

%check
phpunit --bootstrap=%{buildroot}/%{_datadir}/php/%{composer_namespace}/autoload.php tests

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_datadir}/php/%{composer_namespace}
%doc README.md composer.json
%license LICENSE

%changelog
* Tue Nov 15 2016 François Kooman <fkooman@tuxed.net> - 1.0.1-2
- update spec

* Mon Feb 15 2016 François Kooman <fkooman@tuxed.net> - 1.0.1-1
- initial package