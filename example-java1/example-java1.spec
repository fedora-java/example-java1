%global scl_name_prefix example-
%global scl_name_base java
%global scl_name_version 1
%global scl %{scl_name_prefix}%{scl_name_base}%{scl_name_version}
%scl_package %scl

Summary: Package that installs %scl
Name: %scl_name
Version: 1
Release: 1%{?dist}
License: GPLv2+

BuildRequires: scl-utils-build
BuildRequires: %{?scl_prefix_java_common}scldevel
# XXX scldevel should require javapackages-local
BuildRequires: %{?scl_prefix_java_common}javapackages-local

%description
This is the main package for %scl Software Collection.

%package runtime
Summary: Runtime scripts for the %scl Software Collection
Requires: scl-utils
Requires: %{?scl_prefix_java_common}runtime

%description runtime
Package shipping essential scripts to work with the %scl Software
Collection.

%package build
Summary: Build configuration for the %scl Software Collection
Requires: scl-utils-build
Requires: %{name}-scldevel = %{version}-%{release}

%description build
Package shipping essential configuration macros to build the %scl
Software Collection itself.

%package scldevel
Summary: Development files for the %scl Software Collection
Requires: %{name}-runtime = %{version}-%{release}
Requires: %{?scl_prefix_java_common}scldevel

%description scldevel
Package shipping development files, especially useful for development of
packages depending on the %scl Software Collection.

%prep
%setup -c -T

%build
# Enable collection script
# ========================
cat <<EOF >enable
#!/bin/bash
. /opt/rh/%{scl_java_common}/enable
export PATH="%{_bindir}:\${PATH:-/bin:/usr/bin}"
export MANPATH="%{_mandir}:\${MANPATH}"
export JAVACONFDIRS="%{_sysconfdir}/java\${JAVACONFDIRS:+:}\${JAVACONFDIRS:-}"
export XDG_CONFIG_DIRS="%{_sysconfdir}/xdg:\${XDG_CONFIG_DIRS:-/etc/xdg}"
export XDG_DATA_DIRS="%{_datadir}:\${XDG_DATA_DIRS:-/usr/local/share:/usr/share}"
EOF

# SCL devel macros
# ================
cat <<EOF >macros.%{scl}-scldevel
%%scl_%{scl_name_base} %{scl}
%%scl_prefix_%{scl_name_base} %{scl_prefix}
EOF

%install
%{scl_install}
%{scl_install_java}

install -p -m 644 macros.%{scl}-scldevel %{buildroot}%{_root_sysconfdir}/rpm/

# Install scl scripts
install -d -m 755 %{buildroot}%{_scl_scripts}
install -p -m 755 enable %{buildroot}%{_scl_scripts}/

%files

%files runtime -f .java-filelist
%{scl_files}

%files build
%{_root_sysconfdir}/rpm/macros.%{scl}-config

%files scldevel
%{_root_sysconfdir}/rpm/macros.%{scl}-scldevel

%changelog
* Thu May 18 2017 Michael Simacek <msimacek@redhat.com> - 1-1
- Initial version
