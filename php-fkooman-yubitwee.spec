%global composer_vendor         fkooman
%global composer_project        yubitwee
%global composer_namespace      %{composer_vendor}/YubiTwee

%global github_owner            fkooman
%global github_name             php-yubitwee
%global github_commit           4654fa8739b979555198ee60caba8558d00ba560
%global github_short            %(c=%{github_commit}; echo ${c:0:7})

Name:       php-%{composer_vendor}-%{composer_project}
Version:    1.0.0
Release:    0.1%{?dist}
Summary:    YubiKey Validator

Group:      System Environment/Libraries
License:    AGPLv3+

URL:        https://github.com/%{github_owner}/%{github_name}
Source0:    %{url}/archive/%{github_commit}/%{name}-%{version}-%{github_short}.tar.gz

BuildArch:  noarch

BuildRequires:  php(language) >= 5.4.0
BuildRequires:  php-curl
BuildRequires:  php-hash
BuildRequires:  php-pcre
BuildRequires:  php-spl
BuildRequires:  php-standard
BuildRequires:  php-composer(paragonie/random_compat)
BuildRequires:  php-composer(symfony/polyfill-php56)
BuildRequires:  php-composer(fedora/autoloader)
BuildRequires:  %{_bindir}/phpunit

Requires:   php(language) >= 5.4.0
Requires:   php-curl
Requires:   php-hash
Requires:   php-pcre
Requires:   php-spl
Requires:   php-standard
Requires:   php-composer(paragonie/random_compat)
Requires:   php-composer(symfony/polyfill-php56)
Requires:   php-composer(fedora/autoloader)

Provides:   php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
A very simple, secure YubiKey OTP Validator with pluggable HTTP client.

%prep
%setup -qn %{github_name}-%{github_commit} 

%build
cat <<'AUTOLOAD' | tee src/autoload.php
<?php
require_once '%{_datadir}/php/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('fkooman\\YubiTwee\\', __DIR__);
\Fedora\Autoloader\Dependencies::required(array(
    '%{_datadir}/php/random_compat/autoload.php',
    '%{_datadir}/php/Symfony/Polyfill/autoload.php',
));
AUTOLOAD

%install
mkdir -p %{buildroot}%{_datadir}/php/%{composer_namespace}
cp -pr src/* %{buildroot}%{_datadir}/php/%{composer_namespace}

%check
phpunit --bootstrap=%{buildroot}/%{_datadir}/php/%{composer_namespace}/autoload.php

%files
%dir %{_datadir}/php/fkooman
%dir %{_datadir}/php/fkooman/YubiTwee
%{_datadir}/php/%{composer_namespace}
%doc README.md CHANGES.md composer.json
%license LICENSE

%changelog
* Tue Jan 03 2017 François Kooman <fkooman@tuxed.net> - 1.0.0-0.1
- initial package
