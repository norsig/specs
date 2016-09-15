%global composer_vendor         eduvpn
%global composer_project        common
%global composer_namespace      SURFnet/VPN/Common

%global github_owner            eduvpn
%global github_name             vpn-lib-common
%global github_commit           d1a3e49b5d9653497bd7f479409724fdb3377f81
%global github_short            %(c=%{github_commit}; echo ${c:0:7})
%if 0%{?rhel} == 5
%global with_tests              0%{?_with_tests:1}
%else
%global with_tests              0%{!?_without_tests:1}
%endif

Name:       php-%{composer_vendor}-%{composer_project}
Version:    1.0.0
Release:    0.3%{?dist}
Summary:    Common VPN library

Group:      System Environment/Libraries
License:    AGPLv3+

URL:        https://github.com/%{github_owner}/%{github_name}
Source0:    %{url}/archive/%{github_commit}/%{name}-%{version}-%{github_short}.tar.gz
Source1:    %{name}-autoload.php

BuildArch:  noarch
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 

%if %{with_tests}
BuildRequires:  php(language) >= 5.4.0
BuildRequires:  php-json
BuildRequires:  php-hash
BuildRequires:  php-spl
BuildRequires:  php-composer(psr/log)
BuildRequires:  php-composer(symfony/polyfill)
BuildRequires:  php-composer(symfony/yaml)
BuildRequires:  php-composer(symfony/class-loader)
BuildRequires:  %{_bindir}/phpunit
BuildRequires:  %{_bindir}/phpab
%endif

Requires:   php(language) >= 5.4.0
Requires:   php-json
Requires:   php-hash
Requires:   php-spl
Requires:   php-composer(psr/log)
Requires:   php-composer(symfony/polyfill)
Requires:   php-composer(symfony/yaml)
Requires:   php-composer(symfony/class-loader)

Provides:   php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
Common VPN library.

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
* Thu Sep 15 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.3
- update to d1a3e49b5d9653497bd7f479409724fdb3377f81

* Thu Sep 15 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.2
- update to 7ff266d86053d14dad01f32b6e41d17ef59d06a4

* Wed Sep 14 2016 François Kooman <fkooman@tuxed.net> - 1.0.0-0.1
- initial package
