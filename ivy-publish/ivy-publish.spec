%{?scl:%scl_package ivy-publish}
%{!?scl:%global pkg_name %{name}}

Name:           %{?scl_prefix}ivy-publish
Version:        1.0.0
Release:        1%{?dist}
Summary:        Example ivy project
License:        BSD
Source0:        ivy.xml
Source1:        build.xml
Source2:        Main2.java
BuildArch:      noarch

BuildRequires:  %{?scl_prefix_maven}ivy-local
BuildRequires:  %{?scl_prefix_maven}ant
BuildRequires:  %{?scl_prefix}mvn(org.fedoraproject.example:ivy-baz)

%description
%{summary}.

%prep
%setup -q -T -c %{pkg_name}

cp -p %{SOURCE0} ivy.xml
cp -p %{SOURCE1} build.xml
mkdir -p src/org/fedoraproject/example
cp -p %{SOURCE2} src/org/fedoraproject/example/

%pom_xpath_set ivy:publish/@resolver xmvn build.xml

%build
%ant -Divy.mode=local publish-local

%install
%mvn_install

%files -f .mfiles

%changelog
* Fri May 19 2017 Michael Simacek <msimacek@redhat.com> - 1.0.0-1
- Initial version
