#
# Conditional build:
%bcond_with	x	# Use the X Windows System
%bcond_without	cgi	# Disable Local CGI support
%bcond_without	ipv6	# Disable IPv6 Support
%bcond_without	led	# Disable LEDs
%bcond_without	256	# Disable 256 colors support
%bcond_without	lua	# Disable Lua scripting
#
Summary:	Experimantal Links (text WWW browser)
Summary(es):	El links es un browser para modo texto, similar a lynx
Summary(pl):	Eksperymentalny Links (tekstowa przegl±darka WWW)
Summary(pt_BR):	O links é um browser para modo texto, similar ao lynx
Name:		elinks
Version:	0.10.0
Release:	1
Epoch:		1
License:	GPL
Group:		Applications/Networking
#Source0Download:	http://elinks.or.cz/download.html
Source0:	http://elinks.or.cz/download/%{name}-%{version}.tar.bz2
# Source0-md5:	09a199b496bcdaf54791f2010a8351b8
Source1:	%{name}.desktop
Source2:	links.png
#Patch0:		%{name}-pl.po.patch
Patch1:		%{name}-home_etc.patch
Patch2:		%{name}-lua40.patch
Patch3:		%{name}-content-type.patch
URL:		http://elinks.or.cz/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bzip2-devel
BuildRequires:	expat-devel
BuildRequires:	gettext-devel
BuildRequires:	gpm-devel
%{?with_lua:BuildRequires:	lua40-devel >= 4.0.1-9}
BuildRequires:	ncurses-devel => 5.1
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	sed >= 4.0
BuildRequires:	tetex
BuildRequires:	zlib-devel
Provides:	webclient
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/elinks
%define		specflags_ia32	-fomit-frame-pointer

%description
This is the elinks tree - intended to provide feature-rich version of
links, however not rock-stable and dedicated mainly for testing. Its
purpose is to make alternative to links, until Mikulas will have some
time to maintain it, and to test and tune various patches for Mikulas
to be able to include them in the official links releases.

%description -l es
Links es un browser WWW modo texto, similar al Lynx. El links muestra
tablas, hace baja archivos en segundo plano, y usa conexiones HTTP/1.1
keepalive.

%description -l pl
Bogata w opcje i mo¿liwo¶ci wersja tekstowej przegl±darki WWW - links.
elinks jednak jest dedykowana g³ównie do testowania.

%description -l pt_BR
Links é um browser WWW modo texto, similar ao Lynx. O Links exibe
tabelas, baixa arquivos em segundo plano, e usa as conexões HTTP/1.1
keepalive.

%prep
%setup -q
#%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

mv -f po/{no,nb}.po

%build
%{__sed} -i 's,\(^ALL_LINGUAS=.*\)\(no\),\1nb,' configure.in
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
%{!?debug:	--enable-fastmem} \
%{?debug:	--enable-debug} \
	%{!?with_ipv6:--disable-ipv6} \
	%{!?with_lua:--without-lua} \
	--with%{!?with_x:out}-x
%{?with_led:echo    '#define CONFIG_LEDS' >> feature.h}
%{?with_256:echo    '#define CONFIG_256_COLORS' >> feature.h}
%{?with_cgi:echo -e "#ifdef HAVE_SETENV\n\t#define CONFIG_CGI\n#endif" >> feature.h}
%{__make}

cd doc
texi2html elinks-lua.texi
cd ..

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_desktopdir} \
	$RPM_BUILD_ROOT%{_datadir}/%{name} \
	$RPM_BUILD_ROOT{%{_sysconfdir},%{_pixmapsdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.png

%{?with_lua:install contrib/lua/*.lua $RPM_BUILD_ROOT%{_sysconfdir}}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS BUGS ChangeLog NEWS README SITES TODO
%doc contrib/{keybind*,wipe-out-ssl*,lua/elinks-remote}
%doc contrib/conv/{*awk,*.pl,*.sh}
%doc doc/{*.txt,*.html}
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man*/*
%{_desktopdir}/*
%{_pixmapsdir}/*
%{?with_lua:%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}}
