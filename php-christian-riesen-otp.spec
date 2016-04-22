%global composer_vendor         christian-riesen
%global composer_project        otp
%global composer_namespace      Otp

%global github_owner            ChristianRiesen
%global github_name             otp
%global github_commit           20a539ce6280eb029030f4e7caefd5709a75e1ad
%global github_short            %(c=%{github_commit}; echo ${c:0:7})
%if 0%{?rhel} == 5
%global with_tests              0%{?_with_tests:1}
%else
%global with_tests              0%{!?_without_tests:1}
%endif

Name:       php-%{composer_vendor}-%{composer_project}
Version:    1.4.3
Release:    1%{?dist}
Summary:    One Time Passwords

Group:      System Environment/Libraries
License:    MIT

URL:        https://github.com/%{github_owner}/%{github_name}
Source0:    %{url}/archive/%{github_commit}/%{name}-%{version}-%{github_short}.tar.gz
Source1:    %{name}-autoload.php

BuildArch:  noarch
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 

%if %{with_tests}
BuildRequires:  php(language) >= 5.3.0
BuildRequires:  php-date
BuildRequires:  php-hash
BuildRequires:  php-openssl
BuildRequires:  php-spl
BuildRequires:  php-libsodium
BuildRequires:  php-composer(christian-riesen/base32) >= 1.0
BuildRequires:  php-composer(christian-riesen/base32) < 2.0
BuildRequires:  php-composer(paragonie/random_compat) >= 1.0.0
BuildRequires:  php-composer(paragonie/random_compat) < 2.0.0
BuildRequires:  php-composer(symfony/class-loader)
BuildRequires:  %{_bindir}/phpunit
BuildRequires:  %{_bindir}/phpab
%endif

Requires:   php(language) >= 5.3.0
Requires:   php-date
Requires:   php-hash
Requires:   php-openssl
Requires:   php-spl
Requires:   php-libsodium
Requires:   php-composer(paragonie/random_compat) >= 1.0.0
Requires:   php-composer(paragonie/random_compat) < 2.0.0
Requires:   php-composer(christian-riesen/base32) >= 1.0
Requires:   php-composer(christian-riesen/base32) < 2.0
Requires:   php-composer(symfony/class-loader)

Provides:   php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
Implements hotp according to RFC4226 and totp according to RFC6238 (only sha1 
algorithm).

%prep
%setup -qn %{github_name}-%{github_commit}
cp %{SOURCE1} src/%{composer_namespace}/autoload.php

%build

%install
rm -rf %{buildroot} 
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/php
cp -pr src/* ${RPM_BUILD_ROOT}%{_datadir}/php

%if %{with_tests} 
%check
%{_bindir}/phpab --output tests/bootstrap.php tests
echo 'require "%{buildroot}%{_datadir}/php/%{composer_namespace}/autoload.php";' >> tests/bootstrap.php
%{_bindir}/phpunit \
    --bootstrap tests/bootstrap.php
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_datadir}/php/%{composer_namespace}
%doc README.md composer.json
%{!?_licensedir:%global license %%doc} 
%license LICENSE

%changelog
* Fri Apr 22 2016 François Kooman <fkooman@tuxed.net> - 1.4.3-1
- initial package
