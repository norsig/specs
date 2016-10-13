%global composer_vendor         christian-riesen
%global composer_project        otp
%global composer_namespace      Otp

%global github_owner            ChristianRiesen
%global github_name             otp
%global github_commit           b441f8338c0375df3e288225acefb943c0b3cb05
%global github_short            %(c=%{github_commit}; echo ${c:0:7})
%if 0%{?rhel} == 5
%global with_tests              0%{?_with_tests:1}
%else
%global with_tests              0%{!?_without_tests:1}
%endif

Name:       php-%{composer_vendor}-%{composer_project}
Version:    2.2.0
Release:    2%{?dist}
Summary:    One Time Passwords

Group:      System Environment/Libraries
License:    MIT

URL:        https://github.com/%{github_owner}/%{github_name}
Source0:    %{url}/archive/%{github_commit}/%{name}-%{version}-%{github_short}.tar.gz
Source1:    %{name}-autoload.php

BuildArch:  noarch
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 

%if %{with_tests}
BuildRequires:  php(language) >= 5.4.0
BuildRequires:  php-date
BuildRequires:  php-hash
BuildRequires:  php-openssl
BuildRequires:  php-spl
BuildRequires:  php-composer(christian-riesen/base32)
BuildRequires:  php-composer(paragonie/random_compat)
BuildRequires:  php-composer(symfony/class-loader)
BuildRequires:  %{_bindir}/phpunit
BuildRequires:  %{_bindir}/phpab
%endif

Requires:   php(language) >= 5.4.0
Requires:   php-date
Requires:   php-hash
Requires:   php-openssl
Requires:   php-spl
Requires:   php-composer(christian-riesen/base32)
Requires:   php-composer(paragonie/random_compat)
Requires:   php-composer(symfony/class-loader)

Provides:   php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
Implements hotp according to RFC4226 and totp according to RFC6238 (only sha1 
algorithm).

%prep
%setup -qn %{github_name}-%{github_commit}
cp %{SOURCE1} src/autoload.php

%build

%install
rm -rf %{buildroot} 
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/php/%{composer_namespace}
cp -pr src/* ${RPM_BUILD_ROOT}%{_datadir}/php/%{composer_namespace}/

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
* Thu Oct 13 2016 François Kooman <fkooman@tuxed.net> - 2.2.0-2
- do not depend on libsodium any longer

* Wed Sep 14 2016 François Kooman <fkooman@tuxed.net> - 2.2.0-1
- update to 2.2.0

* Fri Apr 22 2016 François Kooman <fkooman@tuxed.net> - 1.4.3-1
- initial package
