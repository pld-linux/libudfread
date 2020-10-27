#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	UDF reader library
Name:		libudfread
Version:	1.1.0
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	https://code.videolan.org/videolan/libudfread/-/archive/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	0502fc712c55ee507c8657742f998141
URL:		https://code.videolan.org/videolan/libudfread
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This library allows reading UDF filesystems, like raw devices and
image files. The library is created and maintained by VideoLAN Project
and is used by projects like VLC and Kodi.

%package devel
Summary:	Header files for libudfread library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libudfread library.

%package static
Summary:	Static libudfread library
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libudfread library.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{__enable_disable static_libs static}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog
%attr(755,root,root) %{_libdir}/libudfread.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libudfread.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libudfread.so
%{_includedir}/udfread
%{_pkgconfigdir}/udfread.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libudfread.a
%endif
