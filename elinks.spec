#
# Conditional build:
# - protocols
%bcond_without	bittorrent	# BitTorrent protocol support
%bcond_without	fsp		# FSP support
%bcond_without	idn		# Internation Domain Names support
%bcond_without	ipv6		# IPv6 support
%bcond_with	smb		# smb protocol support (non-distib: recent libsmbclient is GPL v3)
%bcond_with	gnutls		# GNUTLS-based SSL support (instead of openssl)
%bcond_without	openssl		# OpenSSL-based SSL support
# - content
%bcond_without	cgi		# Local CGI support
%bcond_with	brotli		# Brotli compression support
%bcond_without	js		# experimental (yet quite usable) JavaScript support (using SpiderMonkey)
%bcond_with	lzma		# LZMA support (old API, incompatible with xz-libs)
# - scripting
%bcond_with	guile		# Guile scripting support (non-distrib: guile 2 is LGPL v3+)
%bcond_without	lua		# Lua scripting
%bcond_without	perl		# Perl scripting
%bcond_with	python		# Python scripting support
%bcond_with	ruby		# (experimental) Ruby scripting support
# - display and UI
%bcond_without	256		# 256 colors support
%bcond_without	led		# LEDs
%bcond_without	truecolor	# true color
%bcond_with	olderisbetter	# variuos pre-0.10.0 behaviour rules (typeahead and esc-esc)
%bcond_with	x		# Use the X Window System
# - misc
%bcond_without	verbose		# verbose build (V=1)

%if %{with gnutls}
%undefine	with_openssl
%endif

Summary:	Experimantal Links (text WWW browser)
Summary(es.UTF-8):	El links es un browser para modo texto, similar a lynx
Summary(pl.UTF-8):	Eksperymentalny Links (tekstowa przeglądarka WWW)
Summary(pt_BR.UTF-8):	O links é um browser para modo texto, similar ao lynx
Name:		elinks
Version:	0.13
%define	snap	20180901
%define	rel	8
Release:	4.%{snap}.%{rel}
Epoch:		1
License:	GPL v2
Group:		Applications/Networking
# github gives different archive on each download
# http://www.elinks.cz/download/%{name}-current-%{version}.tar.bz2
Source0:	http://elinks.cz/download/elinks-current-%{version}.tar.bz2
# Source0-md5:	6e45361ed14855ad02d3ae9b7a6ad809
Source1:	%{name}.desktop
Source2:	links.png
Patch0:		%{name}-home_etc.patch
Patch1:		lua53.patch
Patch2:		%{name}-date-format.patch
Patch3:		%{name}-old_incremental.patch
Patch4:		%{name}-0.10.0-0.9.3-typeahead-beginning.patch
Patch5:		%{name}-double-esc.patch
Patch6:		js187.patch
URL:		http://www.elinks.cz/
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake
BuildRequires:	bzip2-devel
BuildRequires:	expat-devel
%{?with_fsp:BuildRequires:	fsplib-devel}
BuildRequires:	gettext-tools
%{?with_gnutls:BuildRequires:	gnutls-devel >= 1.2.5}
BuildRequires:	gpm-devel
%{?with_guile:BuildRequires: guile-devel}
#BuildRequires:	heimdal-devel
%{?with_js:BuildRequires:	js187-devel}
%{?with_brotli:BuildRequires:	libbrotli-devel}
%{?with_idn:BuildRequires:	libidn-devel}
%{?with_smb:BuildRequires:	libsmbclient-devel}
%{?with_lua:BuildRequires:	lua-devel >= 5.3}
%{?with_lzma:BuildRequires:	lzma-devel}
BuildRequires:	ncurses-devel >= 5.1
%{?with_openssl:BuildRequires:	openssl-devel >= 0.9.7d}
%{?with_perl:BuildRequires:	perl-devel}
BuildRequires:	pkgconfig
%{?with_python:BuildRequires:	python-devel}
%{?with_ruby:BuildRequires:	ruby-devel}
BuildRequires:	tre-devel
BuildRequires:	which
BuildRequires:	zlib-devel
Suggests:	mailcap
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

%description -l es.UTF-8
Links es un browser WWW modo texto, similar al Lynx. El links muestra
tablas, hace baja archivos en segundo plano, y usa conexiones HTTP/1.1
keepalive.

%description -l pl.UTF-8
Bogata w opcje i możliwości wersja tekstowej przeglądarki WWW - links.
elinks jednak jest dedykowana głównie do testowania.

%description -l pt_BR.UTF-8
Links é um browser WWW modo texto, similar ao Lynx. O Links exibe
tabelas, baixa arquivos em segundo plano, e usa as conexões HTTP/1.1
keepalive.

%prep
%setup -q -n %{name}-%{version}-%{snap}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%if %{with olderisbetter}
%patch3 -p1
%patch4 -p1
%patch5 -p1
%endif
%patch6 -p1

%build
cp -f /usr/share/automake/config.sub config
%{__aclocal}
%{__autoconf}
%{__autoheader}
%configure \
	%{?with_bittorrent:--enable-bittorrent} \
	%{?with_cgi:--enable-cgi} \
	--enable-88-colors \
	%{?with_256:--enable-256-colors} \
	%{?with_truecolor:--enable-true-color} \
	--enable-exmode \
	%{?debug:--enable-debug} \
	%{!?debug:--enable-fastmem} \
	--enable-finger \
	%{?with_fsp:--enable-fsp} \
	--enable-gopher \
	--enable-html-highlight \
	%{!?with_ipv6:--disable-ipv6} \
	%{?with_leds:--enable-leds} \
	--enable-marks \
	--enable-nntp \
	--disable-no-root \
	%{?with_smb:--enable-smb} \
	%{!?with_brotli:--without-brotli} \
	--without-gc \
	%{?with_gnutls:--with-gnutls} \
	%{?with_guile:--with-guile} \
	%{!?with_idn:--without-idn} \
	%{!?with_lua:--without-lua} \
	%{!?with_lzma:--without-lzma} \
	%{!?with_openssl:--without-openssl} \
	%{?with_perl:--with-perl} \
	%{?with_python:--with-python} \
	%{?with_ruby:--with-ruby} \
	%{!?with_js:--without-spidermonkey} \
	--with-x%{!?with_x:=no}
# xterm -e is default, one might want to change it to something else:
#	--with-xterm="xterm -e"

%{__make} %{?with_verbose:V=1}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_desktopdir} \
	$RPM_BUILD_ROOT%{_datadir}/%{name} \
	$RPM_BUILD_ROOT{%{_sysconfdir},%{_pixmapsdir}}

%{__make} install %{?with_verbose:V=1} \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_datadir}/locale/locale.alias

cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
cp -a %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.png

%{?with_lua:install contrib/lua/*.lua $RPM_BUILD_ROOT%{_sysconfdir}}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS BUGS ChangeLog NEWS README SITES TODO doc/html/*.html
%doc contrib/{keybind*,wipe-out-ssl*,lua/elinks-remote} contrib/conv/{*awk,*.pl,*.sh}
%attr(755,root,root) %{_bindir}/elinks
%{_mandir}/man1/elinks.1*
%{_mandir}/man5/elinks.conf.5*
%{_mandir}/man5/elinkskeys.5*
%{_desktopdir}/elinks.desktop
%{_pixmapsdir}/elinks.png
%if %{with lua}
%dir %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.lua
%endif
