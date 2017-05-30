%{?scl:%scl_package maven-bar}
%{!?scl:%global pkg_name %{name}}

Name:           %{?scl_prefix}maven-bar
Version:        1.0.0
Release:        1%{?dist}
Summary:        Example maven project
License:        BSD
Source0:        pom.xml
Source1:        Main.java
BuildArch:      noarch

BuildRequires:  %{?scl_prefix_maven}maven-local
BuildRequires:  %{?scl_prefix}mvn(org.fedoraproject.example:maven-foo)

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

%jpackage_script org.fedoraproject.example.Main '' '' maven-bar:maven-foo:slf4j/slf4j-api:slf4j/slf4j-simple example 1

%files -f .mfiles
%{_bindir}/example

%changelog
* Fri May 19 2017 Michael Simacek <msimacek@redhat.com> - 1.0.0-1
- Initial version
