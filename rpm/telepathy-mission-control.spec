Name:       telepathy-mission-control

Summary:    Central control for Telepathy connection manager
Version:    5.15.0
Release:    1
Group:      System/Libraries
License:    LGPLv2
URL:        http://mission-control.sourceforge.net/
Source0:    http://telepathy.freedesktop.org/releases/telepathy-mission-control/%{name}-%{version}.tar.gz
Source1:    mktests.sh
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  pkgconfig(dbus-1) >= 0.95
BuildRequires:  pkgconfig(dbus-glib-1) >= 0.82
BuildRequires:  pkgconfig(telepathy-glib) >= 0.19.0
BuildRequires:  pkgconfig(glib-2.0) >= 2.32
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gmodule-no-export-2.0)
BuildRequires:  pkgconfig(gio-2.0) >= 2.28
BuildRequires:  pkgconfig(mce)
BuildRequires:  libxslt
BuildRequires:  python
BuildRequires:  fdupes
BuildRequires:  python-twisted
BuildRequires:  dbus-python

%description
Mission Control, or MC, is a Telepathy component providing a way for
"end-user" applications to abstract some of the details of connection
managers, to provide a simple way to manipulate a bunch of connection
managers at once, and to remove the need to have in each program the
account definitions and credentials.


%package tests
Summary:    Tests package for %{name}
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires:   python-twisted
Requires:   dbus-python
Requires:   pygobject2

%description tests
The %{name}-tests package contains tests and
tests.xml for automated testing.


%package devel
Summary:    Headers files for %{name}
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header
files for developing applications that use %{name}.


%prep
%setup -q -n %{name}-%{version}/telepathy-mission-control

%build
# >> build pre
#autoreconf -vfi
%autogen --disable-static \
--disable-gtk-doc \
--with-accounts-cache-dir=/tmp \
--disable-Werror \
--with-connectivity=connman \
--disable-conn-setting \
--enable-installed-tests \
--disable-gtk-doc
# << build pre


make %{?_smp_mflags}

# >> build post
tests/twisted/mktests.sh > tests/tests.xml
# << build post

%install
rm -rf %{buildroot}
# >> install pre
# << install pre
%make_install

# >> install post
gzip -k ChangeLog
%fdupes %{buildroot}/%{_datadir}/gtk-doc/
%fdupes %{buildroot}/%{_includedir}
install -m 0644 tests/tests.xml $RPM_BUILD_ROOT/opt/tests/telepathy-mission-control/tests.xml
install -m 0644 tests/README $RPM_BUILD_ROOT/opt/tests/telepathy-mission-control/README
# << install post

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
# >> files
%doc COPYING AUTHORS
%{_bindir}/*
%{_datadir}/dbus-1/services/*.service
%{_libdir}/libmission-control-plugins.so.*
%{_libexecdir}/mission-control-5
## --disable-conn-setting
#%{_datadir}/glib-2.0/schemas/im.telepathy.MissionControl.FromEmpathy.gschema.xml
# << files

%files tests
%defattr(-,root,root,-)
/opt/tests/telepathy-mission-control/*
# >> files tests
# << files tests

%files devel
%defattr(-,root,root,-)
# >> files devel
%doc ChangeLog.gz
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libmission-control-plugins.so
%{_mandir}/man1/mc-tool.1.*
%{_mandir}/man1/mc-wait-for-name.1.*
%{_mandir}/man8/mission-control-5.8.*
#%{_datadir}/gtk-doc/*
# << files devel
