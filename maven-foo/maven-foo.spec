%{?scl:%scl_package maven-foo}
%{!?scl:%global pkg_name %{name}}

Name:           %{?scl_prefix}maven-foo
Version:        1.0.0
Release:        1%{?dist}
Summary:        Example maven project
License:        BSD
Source0:        pom.xml
Source1:        Foo.java
BuildArch:      noarch

BuildRequires:  %{?scl_prefix_maven}maven-local
BuildRequires:  %{?scl_prefix_maven}mvn(org.slf4j:slf4j-api)
BuildRequires:  %{?scl_prefix_maven}mvn(org.slf4j:slf4j-simple)

%description
%{summary}.

%prep
%setup -q -T -c %{pkg_name}

cp -p %{SOURCE0} pom.xml
mkdir -p src/main/java/org/fedoraproject/example
cp -p %{SOURCE1} src/main/java/org/fedoraproject/example/

%build
%mvn_build -j


%install
%mvn_install

%files -f .mfiles

%changelog
* Fri May 19 2017 Michael Simacek <msimacek@redhat.com> - 1.0.0-1
- Initial version
