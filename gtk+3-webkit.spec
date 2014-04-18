Summary:	Port of WebKit embeddable web component to GTK+3
Name:		gtk+3-webkit
Version:	2.4.1
Release:	1
License:	BSD-like
Group:		X11/Libraries
Source0:	http://webkitgtk.org/releases/webkitgtk-%{version}.tar.xz
# Source0-md5:	c57ebecff1ba7663b303e21a64840c48
URL:		http://www.webkitgtk.org/
BuildRequires:	EGL-devel
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	curl-devel
BuildRequires:	enchant-devel
BuildRequires:	flex
BuildRequires:	fontconfig-devel
BuildRequires:	geoclue-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	gperf
BuildRequires:	gstreamer-plugins-base-devel
BuildRequires:	gtk+-devel
BuildRequires:	gtk+3-devel
BuildRequires:	icu-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	librsvg-devel
BuildRequires:	libsoup-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	libwebp-devel
BuildRequires:	libxslt-devel
BuildRequires:	pkg-config
BuildRequires:	ruby
BuildRequires:	sqlite3-devel
BuildRequires:	xorg-libXft-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	    %{_libdir}/webkit2gtk-3.0

# unresolved, not sure how bad is it
#   _ZSt11__once_call
#   _ZSt15__once_callable
%define		skip_post_check_so  libwebkit2gtk-3.0.so.* libwebkitgtk-3.0.so.* libjavascriptcoregtk-3.0.so.*

%description
webkit is a port of the WebKit embeddable web component to GTK+.

%package devel
Summary:	Development files for webkit
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Development files for webkit.

%package apidocs
Summary:	WebKitGTK API documentation
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
WebKitGTK API documentation.

%package demo
Summary:	Demo GTK+/webkit application
Group:		Applications
Requires:	%{name} = %{version}-%{release}

%description demo
Simple GTK+/webkit based browser.

%prep
%setup -qn webkitgtk-%{version}

%build
%{__libtoolize}
%{__aclocal} -I Source/autotools
%{__autoheader}
%{__automake}
%{__autoconf}

# https://bugs.webkit.org/show_bug.cgi?id=91154
export CFLAGS="%(echo %{rpmcflags} | sed 's/ -g2/ -g1/g')"
export CXXFLAGS="%(echo %{rpmcxxflags} | sed 's/ -g2/ -g1/g')"
export LDFLAGS="%{rpmldflags}"
%configure \
	--disable-schemas-compile	\
	--disable-silent-rules		\
	--enable-geolocation		\
	--enable-introspection		\
	--enable-spellcheck		\
	--with-gtk=3.0			\
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la
%{__rm} $RPM_BUILD_ROOT%{_libexecdir}/injected-bundle/*.la

%find_lang WebKitGTK-3.0

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/ldconfig
%postun	-p /usr/sbin/ldconfig

%files -f WebKitGTK-3.0.lang
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libjavascriptcoregtk-*.so.0
%attr(755,root,root) %ghost %{_libdir}/libwebkitgtk-*.so.0
%attr(755,root,root) %{_libdir}/libjavascriptcoregtk-*.so.*.*.*
%attr(755,root,root) %{_libdir}/libwebkitgtk-*.so.*.*.*
%{_libdir}/girepository-1.0/*.typelib

%dir %{_libexecdir}
%dir %{_libexecdir}/injected-bundle
%attr(755,root,root) %ghost %{_libdir}/libwebkit2gtk-3.0.so.25
%attr(755,root,root) %{_libdir}/libwebkit2gtk-3.0.so.*.*.*
%attr(755,root,root) %{_libexecdir}/WebKitNetworkProcess
%attr(755,root,root) %{_libexecdir}/WebKitPluginProcess
%attr(755,root,root) %{_libexecdir}/WebKitWebProcess
%attr(755,root,root) %{_libexecdir}/injected-bundle/libwebkit2gtkinjectedbundle.so

%dir %{_datadir}/webkitgtk-3.0
%{_datadir}/webkitgtk-3.0/images
%{_datadir}/webkitgtk-3.0/resources

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/jsc-3
%attr(755,root,root) %{_libdir}/*.so
%{_includedir}/webkitgtk-3.0
%{_pkgconfigdir}/*.pc
%{_datadir}/gir-1.0/*.gir

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/webkit2gtk
%{_gtkdocdir}/webkitdomgtk
%{_gtkdocdir}/webkitgtk

