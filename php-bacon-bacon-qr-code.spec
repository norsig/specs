%global composer_vendor         bacon
%global composer_project        bacon-qr-code
%global composer_namespace      BaconQrCode

%global github_owner            Bacon
%global github_name             BaconQrCode
%global github_commit           031a2ce68c5794064b49d11775b2daf45c96e21c
%global github_short            %(c=%{github_commit}; echo ${c:0:7})
%if 0%{?rhel} == 5
%global with_tests              0%{?_with_tests:1}
%else
%global with_tests              0%{!?_without_tests:1}
%endif

Name:       php-%{composer_vendor}-%{composer_project}
Version:    1.0.1
Release:    1%{?dist}
Summary:    QR Code Generator for PHP 

Group:      System Environment/Libraries
License:    BSD-2-Clause

URL:        https://github.com/%{github_owner}/%{github_name}
Source0:    %{url}/archive/%{github_commit}/%{name}-%{version}-%{github_short}.tar.gz
Source1:    %{name}-autoload.php

BuildArch:  noarch
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 

%if %{with_tests}
BuildRequires:  %{_bindir}/phpunit
BuildRequires:  %{_bindir}/phpab
BuildRequires:  php-composer(symfony/class-loader)
%endif

Requires:   php(language) >= 5.3.3
Requires:   php-gd
Requires:   php-composer(symfony/class-loader)

Provides:   php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
BaconQrCode is a QR code generator for PHP.

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
    --bootstrap tests/bootstrap.php tests
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
* Mon Feb 15 2016 François Kooman <fkooman@tuxed.net> - 1.0.1-1
initial package
