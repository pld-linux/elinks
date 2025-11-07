#
# Conditional build:
# - protocols
%bcond_without	bittorrent	# BitTorrent protocol support
%bcond_without	curl		# FTPes, SFTP, HTTP/2, etc.
%bcond_without	fsp		# FSP support
%bcond_without	idn		# Internation Domain Names support
%bcond_without	ipv6		# IPv6 support
%bcond_with	smb		# smb protocol support (non-distib: recent libsmbclient is GPL v3)
%bcond_with	gnutls		# GNUTLS-based SSL support (instead of openssl)
%bcond_without	openssl		# OpenSSL-based SSL support
# - content
%bcond_without	cgi		# Local CGI support
%bcond_without	brotli		# Brotli compression support
%bcond_without	js		# experimental (yet quite usable) JavaScript support (using quickjs)
%bcond_without	libcss		# libcss support
%bcond_with	lzma		# LZMA support (old API, incompatible with xz-libs)
%bcond_without	zstd	# zstd compression support
# - scripting
%bcond_with	guile		# Guile scripting support (non-distrib: guile 2 is LGPL v3+)
%bcond_without	lua		# Lua scripting
%bcond_with	perl		# Perl scripting
%bcond_with	python		# Python scripting support
%bcond_with	ruby		# (experimental) Ruby scripting support
# - display and UI
%bcond_without	256		# 256 colors support
%bcond_without	led		# LEDs
%bcond_without	sixel		# image display support in SIXEL capable terminals
%bcond_without	truecolor	# true color
%bcond_with	x		# Use the X Window System
# - misc
%bcond_without	verbose		# verbose build (V=1)
%bcond_without	libevent	# build without libevent

%if %{with gnutls}
%undefine	with_openssl
%endif

%if %{without libcss}
%undefine	with_js
%endif

Summary:	Experimantal Links (text WWW browser)
Summary(es.UTF-8):	El links es un browser para modo texto, similar a lynx
Summary(pl.UTF-8):	Eksperymentalny Links (tekstowa przeglądarka WWW)
Summary(pt_BR.UTF-8):	O links é um browser para modo texto, similar ao lynx
Name:		elinks
Version:	0.18.0
Release:	2
Epoch:		1
License:	GPL v2
Group:		Applications/Networking
Source0:	https://github.com/rkd77/elinks/releases/download/v%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	43ac5edc5735117317827550607e9035
Source1:	%{name}.desktop
Source2:	links.png
Patch0:		quickjs.patch
URL:		http://www.elinks.cz/
BuildRequires:	bzip2-devel
%{?with_curl:BuildRequires:	curl-devel >= 7.66.0}
BuildRequires:	expat-devel
%{?with_fsp:BuildRequires:	fsplib-devel}
BuildRequires:	gettext-tools
BuildRequires:	git-core
%{?with_gnutls:BuildRequires:	gnutls-devel >= 1.2.5}
BuildRequires:	gpm-devel
%{?with_guile:BuildRequires: guile-devel}
%{?with_libcss:BuildRequires:	libCSS-devel >= 0.9.2}
%ifnarch %{arch_with_atomics64}
BuildRequires:	libatomic-devel
%endif
BuildRequires:	libstdc++-devel >= 6:8
BuildRequires:	rpmbuild(macros) >= 2.042
%{?with_js:BuildRequires:	sqlite3-devel}
%{?with_brotli:BuildRequires:	libbrotli-devel}
%if %{with js} || %{with libcss}
BuildRequires:	libdom-devel >= 0.4.2
%endif
%{?with_libevent:BuildRequires:	libevent-devel}
%{?with_idn:BuildRequires:	libidn2-devel}
%{?with_sixel:BuildRequires:	libsixel-devel}
%{?with_smb:BuildRequires:	libsmbclient-devel}
%{?with_lua:BuildRequires:	lua53-devel}
%{?with_lzma:BuildRequires:	lzma-devel}
BuildRequires:	meson >= 1.0.1
BuildRequires:	ncurses-devel >= 5.1
BuildRequires:	ninja >= 1.5
%{?with_openssl:BuildRequires:	openssl-devel >= 0.9.7d}
%{?with_perl:BuildRequires:	perl-devel}
BuildRequires:	pkgconfig
%{?with_python:BuildRequires:	python3-devel}
%{?with_js:BuildRequires:	quickjs-devel >= 20250426}
%{?with_ruby:BuildRequires:	ruby-devel}
BuildRequires:	sed
BuildRequires:	tar >= 1:1.22
BuildRequires:	tre-devel
BuildRequires:	which
BuildRequires:	xmlto
%{?with_js:BuildRequires:	xxd}
BuildRequires:	xz
BuildRequires:	zlib-devel
%{?with_zstd:BuildRequires:	zstd-devel}
%{?with_curl:Requires:	curl-libs >= 7.66.0}
%{?with_gnutls:Requires:	gnutls-libs >= 1.2.5}
%{?with_libcss:Requires:	libCSS >= 0.9.2}
%if %{with js} || %{with libcss}
Requires:	libdom >= 0.4.2
%endif
Requires:	ncurses >= 5.1
%{?with_openssl:Requires:	openssl >= 0.9.7d}
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
%setup -q
%patch -P0 -p1

