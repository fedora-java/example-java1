%{?scl:%scl_package ivy-baz}
%{!?scl:%global pkg_name %{name}}

Name:           %{?scl_prefix}ivy-baz
Version:        1.0.0
Release:        1%{?dist}
Summary:        Example ivy project
License:        BSD
Source0:        ivy.xml
Source1:        build.xml
Source2:        Main.java
BuildArch:      noarch

BuildRequires:  %{?scl_prefix_java_common}ivy-local
BuildRequires:  %{?scl_prefix_java_common}ant
BuildRequires:  %{?scl_prefix_java_common}mvn(org.apache.commons:commons-lang3)
BuildRequires:  %{?scl_prefix}mvn(org.fedoraproject.example:maven-foo)

%description
%{summary}.

%prep
%setup -q -T -c %{pkg_name}

cp -p %{SOURCE0} ivy.xml
cp -p %{SOURCE1} build.xml
mkdir -p src/org/fedoraproject/example
cp -p %{SOURCE2} src/org/fedoraproject/example/

%build
%ant -Divy.mode=local compile

%install
%mvn_artifact ivy.xml ivy-baz.jar
%mvn_install

%files -f .mfiles

%changelog
* Fri May 19 2017 Michael Simacek <msimacek@redhat.com> - 1.0.0-1
- Initial version