%build
%meson \
	-Dapidoc=false \
	-Dhtmldoc=true \
	-Dpdfdoc=false \
	-Ddocdir=%{_docdir}/%{name}-%{version} \
	%{?with_bittorrent:-Dbittorrent=true} \
	%{?with_cgi:-Dcgi=true} \
	-D88-colors=true \
	%{?with_256:-D256-colors=true} \
	%{?with_truecolor:-Dtrue-color=true} \
	-Dexmode=true \
	%{?debug:-Ddebug=true} \
	%{!?debug:-Dfastmem=true} \
	-Dfinger=true \
	-Dfsp=%{__true_false fsp} \
	-Dgemini=true \
	-Dgettext=true \
	-Dgopher=true \
	-Dhtml-highlight=true \
	%{!?with_ipv6:-Dipv6=false} \
	%{?with_leds:-Dleds=true} \
	-Dlibsixel=%{__true_false sixel} \
	-Dmarks=true \
	-Dnntp=true \
	-Dno-root=false \
	%{?with_smb:-Dsmb=true} \
	%{?with_brotli:-Dbrotli=true} \
	%{?with_zstd:-Dzstd=true} \
	%{?with_gnutls:-Dgnutls=true} \
	%{?with_guile:-Dguile=true} \
	%{!?with_idn:-Didn=false} \
	%{?with_lua:-Dluapkg=lua5.3} \
	%{?with_lzma:-Dlzma=true} \
	%{?with_openssl:-Dopenssl=true} \
	%{?with_perl:-Dperl=true} \
	%{?with_python:-Dpython=true} \
	%{?with_ruby:-Druby=true} \
	%{?with_js:-Dquickjs=true} \
	%{?with_x:-Dx=true} \
	%{?with_libevent:-Dlibevent=true} \
	%{!?with_curl:-Dlibcurl=false} \
	%{!?with_libcss:-Dlibcss=false}

%meson_build

%install
rm -rf $RPM_BUILD_ROOT
%meson_install

install -d $RPM_BUILD_ROOT%{_desktopdir} \
	$RPM_BUILD_ROOT%{_datadir}/%{name} \
	$RPM_BUILD_ROOT{%{_sysconfdir},%{_pixmapsdir}}

cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
cp -a %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.png

%{?with_lua:install contrib/lua/*.lua $RPM_BUILD_ROOT%{_sysconfdir}}
sed -i -e 's|bin/lua|bin/lua5.3|g' $RPM_BUILD_ROOT%{_sysconfdir}/*lua

install AUTHORS BUGS ChangeLog NEWS README.md SITES TODO $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
install contrib/{keybind*,wipe-out-ssl*,lua/elinks-remote} contrib/conv/{*awk,*.pl,*.sh} $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%{_docdir}/%{name}-%{version}
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
